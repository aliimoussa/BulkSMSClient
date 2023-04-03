import logging
from typing import Union, Tuple

from flask import Blueprint
from flask import request, jsonify

from api.utils import get_client, handle_sms
from api.validators import validate_credentials, validate_send_sms

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def hello():
    return 'hello worldg'


@api_bp.route('/send-sms', methods=['POST'])
def send_sms() -> Union[jsonify, Tuple[str, int]]:
    data = request.get_json()
    credentials = data.get('credentials', {})
    valid_messages, errors = validate_send_sms(data)

    credential_errors = validate_credentials(credentials)
    if credential_errors:
        for error in credential_errors:
            logger.error(error)
        return jsonify(credential_errors), 400
    if valid_messages:
        if errors:
            for error in errors:
                logger.error(error)
        with get_client(credentials) as client:
            handle_sms(client, valid_messages)
    else:
        logger.error("Could not get client instance")
        return "Could not get client instance", 500
    return "SMS sent successfully", 200
