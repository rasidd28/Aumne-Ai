"""Sample script demonstrating programmatic post creation and publication using the Python SDK."""
import sys
import os

# The outer moderation_sdk/ directory is the distribution root; the actual Python
# package lives one level deeper inside it.  Insert that path so Python finds
# the real package (which has __init__.py) before the CWD namespace shadow.
_sdk_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moderation_sdk")
if _sdk_root not in sys.path:
    sys.path.insert(0, _sdk_root)

from moderation_sdk import ApiClient, Configuration
from moderation_sdk.api.posts_api import PostsApi
from moderation_sdk.models.post_create import PostCreate

config = Configuration(host="http://localhost:8000")
client = ApiClient(configuration=config)
posts_api = PostsApi(client)


def _call(api_instance, method_names, *args, **kwargs):
    for name in method_names:
        fn = getattr(api_instance, name, None)
        if callable(fn):
            return fn(*args, **kwargs)
    available = [m for m in dir(api_instance) if not m.startswith("_")]
    raise AttributeError(
        f"None of {method_names} found on {type(api_instance).__name__}. Available: {available}"
    )


def run_demo():
    print("Connecting to ContentMod API at http://localhost:8000 ...")

    # 1. Create a draft article
    payload = PostCreate(
        title="Scaling Background Workers with Asyncio",
        content=(
            "Asynchronous worker pools enable high-throughput task processing while keeping memory "
            "footprints predictable. Combining asyncio queues with graceful shutdown handling ensures "
            "that inflight jobs finish cleanly during production deployments."
        ),
    )
    post = _call(
        posts_api,
        ["create_post", "create_post_posts_post", "create_post_posts__post"],
        payload,
    )
    print(f"Created post #{post.id} — Status: {post.status}")

    # 2. Submit for moderation review
    print(f"Submitting post #{post.id} for review...")
    result = _call(
        posts_api,
        [
            "submit_post",
            "submit_post_posts_post_id_submit_post",
            "submit_post_posts__post_id__submit__post",
        ],
        post_id=post.id,
    )
    print(f"Review result: {result.status} — {result.message}")

    # 3. Publish if approved
    if result.status == "approved":
        print(f"Publishing post #{post.id}...")
        published = _call(
            posts_api,
            [
                "publish_post",
                "publish_post_posts_post_id_publish_patch",
                "publish_post_posts__post_id__publish__patch",
            ],
            post_id=post.id,
        )
        print(f"Publish message: {published.message}")
    else:
        print(f"Post flagged: {result.flagged_reasons}")

    # 4. Query published articles
    listing = _call(
        posts_api,
        ["list_posts", "list_posts_posts_get", "list_posts_posts__get"],
        status="published",
    )
    print(f"\nPublished posts ({listing.total} total):")
    for item in listing.posts:
        print(f" - #{item.id}: {item.title}")


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as exc:
        print(f"Error during execution: {exc}")
        print("Verify backend is reachable on port 8000.")
