from pymongo import MongoClient
import pytest
import mongomock
from unittest.mock import patch
from flask import Flask
from bson.objectid import ObjectId
from app import app, register_user, authenticate_user, logout


app_client = app.test_client()


@pytest.fixture
def client():
    """
    Fixture to configure the app for testing and provide a test client.
    """
    app.config["TESTING"] = True
    mock_mongo_client = mongomock.MongoClient()
    with patch('app.mongo_client', mock_mongo_client):
        with app.test_client() as test_client:
            yield test_client
    #with app.test_client() as test_client:
        #yield test_client

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

@pytest.fixture
def insert_test_item():
    mongo_client = mongomock.MongoClient()
    db = mongo_client["trade_database"]
    items_collection = db['items']

    test_item = {
        "category": "Test",
        "description": "Test Description",
        "condition": "New",
        "price": "100"
    }
    inserted_item = items_collection.insert_one(test_item)
    item_id = inserted_item.inserted_id

    yield str(item_id)  
    items_collection.delete_one({"_id": ObjectId(item_id)})

def test_EditItem_get(client, insert_test_item):
    item_id = insert_test_item  
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'

    response = client.get(f'/EditItem/{item_id}')
    assert response.status_code == 200
   

def test_EditItem_post(client, insert_test_item):
    item_id = insert_test_item  

    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'

    updated_item_data = {
        'category': 'Updated Category',
        'description': 'Updated Description',
        'condition': 'Updated Condition',
        'price': 'Updated Price',
    }
    response = client.post(f'/EditItem/{item_id}', data=updated_item_data)
    assert response.status_code in [200, 302]


def test_DeleteItem(client, insert_test_item):
    item_id = insert_test_item

    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'

    response = client.post(f'/DeleteItem/{item_id}')
    assert response.status_code == 302

    mongo_client = mongomock.MongoClient()
    db = mongo_client["trade_database"]
    items_collection = db['items']
    deleted_item = items_collection.find_one({"_id": ObjectId(item_id)})
    
    assert deleted_item is None


def test_YourItemDetail(client, insert_test_item):
    item_id = insert_test_item

    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'

    response = client.get(f'/YourItemDetail/{item_id}')
    assert response.status_code == 200


def test_invalid_item(client):
    invalid_item_id = str(ObjectId())
    response = client.get(f'/ViewItemDetail/{invalid_item_id}')
    assert response.status_code == 200


def test_add_no_login():
    response = app_client.post('/AddItem', data={'category': 'Electronics', 'description': 'Brand new smartphone', 'condition': 'New', 'price': '500'})
    assert response.status_code == 302 


def test_image_retrieval(insert_test_item):
    item_id_to_retrieve_image = insert_test_item
    response = app_client.get(f'/images/{item_id_to_retrieve_image}')
    assert response.status_code == 404

def test_image_upload():
    with app_client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['username'] = 'testuser'
    image_file = open('test_image_file/test_image.jpg', 'rb') 
    response = app_client.post('/AddItem', data={'category': 'Electronics', 'description': 'Smartphone', 'condition': 'New', 'price': '500', 'item_image': (image_file, 'test_image.jpg')})
    assert response.status_code in [200, 302] 