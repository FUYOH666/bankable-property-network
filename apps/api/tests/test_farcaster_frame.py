from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_frame_attest_renders_frame_meta_tags() -> None:
    r = client.get("/api/frame/attest?deal_id=0xabc&decision=approve")
    assert r.status_code == 200
    body = r.text
    assert '<meta property="fc:frame" content="vNext"' in body
    assert 'fc:frame:image' in body
    assert 'fc:frame:button:1' in body
    assert 'fc:frame:post_url' in body
    assert "/api/frame/image" in body


def test_frame_image_serves_svg() -> None:
    r = client.get("/api/frame/image?deal_id=0xabc&decision=approve")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/svg+xml")
    assert "<svg" in r.text
    assert "VERIFIED" in r.text


def test_frame_image_reject_decision() -> None:
    r = client.get("/api/frame/image?deal_id=0xdef&decision=reject")
    assert r.status_code == 200
    assert "REJECTED" in r.text


def test_frame_image_pending_default() -> None:
    r = client.get("/api/frame/image")
    assert r.status_code == 200
    assert "PENDING" in r.text


def test_frame_post_bounces_to_get() -> None:
    r = client.post("/api/frame/attest")
    assert r.status_code == 200
    assert "fc:frame" in r.text
