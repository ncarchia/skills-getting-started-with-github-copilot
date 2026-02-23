import pytest


def test_get_activities(client):
    # Arrange – nothing special, client fixture ready
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_nonexistent_activity(client):
    # Act
    response = client.post(
        "/activities/Nonexistent/signup", params={"email": "foo@bar"}
    )

    # Assert
    assert response.status_code == 404


def test_signup_already_registered(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up

    # Act
    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 400


def test_remove_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_signup_not_registered(client):
    # Act
    response = client.delete(
        "/activities/Chess Club/signup", params={"email": "not@here"}
    )

    # Assert
    assert response.status_code == 400


def test_remove_signup_nonexistent_activity(client):
    # Act
    response = client.delete(
        "/activities/No/signup", params={"email": "a@b"}
    )

    # Assert
    assert response.status_code == 404
