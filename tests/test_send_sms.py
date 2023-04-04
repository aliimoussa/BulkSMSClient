import unittest
from unittest.mock import patch
from api.route import send_sms
from flask import Flask

app = Flask(__name__)


def test_send_multiple_sms_messages(client):
    data = {
        "credentials": {
            "host": "smscsim.smpp.org",
            "port": " 2775",
            "system_id": "9qCBIdSB",
            "password": "9qCBIdSB"
        }
        , 'messages': [
            {'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message 1'},
            {'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message 2'},
            {'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message 4'},
            {'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message 5'},
        ]}
    response = client.post('/api/send-sms', json=data)
    print(response)
    assert response.status_code, 200


def test_send_single_sms_message(client):
    data = {
        "credentials": {
            "host": "smscsim.smpp.org",
            "port": " 2775",
            "system_id": "9qCBIdSB",
            "password": "9qCBIdSB"
        },
        'messages': [{'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message'}]}
    response = client.post('/send-sms', json=data)
    assert response.status_code, 200


def test_send_empty_message_data(client):
    data = {}
    response = client.post('/send-sms', json=data)
    assert response.status_code, 400


def test_send_missing_message_data(client):
    data = {'nodata': 'missing'}
    response = client.post('/send-sms', json=data)
    assert response.status_code, 400


def test_send_invalid_message_data(client):
    data = {
        "credentials": {
            "host": "smscsim.smpp.org",
            "port": " 2775",
            "system_id": "9qCBIdSB",
            "password": "9qCBIdSB"
        }, 'messages': [
            {'xyz': 'xyz'},
            {'dst_number': '1234567890', 'source_number': '0987654321', 'content': 'Test message'}
        ]}
    response = client.post('/send-sms', json=data)
    assert response.status_code, 200
