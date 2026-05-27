import pytest
from fastapi.testclient import TestClient
from app.main import app



def get_auth_token(client,email: str, password: str) -> str:
    # Helper function to register and login a user and return their token
    # We use this in multiple tests so it makes sense to extract it
    client.post("/register", json={
        "email": email,
        "password": password
    })
    response = client.post("/login", data={
        "username": email,
        "password": password
    })
    return response.json()["access_token"]


def test_create_transaction_success(client):
    # Test that an authenticated user can create a transaction
    token = get_auth_token(client,"trans1@test.com", "password123")
    
    # We pass the token in the Authorization header as Bearer
    # This is how every real API client sends JWT tokens
    response = client.post("/transactions",
        json={
            "amount": 50.00,
            "category": "food",
            "description": "Lunch",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.00
    assert data["category"] == "food"
    assert data["type"] == "expense"
    assert "id" in data
    assert "user_id" in data


def test_create_transaction_no_token(client):
    # Test that creating a transaction without a token returns 401
    # This is the authorization test - no token means no access
    response = client.post("/transactions",
        json={
            "amount": 50.00,
            "category": "food",
            "description": "Lunch",
            "type": "expense"
        }
        # Notice no headers - no token sent
    )
    
    # Should be rejected with 401 Unauthorized
    assert response.status_code == 401


def test_create_transaction_invalid_token(client):
    # Test that a fake or tampered token is rejected
    response = client.post("/transactions",
        json={
            "amount": 50.00,
            "category": "food",
            "type": "expense"
        },
        # This is a completely fake token - signature will not match
        headers={"Authorization": "Bearer faketoken123"}
    )
    
    assert response.status_code == 401


def test_get_transactions_success(client):
    # Test that a user can retrieve their own transactions
    token = get_auth_token(client, "trans2@test.com", "password123")
    
    # Create a transaction first
    client.post("/transactions",
        json={"amount": 100.00, "category": "salary", "type": "income"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Now retrieve all transactions
    response = client.get("/transactions",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)   # response should be a list
    assert len(data) >= 1           # at least one transaction exists


def test_user_cannot_see_other_users_transactions(client):
    # This is a critical security test
    # User A creates a transaction
    # User B should not be able to see it
    
    token_a = get_auth_token(client, "usera@test.com", "password123")
    token_b = get_auth_token(client, "userb@test.com", "password123")
    
    # User A creates a transaction
    client.post("/transactions",
        json={"amount": 999.00, "category": "secret", "type": "income"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    
    # User B retrieves their transactions
    response = client.get("/transactions",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # User B should see zero transactions
    # User A's transaction should not appear
    categories = [t["category"] for t in data]
    assert "secret" not in categories


def test_delete_transaction_success(client):
    # Test that a user can delete their own transaction
    token = get_auth_token(client, "trans3@test.com", "password123")
    
    # Create a transaction
    create_response = client.post("/transactions",
        json={"amount": 25.00, "category": "coffee", "type": "expense"},
        headers={"Authorization": f"Bearer {token}"}
    )
    transaction_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 204 No Content means successful deletion
    assert response.status_code == 204


def test_delete_other_users_transaction(client):
    # Test that a user cannot delete another user's transaction
    token_a = get_auth_token(client, "deluser_a@test.com", "password123")
    token_b = get_auth_token(client, "deluser_b@test.com", "password123")
    
    # User A creates a transaction
    create_response = client.post("/transactions",
        json={"amount": 75.00, "category": "gym", "type": "expense"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    transaction_id = create_response.json()["id"]
    
    # User B tries to delete User A's transaction
    response = client.delete(f"/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    
    # Should return 404 - we don't even confirm the transaction exists
    # to avoid leaking information
    assert response.status_code == 404