import requests

from jsonschema import validate

from schemas.create_user import create_user
from schemas.get_single_user import get_single_user
from schemas.update_user import update_user
from schemas.unsuccessful_register import unsuccessful_register
from schemas.successful_register import successful_register

url = 'https://reqres.in'


def test_get_single_user():
    endpoint = '/api/users/'
    id = 2

    headers = {
        'x-api-key': 'reqres-free-v1'
    }
    response = requests.get(url + endpoint + str(id), headers=headers)
    body = response.json()

    assert response.status_code == 200
    validate(body, get_single_user)
    assert body['data']['id'] == id
    assert body['data']['email'] == 'janet.weaver@reqres.in'
    assert body['data']['first_name'] == 'Janet'
    assert body['data']['last_name'] == 'Weaver'

def test_get_list_users():
    endpoint = '/api/users'

    params = {
        "page": 2
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.get(url + endpoint, params=params, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body['page'] == params['page']

def test_create_user():
    endpoint = '/api/users'

    payload = {
        "name": "morpheus",
        "job": "teacher"
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.post(url + endpoint, data=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    validate(body, create_user)
    assert body['name'] == 'morpheus'
    assert body['job'] == 'teacher'

def test_successful_register():
    endpoint = '/api/register'

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.post(url + endpoint, json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    validate(body, successful_register)

def test_unsuccessful_register():
    endpoint = '/api/register'

    payload = {
        "email": "eve.holt@reqres.in",
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.post(url + endpoint, json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 400
    validate(body, unsuccessful_register)

def test_delete_user():
    endpoint = '/api/users/'
    id = 2
    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.delete(url + endpoint + str(id),  headers=headers)

    assert response.status_code == 204

def test_update_user():
    endpoint = '/api/users/'
    id = 2

    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.put(url + endpoint + str(id), data=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    validate(body, update_user)
    assert body["name"] == "morpheus"
    assert body["job"] == "zion resident"

def test_single_user_not_found():
    endpoint = '/api/users/'
    id = 23

    headers = {
        'x-api-key': 'reqres-free-v1'
    }

    response = requests.get(url + endpoint + str(id), headers=headers)

    assert response.status_code == 404