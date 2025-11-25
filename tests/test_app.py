from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    test_email = "test.student@mergington.edu"

    # Ensure not already present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]
    assert resp.json()["message"].startswith("Signed up")

    # Attempt duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp2.status_code == 400

    # Unregister
    resp3 = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp3.status_code == 200
    assert test_email not in activities[activity]["participants"]
    assert resp3.json()["message"].startswith("Unregistered")

    # Unregistering again returns 404
    resp4 = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp4.status_code == 404


def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/Nonexistent/participants?email=foo@bar.com")
    assert resp.status_code == 404
