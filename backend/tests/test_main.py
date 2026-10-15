import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.database import Base, get_db
from app.moderation import (
    moderate_content,
    _check_length,
    _check_banned_words,
    _check_tone,
)

TEST_DATABASE_URL = "sqlite:///./test_content_mod.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=test_engine)


VALID_CONTENT = (
    "Engineering reliable backend services requires thorough integration testing, "
    "pragmatic API design, and disciplined operational monitoring across deployments."
)

SHORT_CONTENT = "Draft notes."

CAPS_CONTENT = "THIS WHOLE ANNOUNCEMENT IS SHOUTED IN ALL CAPS WITHOUT ANY LOWERCASE LETTERS."

BANNED_CONTENT = (
    "I hate this platform, it is worthless garbage run by complete idiots who destroy everything."
)


class TestModerationLength:
    def test_content_too_short_flagged(self):
        approved, reasons = moderate_content("Article Title", "Short.")
        assert not approved
        assert any("too short" in r.lower() for r in reasons)

    def test_content_minimum_length_passes(self):
        content = "A" * 50
        approved, reasons = moderate_content("Article Title", content)
        length_issues = [r for r in reasons if "short" in r.lower() or "long" in r.lower()]
        assert len(length_issues) == 0

    def test_content_too_long_flagged(self):
        content = "A" * 2001
        approved, reasons = moderate_content("Article Title", content)
        assert not approved
        assert any("too long" in r.lower() for r in reasons)

    def test_content_exact_minimum_passes(self):
        content = "x" * 50
        reasons = _check_length(content)
        assert len(reasons) == 0

    def test_content_exact_maximum_passes(self):
        content = "x" * 2000
        reasons = _check_length(content)
        assert len(reasons) == 0

    def test_content_one_over_max_flagged(self):
        content = "x" * 2001
        reasons = _check_length(content)
        assert len(reasons) == 1
        assert "too long" in reasons[0].lower()


class TestModerationBannedWords:
    def test_banned_word_flagged(self):
        reasons = _check_banned_words("Title", "You are a stupid person.")
        assert len(reasons) == 1
        assert "stupid" in reasons[0]

    def test_banned_word_in_title_flagged(self):
        reasons = _check_banned_words("Stupid title", "Normal content here.")
        assert len(reasons) == 1

    def test_banned_word_case_insensitive(self):
        reasons = _check_banned_words("Title", "You are an IDIOT.")
        assert len(reasons) == 1

    def test_partial_match_not_flagged(self):
        assert _check_banned_words("Title", "A classic shell script about assets.") == []

    def test_no_banned_words_passes(self):
        reasons = _check_banned_words(
            "My Blog",
            "This is a thoughtful article explaining core architectural concepts.",
        )
        assert len(reasons) == 0

    def test_multiple_banned_words_flagged(self):
        approved, reasons = moderate_content("Title", BANNED_CONTENT * 3)
        assert not approved


class TestModerationTone:
    def test_all_caps_flagged(self):
        reasons = _check_tone(CAPS_CONTENT)
        assert len(reasons) >= 1
        assert any("aggressive" in r.lower() or "caps" in r.lower() for r in reasons)

    def test_normal_case_passes(self):
        reasons = _check_tone(VALID_CONTENT)
        assert len(reasons) == 0

    def test_excessive_exclamation_flagged(self):
        reasons = _check_tone("This is great!!!! You must buy it!!!!")
        assert any("punctuation" in r.lower() for r in reasons)

    def test_short_caps_not_penalized(self):
        reasons = _check_tone("OK DONE")
        assert not any("aggressive" in r.lower() for r in reasons)


class TestModerationFullPipeline:
    def test_polite_300char_post_approved(self):
        content = (
            "This is an insightful discussion regarding system architecture and distributed workflows. "
            "It breaks down complex trade-offs into practical steps that software engineering teams "
            "can implement when scaling high-concurrency microservices safely."
        )
        approved, reasons = moderate_content("Technical Architecture", content)
        assert approved
        assert reasons == []

    def test_short_caps_post_flagged_multiple_reasons(self):
        approved, reasons = moderate_content("URGENT", "VERY SHORT")
        assert not approved
        assert len(reasons) >= 1

    def test_profanity_flagged(self):
        content = "x" * 100 + " I hate this garbage product."
        approved, reasons = moderate_content("Post", content)
        assert not approved


class TestCreatePost:
    def test_create_draft_post_success(self, client):
        response = client.post("/posts/", json={"title": "Hello World", "content": VALID_CONTENT})
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "draft"
        assert data["title"] == "Hello World"
        assert data["flagged_reasons"] is None

    def test_create_post_missing_title(self, client):
        response = client.post("/posts/", json={"content": VALID_CONTENT})
        assert response.status_code == 422

    def test_create_post_missing_content(self, client):
        response = client.post("/posts/", json={"title": "Title Only"})
        assert response.status_code == 422

    def test_create_post_empty_title(self, client):
        response = client.post("/posts/", json={"title": "", "content": VALID_CONTENT})
        assert response.status_code == 422


class TestGetPost:
    def test_get_existing_post(self, client):
        create_resp = client.post("/posts/", json={"title": "Test Get", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        response = client.get(f"/posts/{post_id}")
        assert response.status_code == 200
        assert response.json()["id"] == post_id

    def test_get_nonexistent_post_returns_404(self, client):
        response = client.get("/posts/99999")
        assert response.status_code == 404

    def test_get_post_has_required_fields(self, client):
        create_resp = client.post("/posts/", json={"title": "Fields Test", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        data = client.get(f"/posts/{post_id}").json()
        for field in ["id", "title", "content", "status", "created_at"]:
            assert field in data


class TestListPosts:
    def test_list_all_posts(self, client):
        response = client.get("/posts/")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
        assert "total" in data

    def test_list_posts_filter_by_draft(self, client):
        response = client.get("/posts/?status=draft")
        assert response.status_code == 200
        data = response.json()
        for post in data["posts"]:
            assert post["status"] == "draft"

    def test_list_posts_invalid_status(self, client):
        response = client.get("/posts/?status=invalid_status")
        assert response.status_code == 422

    def test_list_posts_filter_by_approved(self, client):
        response = client.get("/posts/?status=approved")
        assert response.status_code == 200


class TestSubmitPost:
    def test_submit_valid_post_approved(self, client):
        create_resp = client.post("/posts/", json={"title": "Good Post", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "approved"
        assert data["flagged_reasons"] is None

    def test_submit_short_content_flagged(self, client):
        create_resp = client.post("/posts/", json={"title": "Short", "content": "Too short."})
        post_id = create_resp.json()["id"]
        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "flagged"
        assert data["flagged_reasons"] is not None
        assert "short" in data["flagged_reasons"].lower()

    def test_submit_all_caps_content_flagged(self, client):
        create_resp = client.post("/posts/", json={"title": "CAPS POST", "content": CAPS_CONTENT})
        post_id = create_resp.json()["id"]
        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 200
        assert response.json()["status"] == "flagged"

    def test_submit_banned_words_flagged(self, client):
        content = "x" * 50 + " I hate this worthless garbage product. It is for idiots."
        create_resp = client.post("/posts/", json={"title": "Rant", "content": content})
        post_id = create_resp.json()["id"]
        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 200
        assert response.json()["status"] == "flagged"

    def test_submit_already_submitted_returns_conflict(self, client):
        create_resp = client.post("/posts/", json={"title": "Re-submit Test", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 409

    def test_submit_nonexistent_post_returns_404(self, client):
        response = client.post("/posts/99999/submit/")
        assert response.status_code == 404


class TestPublishPost:
    def test_publish_approved_post_success(self, client):
        create_resp = client.post("/posts/", json={"title": "Publish Me", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        response = client.patch(f"/posts/{post_id}/publish/")
        assert response.status_code == 200
        assert response.json()["status"] == "published"

    def test_publish_draft_post_fails(self, client):
        create_resp = client.post("/posts/", json={"title": "Draft Publish", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        response = client.patch(f"/posts/{post_id}/publish/")
        assert response.status_code == 409
        assert "Only approved posts can be published." in response.json()["detail"]

    def test_publish_flagged_post_fails(self, client):
        create_resp = client.post("/posts/", json={"title": "Flag Publish", "content": "Short."})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        response = client.patch(f"/posts/{post_id}/publish/")
        assert response.status_code == 409
        assert "Only approved posts can be published." in response.json()["detail"]

    def test_publish_already_published_returns_conflict(self, client):
        create_resp = client.post("/posts/", json={"title": "Already Published", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        client.patch(f"/posts/{post_id}/publish/")
        response = client.patch(f"/posts/{post_id}/publish/")
        assert response.status_code == 409

    def test_publish_nonexistent_post_returns_404(self, client):
        response = client.patch("/posts/99999/publish/")
        assert response.status_code == 404

    def test_published_post_is_read_only(self, client):
        create_resp = client.post("/posts/", json={"title": "Read Only", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        client.patch(f"/posts/{post_id}/publish/")

        response = client.post(f"/posts/{post_id}/submit/")
        assert response.status_code == 409

    def test_published_post_in_filter(self, client):
        create_resp = client.post("/posts/", json={"title": "Filter Published", "content": VALID_CONTENT})
        post_id = create_resp.json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        client.patch(f"/posts/{post_id}/publish/")

        list_resp = client.get("/posts/?status=published")
        ids = [p["id"] for p in list_resp.json()["posts"]]
        assert post_id in ids


class TestSpecExamples:
    def test_20_char_all_caps_flagged_short_and_aggressive(self):
        content = "THIS IS UNACCEPTABLE!"  # 21 chars
        approved, reasons = moderate_content("Title", content)
        assert not approved
        joined = " ".join(reasons).lower()
        assert "too short" in joined
        assert "aggressive" in joined

    def test_profanity_reason_names_the_word(self):
        content = "This was a thoughtful and well researched article, but the author is an idiot."
        approved, reasons = moderate_content("Review", content)
        assert not approved
        assert any("idiot" in r for r in reasons)


class TestImmutability:
    def _published_id(self, client):
        post_id = client.post("/posts/", json={"title": "Locked", "content": VALID_CONTENT}).json()["id"]
        client.post(f"/posts/{post_id}/submit/")
        client.patch(f"/posts/{post_id}/publish/")
        return post_id

    def test_no_endpoint_can_edit_published_content(self, client):
        post_id = self._published_id(client)
        for method in (client.put, client.patch, client.delete):
            assert method(f"/posts/{post_id}").status_code == 405
        data = client.get(f"/posts/{post_id}").json()
        assert data["content"] == VALID_CONTENT
        assert data["status"] == "published"


class TestHealthEndpoint:
    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
