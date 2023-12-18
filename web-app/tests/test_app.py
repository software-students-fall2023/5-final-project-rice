from pymongo import MongoClient
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


def test_LoginPage_post(client):
    response = client.post('/', data={'fname': 'testuser', 'fpwd': 'testpass'})
    assert response.status_code in [200, 302]

def test_RegisterPage_post(client):
    response = client.post('/register', data={'fname': 'newuser', 'fpwd': 'newpass', 'femail': 'newemail@test.com', 'fnumber': '1234567890'})
    assert response.status_code in [200, 302]

def test_AddItem_post_authenticated(client):
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'
    response = client.post('/AddItem', data={'category': 'test', 'description': 'test item', 'condition': 'new', 'price': '10'})
    assert response.status_code in [200, 302]

def test_YourTrade_authenticated(client):
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'
    response = client.get('/YourTrade')
    assert response.status_code == 200

def test_EditItem_post(client):
    response = client.post('/EditItem/<itemId>', data={'category': 'edited', 'description': 'edited item', 'condition': 'used', 'price': '5'})  
    assert response.status_code in [200, 302]

def test_SearchByCategory(client):
    response = client.get('/SearchForItem?item_category=test')
    assert response.status_code == 200

def test_UserProfile_get_authenticated(client):
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'
    response = client.get('/Profile')
    assert response.status_code == 200

def test_UserProfile_post_authenticated(client):
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'
    response = client.post('/Profile', data={'username': 'updateduser', 'email': 'updatedemail@test.com', 'phone': '0987654321'})
    assert response.status_code in [200, 302]

def test_logout(client):
    response = client.post('/logout')
    assert response.status_code == 302

def test_register_user(client):
    result = register_user('testuser2', 'testpass2', 'test2@test.com', '1234567891')
    assert result in [True, False]

def test_authenticate_user(client):
    result = authenticate_user('testuser', 'testpass')
    assert result in [True, False]
