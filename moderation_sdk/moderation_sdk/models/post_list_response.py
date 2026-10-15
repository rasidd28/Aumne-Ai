from moderation_sdk.models.post_response import PostResponse


class PostListResponse:
    def __init__(self, posts=None, total: int = 0, **kwargs):
        self.posts = [p if isinstance(p, PostResponse) else PostResponse(**p) for p in (posts or [])]
        self.total = total
