"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts


def create_app() -> FastAPI:
    app = FastAPI(
        title="ContentMod API",
        description="Create blog posts, run them through automated moderation, and publish the approved ones.",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "posts",
                "description": "Create, review and publish posts",
            }
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Schema is owned by Alembic (`alembic upgrade head`), not create_all.
    app.include_router(posts.router, prefix="/posts", tags=["posts"])

    @app.get("/", tags=["health"])
    def read_root():
        return {
            "message": "Content Moderation Platform API",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    return app
