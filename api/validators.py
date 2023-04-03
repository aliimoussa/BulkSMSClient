def validate_credentials(credentials):
    errors = []
    if not credentials:
        errors.append('Credentials are missing')
    elif not isinstance(credentials, dict):
        errors.append('Invalid credentials')

    for key in ['host', 'port', 'system_id', 'password']:
        if key not in credentials:
            errors.append(f'{key} is missing in credentials')
            continue
        value = credentials[key]
        if not value or not isinstance(value, str):
            errors.append(f'Invalid {key} in credentials')

    return errors


def validate_send_sms(data):
    errors = []
    valid_messages = []
    messages = data.get('messages', [])

    for msg in messages:
        dest_number = msg.get('dst_number')
        source_number = msg.get('source_number')
        content = msg.get('content')
        if not dest_number:
            errors.append({'message': msg, 'error': 'Destination number is missing'})
        elif not isinstance(dest_number, str) or len(dest_number) > 15:
            errors.append({'message': msg, 'error': 'Invalid destination number'})

        if not source_number:
            errors.append({'message': msg, 'error': 'Source number is missing'})
        elif not isinstance(source_number, str) or len(source_number) > 15:
            errors.append({'message': msg, 'error': 'Invalid source number'})

        if not content:
            errors.append({'message': msg, 'error': 'Content is missing'})
        elif not isinstance(content, str) or len(content) > 140:
            errors.append({'message': msg, 'error': 'Invalid content'})

        if dest_number == source_number:
            errors.append({'message': msg, 'error': 'Destination number and source number can not be the same'})
        else:
            valid_messages.append(msg)

    for msg_error in errors:
        valid_messages = [msg for msg in valid_messages if msg != msg_error['message']]

    return valid_messages, errors
