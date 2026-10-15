"""API endpoints for post lifecycle and moderation workflow."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.moderation import moderate_content

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.PostResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_post",
    summary="Create a draft post",
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


@router.post(
    "/{post_id}/submit/",
    response_model=schemas.PostSubmitResponse,
    operation_id="submit_post",
    summary="Submit post for review",
)
def submit_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found.",
        )
    if post.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Post is already in '{post.status}' status. "
                "Only draft posts can be submitted for review."
            ),
        )

    is_approved, reasons = moderate_content(post.title, post.content)
    new_status = "approved" if is_approved else "flagged"
    flagged_reasons_str = " | ".join(reasons) if reasons else None

    updated_post = crud.update_post_status(
        db=db,
        post=post,
        status=new_status,
        flagged_reasons=flagged_reasons_str,
    )

    if is_approved:
        message = "Post has been approved and is ready to be published."
    else:
        message = f"Post has been flagged. Reason(s): {flagged_reasons_str}"

    return schemas.PostSubmitResponse(
        id=updated_post.id,
        status=updated_post.status,
        flagged_reasons=updated_post.flagged_reasons,
        message=message,
    )


@router.get(
    "/",
    response_model=schemas.PostListResponse,
    operation_id="list_posts",
    summary="List posts",
)
def list_posts(
    status: Optional[str] = Query(
        default=None,
        description="Filter by post status",
        pattern="^(draft|flagged|approved|published)$",
    ),
    skip: int = Query(default=0, ge=0, description="Offset for pagination"),
    limit: int = Query(default=100, ge=1, le=500, description="Limit per page"),
    db: Session = Depends(get_db),
):
    posts = crud.get_posts(db=db, status=status, skip=skip, limit=limit)
    total = crud.count_posts(db=db, status=status)
    return schemas.PostListResponse(posts=posts, total=total)


@router.patch(
    "/{post_id}/publish/",
    response_model=schemas.PostPublishResponse,
    operation_id="publish_post",
    summary="Publish an approved post",
)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found.",
        )
    if post.status == "published":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post is already published.",
        )
    if post.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only approved posts can be published.",
        )

    updated_post = crud.update_post_status(db=db, post=post, status="published")

    return schemas.PostPublishResponse(
        id=updated_post.id,
        status=updated_post.status,
        message="Post has been successfully published and is now read-only.",
    )


@router.get(
    "/{post_id}",
    response_model=schemas.PostResponse,
    operation_id="get_post",
    summary="Get post details",
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found.",
        )
    return post
