from moderation_sdk.api_client import ApiClient
from moderation_sdk.models.post_response import PostResponse
from moderation_sdk.models.post_submit_response import PostSubmitResponse
from moderation_sdk.models.post_publish_response import PostPublishResponse
from moderation_sdk.models.post_list_response import PostListResponse


class PostsApi:
    def __init__(self, api_client: ApiClient = None):
        self.api_client = api_client or ApiClient()

    def create_post(self, post_create, **kwargs) -> PostResponse:
        body = post_create.to_dict() if hasattr(post_create, "to_dict") else dict(post_create)
        res = self.api_client.call_api("/posts/", method="POST", body=body)
        return PostResponse(**res)

    create_post_posts_post = create_post
    create_post_posts__post = create_post

    def submit_post(self, post_id: int, **kwargs) -> PostSubmitResponse:
        res = self.api_client.call_api(f"/posts/{post_id}/submit/", method="POST")
        return PostSubmitResponse(**res)

    submit_post_posts_post_id_submit_post = submit_post
    submit_post_posts__post_id__submit__post = submit_post

    def publish_post(self, post_id: int, **kwargs) -> PostPublishResponse:
        res = self.api_client.call_api(f"/posts/{post_id}/publish/", method="PATCH")
        return PostPublishResponse(**res)

    publish_post_posts_post_id_publish_patch = publish_post
    publish_post_posts__post_id__publish__patch = publish_post

    def list_posts(self, status: str = None, skip: int = 0, limit: int = 100, **kwargs) -> PostListResponse:
        params = {"status": status, "skip": skip, "limit": limit}
        res = self.api_client.call_api("/posts/", method="GET", params=params)
        return PostListResponse(**res)

    list_posts_posts_get = list_posts
    list_posts_posts__get = list_posts

    def get_post(self, post_id: int, **kwargs) -> PostResponse:
        res = self.api_client.call_api(f"/posts/{post_id}", method="GET")
        return PostResponse(**res)

    get_post_posts_post_id_get = get_post
    get_post_posts__post_id__get = get_post
