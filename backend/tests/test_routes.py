#from flask import Flask
#from backend.resources.routes import init_routes
import re
import requests as r
from random import randint as rand
import json

#app = Flask(__name__)
#init_routes( app )
base_url = 'http://127.0.0.1:5000'

headers = {'Content-type': 'application/json'}
open('log.log','w').close()



def log(response):
    log_text( str(response) )
    log_text( str(response.status_code) )
    log_text( str(response.text) )

def log_text( s: str ):
    with open('log.log','a') as f:
        f.write( s )

def super_admin_authorized_header():
    url = base_url + '/login'
    data = {'username':'user','password':'user'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    access_token = response.json()['access_token']
    auth_head = headers.copy()
    auth_head['Authorization'] = 'Bearer ' + str( access_token )

    return auth_head

def super_admin_authorized_header_without_json():
    url = base_url + '/login'
    data = {'username':'user','password':'user'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    access_token = response.json()['access_token']
    auth_head = {}
    auth_head['Authorization'] = 'Bearer ' + str( access_token )

    return auth_head


def admin_authorized_header():
    url = base_url + '/login'
    data = {'username':'admin','password':'admin'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    access_token = response.json()['access_token']
    auth_head = headers.copy()
    auth_head['Authorization'] = 'Bearer ' + str( access_token )
    return auth_head

def wrong_authorized_header():
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjY4OTc3NiwianRpIjoiMWFhZWZjMWEtZmI3Mi00MjFjLWEzMmUtNGQ3YTI5OWU5MTA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNjY2Njg5Nzc2LCJleHAiOjE2NjY2OTMzNzZ9.8hdEo0FrkrGbeU7ThCUabCcdFDD5hzXRKWMwo82N0j7'
    auth_head = headers.copy()
    auth_head['Authorization'] = 'Bearer ' + str( access_token )
    return auth_head

def admin_authorized_header_without_json():
    url = base_url + '/login'
    data = {'username':'admin','password':'admin'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    access_token = response.json()['access_token']
    auth_head = {}
    auth_head['Authorization'] = 'Bearer ' + str( access_token )
    return auth_head



def create_new_admin():
    url = base_url + '/add_admin'
    data = {
        "admin_type": "admin",
        "username": "another_admin_" + str(rand(1000,9999)) ,
        "password": "another_admin_pass",
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == { "msg": "Admin added" }


def get_new_created_admin_id():
    create_new_admin()
    url = base_url + '/get_admins'
    response = r.get( url, headers=super_admin_authorized_header() )
    return response.json()[-1]['id']













def test_get_unknown_route():
    url = base_url + '/'
    response = r.get(url)
    assert response.status_code == 404

def test_login_with_wrong_http_method():
    url = base_url + '/login'
    response = r.get( url )

    assert response.status_code == 405



def test_login_with_empty_body():
    url = base_url + '/login'
    response = r.post( url )

    assert response.status_code == 400
    assert response.json() == {"msg":"Missing JSON in request"}



def test_login_without_username():
    url = base_url + '/login'

    data = {'password':'pass'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    assert response.status_code == 400
    assert response.json() == {"msg": "Missing username parameter"}


def test_login_without_password():
    url = base_url + '/login'

    data = {'username':'user'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    assert response.status_code == 400
    assert response.json() == {"msg": "Missing password parameter"}

def test_login_with_wrong_password():
    url = base_url + '/login'

    data = {'username':'admin','password':'_'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    assert response.status_code == 401
    assert response.json() == {"msg": "Bad username or password"}


def test_login():
    url = base_url + '/login'

    data = {'username':'admin','password':'admin'}
    response = r.post( url, data=json.dumps(data), headers=headers )

    assert response.status_code == 200



def test_logout_without_auth_header():
    url = base_url + '/logout'
    response = r.delete( url, headers=headers )

    assert response.status_code == 401
    assert response.json() == { "msg": "Missing Authorization Header" }


def test_logout_with_wrong_auth_header():
    url = base_url + '/logout'
    response = r.delete( url, headers=wrong_authorized_header() )

    assert response.status_code == 422
    assert response.json() == { "msg": "Signature verification failed" }

def test_logout():
    url = base_url + '/logout'
    response = r.delete( url, headers=admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == { "msg": "Refresh token successfully revoked" }


def test_add_admin_not_as_super_admin():
    url = base_url + '/add_admin'
    response = r.post( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }



def test_add_admin_not_as_super_admin_without_body():
    url = base_url + '/add_admin'
    response = r.post( url, headers=admin_authorized_header_without_json() )

    assert response.status_code == 400
    assert response.json() == { "msg": "Missing JSON in request" }

def test_add_admin_as_super_admin_without_body():
    url = base_url + '/add_admin'
    data = {}
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 400
    assert response.json() == { "msg": "Missing username parameter" }



def test_add_admin_as_super_admin_existing_admin():
    url = base_url + '/add_admin'
    data = {
        "admin_type": "admin",
        "username": "admin",
        "password": "admin",
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 409
    assert response.json() == { "msg": "Admin with this username already exists" }

def test_add_admin_as_super_admin():
    url = base_url + '/add_admin'
    data = {
        "admin_type": "admin",
        "username": "another_admin_" + str(rand(1000,9999)) ,
        "password": "another_admin_pass",
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == { "msg": "Admin added" }




def test_get_admins_not_as_super_admin():
    url = base_url + '/get_admins'
    response = r.get( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }


def test_get_admins_as_super_admin():
    url = base_url + '/get_admins'
    response = r.get( url, headers=super_admin_authorized_header() )

    assert response.status_code == 200



def test_change_admin_type_not_as_super_admin():
    url = base_url + '/change_admin_type' 
    response = r.post( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }


def test_change_admin_type_as_super_admin_without_body():
    url = base_url + '/change_admin_type' 
    response = r.post( url, headers=super_admin_authorized_header() )

    assert response.status_code == 400


def test_change_admin_type_as_super_admin_of_unknown_admin():
    url = base_url + '/change_admin_type' 
    data = {
        'admin_id':'9999',
        'admin_type':'admin'
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 404
    assert response.json() == {"msg": "Admin with this id does not exists" }



def test_change_admin_type_as_super_admin_of_unknown_type():
    url = base_url + '/change_admin_type' 
    data = {
        'admin_id':'1',
        'admin_type':'admin123'
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )


    assert response.status_code == 400
    assert response.json() == {"msg": "Admin type must be super_admin or admin" }


def test_change_admin_type_as_super_admin():
    url = base_url + '/change_admin_type' 
    data = {
        'admin_id':'1',
        'admin_type':'admin'
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == {"msg": "Admin type changed" }



def test_delete_admin_not_as_super_admin():
    url = base_url + '/delete_admin/3' 
    response = r.delete( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }


def test_delete_admin_as_super_admin_of_unknown_id():
    url = base_url + '/delete_admin/9999' 
    response = r.delete( url, headers=super_admin_authorized_header() )

    assert response.status_code == 404
    assert response.json() == { "msg": "Admin with this id does not exists" }


def test_delete_admin_as_super_admin():
    new_admin_id = get_new_created_admin_id()
    url = base_url + '/delete_admin/' + str(new_admin_id)
    response = r.delete( url, headers=super_admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == { "msg": "Admin deleted" }


def test_get_admin_id_not_as_super_admin():
    url = base_url + '/get_admin/1' 
    response = r.get( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }


def test_get_admin_id_as_super_admin_of_unknown_admin():
    url = base_url + '/get_admin/9999' 
    response = r.get( url, headers=super_admin_authorized_header() )

    assert response.status_code == 404
    assert response.json() == { "msg": "Admin not found" }


def test_get_admin_id_as_super_admin():
    new_admin_id = get_new_created_admin_id()
    url = base_url + '/get_admin/' + str(new_admin_id)
    response = r.get( url, headers=super_admin_authorized_header() )

    assert response.status_code == 200


def test_modify_admin_not_as_super_admin():
    url = base_url + '/modify_admin' 
    response = r.post( url, headers=admin_authorized_header() )

    assert response.status_code == 403
    assert response.json() == { "msg": "You are not supper admin(" }


def test_modify_admin_as_super_admin_with_empy_body():
    url = base_url + '/modify_admin' 
    response = r.post( url, headers=super_admin_authorized_header_without_json() )

    assert response.status_code == 400
    assert response.json() == { "msg": "Missing JSON in request" }

def test_modify_admin_as_super_admin_of_unknown_admin():
    url = base_url + '/modify_admin' 
    data = {
        'admin_id':9999,
        'username':'admin',
        'username':'admin'
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 404
    assert response.json() == { "msg": "Admin with this id does not exists" }


def test_modify_admin_as_super_admin():
    url = base_url + '/modify_admin' 
    data = {
        'admin_id':1,
        'username':'admin',
        'username':'admin'
    }
    response = r.post( url, data=json.dumps(data), headers=super_admin_authorized_header() )

    assert response.status_code == 200
    assert response.json() == { "msg": "Admin modified" }













