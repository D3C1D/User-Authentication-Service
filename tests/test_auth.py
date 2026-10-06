from fastapi.testclient import (
    TestClient
)

from app.main import app


client = TestClient(
    app
)


def test_root():

    response = client.get(
        "/"
    )

    assert response.status_code == 200

    assert response.json() == {
        "message":
            "User Authentication Service"
    }


def test_register_user():

    response = client.post(
        "/register",
        json={
            "username":
                "testuser",
            "email":
                "test@example.com",
            "password":
                "Password123"
        }
    )

    assert response.status_code == 200


def test_login_user():

    response = client.post(
        "/login",
        json={
            "email":
                "test@example.com",
            "password":
                "Password123"
        }
    )

    assert response.status_code == 200