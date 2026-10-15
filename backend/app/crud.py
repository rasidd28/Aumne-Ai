from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas


def create_post(db: Session, post: schemas.PostCreate) -> models.Post:
    record = models.Post(
        title=post.title,
        content=post.content,
        status="draft",
        flagged_reasons=None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(
    db: Session,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Post]:
    query = db.query(models.Post)
    if status:
        query = query.filter(models.Post.status == status)
    return query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()


def count_posts(db: Session, status: Optional[str] = None) -> int:
    query = db.query(models.Post)
    if status:
        query = query.filter(models.Post.status == status)
    return query.count()


def update_post_status(
    db: Session,
    post: models.Post,
    status: str,
    flagged_reasons: Optional[str] = None,
) -> models.Post:
    post.status = status
    if flagged_reasons is not None:
        post.flagged_reasons = flagged_reasons
    db.commit()
    db.refresh(post)
    return post
