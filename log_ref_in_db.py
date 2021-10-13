import psycopg2
import os
import binascii


def save_ref(event_id, recipient_email, recipient_name):

    con = psycopg2.connect(database=os.environ.get('DEV_POSTGRES_DATABASE') if os.environ.get('DB_MODE') == 'development' else os.environ.get('POSTGRES_DATABASE'),
                           user=os.environ.get('DEV_POSTGRES_USER') if os.environ.get('DB_MODE') == 'development' else os.environ.get('POSTGRES_USER'),
                           password=os.environ.get('DEV_POSTGRES_PASSWORD') if os.environ.get('DB_MODE') == 'development' else os.environ.get('POSTGRES_PASSWORD'),
                           host=os.environ.get('DEV_POSTGRES_HOST') if os.environ.get('DB_MODE') == 'development' else os.environ.get('POSTGRES_HOST'),
                           port=os.environ.get('DEV_POSTGRES_PORT') if os.environ.get('DB_MODE') == 'development' else os.environ.get('POSTGRES_PORT'))
    cur = con.cursor()
    cert_ref_id = str(binascii.b2a_hex(os.urandom(16)), 'UTF-8')
    cur.execute(
        '''INSERT INTO certs ("id", "eventId", "recipientEmail", "recipientName") VALUES (%(cert_ref_id)s, %(event_id)s, %(recipient_email)s, %(recipient_name)s);''',
        {
            'cert_ref_id': cert_ref_id,
            'event_id': event_id,
            'recipient_email': recipient_email,
            'recipient_name': recipient_name
        }
    )

    con.commit()
    con.close()
    return cert_ref_id
