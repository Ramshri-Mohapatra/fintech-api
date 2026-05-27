import pytest 
from fastapi.testclient import TestClient
from app.main import app


def test_register_user(client):
    response = client.post("/register", json={"email": "test@test.com","password": "password567"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "password" not in data

def test_register_duplicate_email(client):

    client.post("/register", json={"email": "duplicate@test.com", "password": "password123"
    })
    
    # Second registration with same email - this should fail
    response = client.post("/register", json={"email": "duplicate@test.com","password": "password123"
    })

    assert response.status_code == 400 #bad requesst invalid inpiut from client
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client):

    client.post("/register", json={
        "email":"logintest@test.com" , "password" : "password567"})
    
    response = client.post("/login", data={
        "username": "logintest@test.com",
        "password": "password567"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
   
    client.post("/register", json={
        "email": "wrongpass@test.com",
        "password": "password123"
    })
    
    # Try to login with wrong password
    response = client.post("/login", data={
        "username": "wrongpass@test.com",
        "password": "wrongpassword"  # deliberately wrong
    })
    
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    
    response = client.post("/login", data={
        "username": "nobody@test.com",
        "password": "password123"
    })
    
    
    assert response.status_code == 401