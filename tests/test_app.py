import sys
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = f"{uuid4().hex}@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert activities_response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request():
    # Arrange
    activity_name = "Chess Club"
    email = f"{uuid4().hex}@example.com"

    # Act
    first_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    duplicate_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup_response.status_code == 200
    assert duplicate_signup_response.status_code == 400
    assert duplicate_signup_response.json()["detail"] == "Student already signed up for this activity"
