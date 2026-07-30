from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_chat_success() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "customer_id": "cus_001",
            "message": "Đơn hàng của tôi đang ở đâu?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == "cus_001"
    assert (
        data["reply"]
        == "Tôi đã nhận được câu hỏi: Đơn hàng của tôi đang ở đâu?"
    )


def test_create_chat_with_empty_message() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "customer_id": "cus_001",
            "message": "     ",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Message cannot be empty"
    }


def test_create_chat_without_customer_id() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Kiểm tra đơn hàng giúp tôi",
        },
    )

    assert response.status_code == 422