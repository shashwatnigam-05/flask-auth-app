"""Tests for the Flask Authentication Application."""
import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key-for-testing-only'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_index_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_signup_page_loads(client):
    response = client.get('/signup')
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_signup_creates_user(client):
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@example.com'


def test_signup_rejects_short_password(client):
    response = client.post('/signup', data={
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'short'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='testuser2').first()
        assert user is None


def test_signup_rejects_duplicate_username(client):
    client.post('/signup', data={
        'username': 'dupuser',
        'email': 'first@example.com',
        'password': 'password123'
    })
    response = client.post('/signup', data={
        'username': 'dupuser',
        'email': 'second@example.com',
        'password': 'password456'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert User.query.filter_by(username='dupuser').count() == 1


def test_login_valid_credentials(client):
    client.post('/signup', data={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'mypassword123'
    })
    response = client.post('/login', data={
        'email': 'login@example.com',
        'password': 'mypassword123'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/dashboard' in response.headers['Location']


def test_login_invalid_credentials(client):
    response = client.post('/login', data={
        'email': 'nobody@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_open_redirect_blocked(client):
    """The login next parameter must not allow external redirects."""
    response = client.post('/login?next=http://evil.com', data={
        'email': 'nobody@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=False)
    # Should stay on login, not redirect to evil.com
    if response.status_code == 302:
        assert 'evil.com' not in response.headers.get('Location', '')


def test_password_not_stored_in_plaintext(client):
    client.post('/signup', data={
        'username': 'hashcheck',
        'email': 'hash@example.com',
        'password': 'mypassword123'
    })
    with app.app_context():
        user = User.query.filter_by(username='hashcheck').first()
        assert user.password_hash != 'mypassword123'
        assert len(user.password_hash) > 20
