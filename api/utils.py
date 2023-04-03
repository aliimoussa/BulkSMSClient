import smpplib.client
import smpplib.consts
import smpplib.gsm
from flask import make_response
from smpplib.exceptions import PDUError


def get_client(credentials):
    client = smpplib.client.Client(str(credentials.get('host')), credentials.get('port'))
    # Print when obtain message_id
    client.set_message_sent_handler(
        lambda pdu: print(f'sent: {pdu.sequence} {pdu.message_id}\n'))
    client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
    client.connect()

    # Bind to the SMPP server
    client.bind_transceiver(
        system_id=str(credentials.get('system_id')),
        password=str(credentials.get('password')),
        system_type='smpplib'
    )

    return client


def handle_sms(client, messages):
    try:
        for msg in messages:
            dest_number = msg.get('dst_number')
            source_number = msg.get('source_number')
            content = msg.get('content')
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(f'u\'{content}')
            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                    source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
                    # Make sure it is a byte string, not unicode:
                    source_addr=str(source_number),
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure these two params are byte strings, not unicode:
                    destination_addr=str(dest_number),
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )
                print(pdu.sequence)

    except PDUError as e:
        print(f'Error sending message: {str(e)}')
    client.listen()

    # Unbind and Disconnect from the SMPP server
    client.unbind()
    client.disconnect()
    # return make_response("SMS messages sent successfully.")


# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
    print(f'delivered: {pdu.sequence} {pdu.receipted_message_id}\n')
    return 0
