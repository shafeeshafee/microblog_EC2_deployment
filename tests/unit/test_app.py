import pytest
from app import create_app
from config import Config

# test config using in-memory sqlite db and disabling elasticsearch
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None

# fixture to provide a flask test client
@pytest.fixture
def client():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    
    yield app.test_client()  # provide the test client
    
    app_context.pop()  # clean up after tests

# test to see if home page redirects to login
def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

# test if login page loads successfully
def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
