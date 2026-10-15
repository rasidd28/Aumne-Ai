# ContentMod

A small blogging platform where every post goes through automated moderation before it can be published.

- **Backend:** FastAPI + SQLite, migrations with Alembic
- **Frontend:** React + Axios (talks to the API only)
- **SDK:** Python client generated with OpenAPI Generator CLI
- **Tests:** pytest

## How it works

1. Create a post. It starts as a `draft`.
2. Submit it for review. The moderation check marks it `approved` or `flagged`, and says why if flagged.
3. Publish an approved post. Published posts are read-only; there is no endpoint that can change them.

Only drafts can be submitted, and only approved posts can be published. Anything else returns `409`.

## Moderation rules

| Rule | What gets flagged |
|---|---|
| Length | Under 50 or over 2000 characters |
| Banned words | Any word from the sample profanity/insult list (whole words only) |
| Tone | More than 60% uppercase (8+ letters), or 4+ `!`/`?` in a row |

A post can break several rules at once, and every reason is returned. For example, `THIS IS UNACCEPTABLE!` is flagged as too short and aggressive.

## Requirements

- Python 3.9+
- Node.js 16+
- Java 11+ (only needed to generate the SDK)

## Setup and run

```bat
setupdev.bat
runapplication.bat
```

`setupdev.bat` creates the virtualenv, installs dependencies, runs the migrations, loads the sample data and installs the frontend packages. `runapplication.bat` opens the backend and frontend in two windows.

- App: http://localhost:3000
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

If you have an old `content_mod.db` from before the migrations existed, delete it before running setup.

### Manual steps

```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python seed.py        # optional sample data, skipped if the table has rows
python main.py

# in another terminal
cd frontend
npm install
npm start
```

## API

| Method | Path | Description |
|---|---|---|
| POST | `/posts/` | Create a draft |
| POST | `/posts/{id}/submit/` | Submit for review |
| GET | `/posts/` | List posts, optional `?status=draft\|flagged\|approved\|published` |
| PATCH | `/posts/{id}/publish/` | Publish an approved post |
| GET | `/posts/{id}` | Get one post |

Errors: `404` post not found, `409` invalid status change, `422` invalid input.

## Python SDK

Run this from the project root (after `setupdev.bat`):

```bat
generate_sdk.bat
```

It checks for Java and the generator CLI (installing the CLI if needed), starts the backend if it isn't already running, generates `moderation_sdk/`, installs it into the backend virtualenv, runs `sdk_usage_example.py` as a smoke test, and stops the backend again if it started it.

Usage:

```python
from moderation_sdk import ApiClient, Configuration
from moderation_sdk.api.posts_api import PostsApi
from moderation_sdk.models.post_create import PostCreate

api = PostsApi(ApiClient(Configuration(host="http://localhost:8000")))

post = api.create_post(PostCreate(title="Hello", content="..."))
review = api.submit_post(post_id=post.id)
if review.status == "approved":
    api.publish_post(post_id=post.id)
```

## Tests

```bat
cd backend
env\Scripts\activate
pytest -v
```

## Frontend

Create and save drafts, submit for review (with the flag reasons shown), filter by status, publish approved posts, and read published ones in a read-only view. The list refreshes every 15 seconds, and there is a dashboard with charts.
