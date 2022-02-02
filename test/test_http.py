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
    payload = {'name': 'Default user', 'song_id': '11dFghVXANMlKmJXsNCbNl'}
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

# Test Authentication
def test_register_succesfull(client):
    payload = {'name':'TestName','password':'TestPassword','height':'190','hair_length':'long'}
    landing = client.post('/auth/register', data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "user registered succesfully"

def test_register_already_registered(client):
    payload = {
        'name':'TestName',
        'password':'TestPassword',
        'height':'190',
        'hair_length':'60'
    }
    landing = client.post("/auth/register", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "User TestName is already registered."

def test_register_failed_no_name(client):
    payload = {
        'password':'TestPassword',
        'height':'190',
        'hair_length':'60'
    }
    landing = client.post("/auth/register", data=json.dumps(payload), follow_redirects=True)
    # res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    # assert res["message"] == "Name is required."

def test_register_failed_no_password(client):
    payload = {
        'name':'TestName',
        'height':'190',
        'hair_length':'60'
    }
    landing = client.post("/auth/register", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "Password is required."

def test_register_failed_no_height(client):
    payload = {
        'name':'TestName',
        'password':'TestPassword',
        'hair_length':'60'
    }
    landing = client.post("/auth/register", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "Height is required."

def test_register_failed_no_hair_length(client):
    payload = {
        'name':'TestName',
        'password':'TestPassword',
        'height':'190',
    }
    landing = client.post("/auth/register", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "Hair Length is required."

def test_login_user_not_found(client):
    payload = {
        'name': 'NotExistingUser',
        'password':'NotExistingPassword'
    }
    landing = client.post("/auth/login", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "user not found"

def test_login_user_wrong_password(client):
    payload = {
        'name': 'TestName',
        'password':'NotExistingPassword'
    }
    landing = client.post("/auth/login", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 403
    assert res["message"] == "password is incorrect"

def test_login_succesful(client):
    payload = {
        'name': 'TestName',
        'password':'TestPassword'
    }
    landing = client.post("/auth/login", data=json.dumps(payload), follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["message"] == "user logged in succesfully"

# Test Spotify API
def test_spotify_get_not_existing_id(client):
    not_existing_id = '123456789436364215'
    landing = client.get(f'/song/{not_existing_id}', follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["error"]["message"] == "invalid id"

def test_spotify_get_succesfull(client):
    existing_id = '11dFghVXANMlKmJXsNCbNl'
    landing = client.get(f'/song/{existing_id}', follow_redirects=True)
    res = json.loads(landing.data.decode())
    assert landing.status_code == 200
    assert res["id"] == existing_id
