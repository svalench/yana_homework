import json
import os

import pytest
import requests

from constants import URL, PAYLOAD

session = requests.Session()
session.headers.update({"accept": "application/json", "Content-Type": "application/json"})



@pytest.mark.parametrize("method,url,payload,status", [
    ('get', f"{URL}store/inventory",{},200),
    ])
def test_get_store_inventory(method, url, payload, status):
    response = session.request(method=method, url=url, json=payload)
    assert response.status_code == status


@pytest.mark.parametrize("url_post,payload,status_post,url_get,status_get", [
    (f"{URL}pet", PAYLOAD, 200, f"{URL}pet/%s", 200),
    ])
def test_add_pet(url_post, payload, status_post, url_get,status_get):
    post_response = session.request(method='POST', url=url_post, json=payload)
    assert post_response.status_code == status_post
    response_data = post_response.json()
    url_get = url_get % post_response.json()["id"]
    get_response = session.request(method='GET', url=url_get)
    assert get_response.status_code == status_get
    open('file.txt', 'wb')
    files = {'file': ('file.txt', open('file.txt', 'rb'),'multipart/form-data')}
    post_response_add_img = requests.post( f'{URL}pet/%s/uploadImage' % response_data["id"], files=files)
    assert post_response_add_img.status_code == 200
    delete_response = session.request(method='DELETE', url=url_get)
    os.remove('file.txt')


@pytest.mark.parametrize("url_post,payload,status_post,url_get,statu_delete,status_get", [
    (f"{URL}pet", PAYLOAD, 200, f"{URL}pet/%s", 200, 404),
    ])
def test_delete(url_post, payload, status_post, url_get, statu_delete, status_get):
    post_response = session.request(method='POST', url=url_post, json=payload)
    assert post_response.status_code == status_post
    url_get = url_get % post_response.json()["id"]
    delete_response = session.request(method='DELETE', url=url_get)
    assert delete_response.status_code == statu_delete
    get_response = session.request(method='GET', url=url_get)
    assert get_response.status_code == status_get


@pytest.mark.parametrize("url_post,payload,status_post,url_get,statu_put,status_get,name", [
    (f"{URL}pet", PAYLOAD, 200, f"{URL}pet/%s", 200, 200,'test'),
    ])
def test_update_pet(url_post, payload, status_post, url_get, statu_put, status_get,name):
    post_response = session.request(method='POST', url=url_post, json=payload)
    assert post_response.status_code == status_post
    response_data = post_response.json()
    response_data['name'] = name
    put_response = session.request(method='PUT', url= f"{URL}pet", json=response_data)
    assert put_response.status_code == statu_put
    get_response = session.request(method='GET', url=url_get % response_data["id"])
    assert get_response.status_code == status_get
    assert get_response.json()['name'] == name


@pytest.mark.parametrize("url,status,exists", [
    (f"{URL}pet/findByStatus", "available", True),
    (f"{URL}pet/findByStatus", "errorstatus", False),
    ])
def test_params(url, status, exists):
    get_response = requests.get(
        url=url,
        params={"status": status},
        headers={"accept": "application/json"}
    )
    data = get_response.json()
    assert bool(len(data)) == exists
    assert get_response.status_code == 200