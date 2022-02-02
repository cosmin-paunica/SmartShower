import pytest
import json
from app import create_app

@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Welcome to SmartShower!' in html
    assert landing.status_code == 200

# Test Users
def test_get_users(client):
    landing = client.get("/users")
    assert landing.status_code == 200

def test_add_user(client):
    payload = {'name': 'unit_test_name', 'password' : 'parola', 'height': '180', 'hair_length' : 'long'}
    res = client.post('/users', data=json.dumps(payload), follow_redirects=True)
    assert res.status_code == 200

    payload = {'height': '180', 'hair_length' : 'long'}
    res = client.post('/users', data=json.dumps(payload), follow_redirects=True)
    res_data = json.loads(res.data.decode())
    assert res_data["message"] == 'Fields must be nonempty!'

def test_get_single_user(client):
    landing = client.get("/users/unit_test_name")
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["name"] == "unit_test_name"
    assert res["height"] == 180.0
    assert res["hair_length"] == "long"

def test_modify_user(client):
    payload = {'new_name': 'updated_unit_test_name', 'new_height': '190', 'new_hair_length' : 'short'}
    landing = client.put("/users/unit_test_name", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == 'User updated!'

def test_delete_user(client):
    landing = client.delete("/users/updated_unit_test_name")
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == 'Successfully deleted!'


# Test Water
def test_get_water_params(client):
    landing = client.get("/water/temperature")
    assert landing.status_code == 200

def test_set_water_params(client):
    payload = {'temperature': '40.5', 'preparation_date' : '01/27/22'}
    landing = client.put("/water/temperature", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == 'Watter parameters added successfully!'

def test_add_consumption(client):
    payload = {'consumption': '40.8'}
    landing = client.post("/water/consumption", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Water consumption inserted successfully!"


# Test Shower
def test_start_shower(client):
    payload = {'name': 'Default user'}
    landing = client.get("/start", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Shower started successfully!"

def test_end_shower(client):
    payload = {'consumption': '40.8'}
    landing = client.post("/end", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Shower ended successfully!"


# Test Dispenser
def test_get_fill_value(client):
    landing = client.get("/dispenser")
    assert landing.status_code == 200

def test_use_dispenser(client):
    payload = {'name': 'Default user'}
    landing = client.put("/dispenser", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Dispenser successfully used!"

def test_fill_dispenser(client):
    landing = client.post("/dispenser")
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Dispenser successfully filled!"


# Test Quality
def test_get_quality_info(client):
    landing = client.get("/quality")
    assert landing.status_code == 200

def test_set_quality_info(client):
    landing = client.post("/quality")
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "Quality inserted successfully!"