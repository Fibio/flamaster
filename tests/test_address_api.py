from flask.helpers import json
from flamaster.app import db, app
from flamaster.account.models import Address

from conftest import url_client, login, logout, create_user


first_address = {'city': u'Kharkov',
                 'street': u'23b, Sumskaya av.',
                 'apartment': u'1',
                 'zip_code': u'626262',
                 'type': 'billing'}

dafault_address = {'user_id': 1,
                   'city': u'Test_city',
                   'street': u'Test_street',
                   'apartment': u'12',
                   'zip_code': u'121212',
                   'type': 'billing'}


def setup_module(module):
    db.create_all()
    with app.test_request_context('/'):
        create_user()


def teardown_module(module):
    db.session.remove()
    db.drop_all()

@url_client('account.addresses')
def test_address_creation_failed_unauth(url, client):
    data = first_address.copy()
    resp = client.post(url, data=json.dumps(data),
                       content_type='application/json')

    assert resp.status_code == 401


@url_client('account.addresses')
def test_address_creation_failed_no_data(url, client):
    data = first_address.copy()
    del data['type'], data['city'], data['street']
    uid = json.loads(login(client).data)['uid']
    resp = client.post(url, data=json.dumps(data),
                       content_type='application/json')

    assert 'type' in json.loads(resp.data)
    assert 'city' in json.loads(resp.data)
    assert 'street' in json.loads(resp.data)
    assert resp.status_code == 400

    logout(client, uid)


@url_client('account.addresses')
def test_addresses_get_failed(url, client):
    resp = client.get(url, content_type='application/json')
    assert resp.status_code == 401


@url_client('account.addresses')
def test_addresses_get_success(url, client):
    uid = json.loads(login(client).data)['uid']
    resp = client.get(url, content_type='application/json')

    assert json.loads(resp.data) == {}
    assert resp.status_code == 200
    logout(client, uid)


@url_client('account.addresses', id=1)
def test_addresses_put_403(url, client):
    Address.create(**dafault_address)
    resp = client.put(url, content_type='application/json')
    assert resp.status_code == 403


@url_client('account.addresses', id=1)
def test_addresses_put_400(url, client):
    uid = json.loads(login(client).data)['uid']
    resp = client.put(url, content_type='application/json')

    assert resp.status_code == 400
    logout(client, uid)


@url_client('account.addresses', id=1)
def test_addresses_put_not_valid_data(url, client):
    uid = json.loads(login(client).data)['uid']
    address_data = first_address.copy()
    del address_data['city']
    resp = client.put(url, data=json.dumps(address_data),
                      content_type='application/json')
    assert resp.status_code == 404
    logout(client, uid)


@url_client('account.addresses', id=1)
def test_addresses_put_201(url, client):
    uid = json.loads(login(client).data)['uid']
    resp = client.put(url, data=json.dumps(first_address),
                      content_type='application/json')

    response_data = json.loads(resp.data)
    assert 'id' in response_data
    assert response_data['city'] == first_address['city']
    assert resp.status_code == 201
    logout(client, uid)


@url_client('account.addresses', id=1)
def test_addresses_delete_404(url, client):
    resp = client.delete(url, content_type='application/json')
    assert resp.status_code == 404


@url_client('account.addresses', id=1)
def test_addresses_delete_400(url, client):
    uid = json.loads(login(client).data)['uid']
    resp = client.delete(url, content_type='application/json')

    assert resp.status_code == 200
    logout(client, uid)
