from fastapi.testclient import TestClient
from main import app
client=TestClient(app)

def test_root_return_200():
    response=client.get('/')
    assert response.status_code==200
def test_root_return_app_name():
    response=client.get('/')
    assert 'app_name' in response.json()
