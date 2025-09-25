import pytest
from app import create_app, db
from app.models import Task

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Test task'})
    assert response.status_code == 201
    assert response.json['title'] == 'Test task'

def test_get_tasks(client):
    client.post('/tasks', json={'title': 'Task 1'})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json['tasks']) == 1
