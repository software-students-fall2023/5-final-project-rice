import pytest
from flask import Flask
from app import app, register_user, authenticate_user, logout


app_client = app.test_client()


@pytest.fixture
def client():
    """
    Fixture to configure the app for testing and provide a test client.
    """
    app.config["TESTING"] = True
    
    with app.test_client() as test_client:
        yield test_client

def test_LoginPage_render(client):
    response = client.get('/')
    assert response.status_code == 200

def test_RegisterPage_render(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_RootPage_render(client):
    response = client.get('/Trade')
    assert response.status_code == 200

def test_AddItemPage_render(client):
    response = client.get('/AddItem')
    assert response.status_code == 200

def test_ViewAllTrade_render(client):
    response = client.get('/ViewAllTrade')
    assert response.status_code == 200



def test_YourTrade_unathenticated(client):
    response = client.get('/YourTrade')
    assert response.status_code == 302

def test_SearchForItem_render(client):
    response = client.get('/SearchForItem')
    assert response.status_code == 200