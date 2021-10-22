import os
import sys
from zipfile import ZipFile
from dotenv import load_dotenv
import pandas as pd
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def generate_plain_mail_content(recipient_name, certificate_title, event_name, issuing_organization):
    if certificate_title == "Certificate Of Participation":
        return '''\
        Greetings {}! ✨ \n\n
        {} deeply honours your hearty participation in {}.\n\n
        Please go through the certificate attached herewith. In case of any issues or queries please do feel free to mail us. \n\n
        Do try to participate in the valuable sessions organized by {} in the upcoming days.\n\n
        Thanking you.
        '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Certificate of Achievement":
        return '''\
               Greetings {}! ✨ \n\n
               {} deeply honours your hearty participation in {}. We are really glad to announce you as the winner of the competition.\n\n
               Congratulations!\n\n
               Please go through the certificate attached herewith.\n
               In case of any issues or queries please do feel free to mail us.
               Do try to participate in the valuable sessions organized by {} in the upcoming days. \n\n
               Thanking you.
               '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Volunteer Certificate":
        return '''\
                Greetings {}! ✨\n\n
                {} deeply honours your hearty volunteering in organising {}.\n\n
                Please go through the certificate attached herewith.\n
                In case of any issues or queries please do feel free to mail us. 
                Do try to coordinate with {} in the upcoming days! \n\n
                Thanking you.
                '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Coordinator Certificate":
        return '''
                Greetings {}! ✨<br /><br />
                {} deeply honours your hearty coordination in organising {}.<br /><br />
                Please go through the certificate attached herewith.
                In case of any issues or queries please do feel free to mail us. <br /><br />
                We expect the same in the upcoming events too!<br /><br />
                Thanking you.
                '''.format(recipient_name, issuing_organization, event_name)


def generate_html_mail_content(recipient_name, certificate_title, event_name, issuing_organization):
    if certificate_title == "Certificate Of Participation":
        return '''\
                <html>
                <body>
                <p>
                Greetings {}! ✨ <br /><br />
                {} deeply honours your hearty participation in <strong>{}</strong>.<br /><br />
                Please go through the certificate attached herewith.
                In case of any issues or queries please do feel free to mail us. <br /><br />
                Do try to participate in the valuable sessions organized by <strong>{}</strong> in the upcoming days.<br /><br />
                Thanking you.
                </p>
                </body>
                </html>
                '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Certificate of Achievement":
        return '''\
                <html>
                <body>
                <p>
                Greetings {}! ✨ <br /><br />
                {} deeply honours your hearty participation in <strong>{}</strong>. We are really glad to announce you as the winner of the competition.<br /><br />
                Congratulations!<br /><br />
                Please go through the certificate attached herewith.<br />
                In case of any issues or queries please do feel free to mail us.
                Do try to participate in the valuable sessions organized by <strong>{}</strong> in the upcoming days. <br /><br />
                Thanking you.
                </p>
                </body>
                </html>
                '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Volunteer Certificate":
        return '''\
                <html>
                <body>
                <p>
                Greetings {}! ✨<br /><br />
                {} deeply honours your hearty volunteering in organising <strong>{}</strong>.<br /><br />
                Please go through the certificate attached herewith.<br />
                In case of any issues or queries please do feel free to mail us. 
                Do try to coordinate with <strong>{}</strong> in the upcoming days! <br /><br />
                Thanking you.
                </p>
                </body>
                </html>
                '''.format(recipient_name, issuing_organization, event_name, issuing_organization)

    elif certificate_title == "Coordinator Certificate":
        return '''
                <html>
                <body>
                <p>
               Greetings {}! ✨<br /><br />
               {} deeply honours your hearty coordination in organising <strong>{}</strong>.<br /><br />
               Please go through the certificate attached herewith.
               In case of any issues or queries please do feel free to mail us. <br /><br />
               We expect the same in the upcoming events too!<br /><br />
               Thanking you.
               </p>
                </body>
                </html>
               '''.format(recipient_name, issuing_organization, event_name)


def mail(cert, recipient_email):
    print("sending certificate to {}".format(recipient_email))
    sys.stdout.flush()

    load_dotenv()
    port = 465
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    # "alternative" for using plain/html alternatively based on client.
    message = MIMEMultipart("alternative")
    message["subject"] = "{} | {} | {}".format(cert.certificate_title, cert.event_name, cert.issuing_organization)
    message["From"] = "{}".format(cert.issuing_organization)
    message["To"] = recipient_email

    # content as plain/html text.
    plain_content_string = generate_plain_mail_content(cert.recipient_name, cert.certificate_title, cert.event_name, cert.issuing_organization)

    html_content_string = generate_html_mail_content(cert.recipient_name, cert.certificate_title, cert.event_name, cert.issuing_organization)

    # converting content to respective MIMEText objects
    plain_part = MIMEText(plain_content_string, "plain")
    html_part = MIMEText(html_content_string, "html")

    # attaching html and plain parts to MIMEMultipart object.
    message.attach(plain_part)
    message.attach(html_part)

    # Open PDF file in binary mode
    with open(cert.cert_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        attachment_part = MIMEBase("application", "pdf")
        attachment_part.set_payload(attachment.read())

    # 'Content-Disposition' Response header because content is expected to be locally downloadable
    # filename parameter specifies the filename of the file received by the recipient.
    attachment_part.add_header("Content-Disposition", "attachment", filename=cert.recipient_name + '.pdf')

    # Encodes the payload into base64 form and sets the Content-Transfer-Encoding header to base64
    encoders.encode_base64(attachment_part)

    # Add attachment to message and convert message to string
    message.attach(attachment_part)

    # creates an ssl context and verifies its certificates
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as gmail_smtp_server:
        try:
            gmail_smtp_server.login(sender_email, sender_password)
            gmail_smtp_server.sendmail(sender_email, recipient_email, message.as_string())
            print("successfully sent mail to {}".format(recipient_email))
            sys.stdout.flush()
            return None
        except Exception as e:
            print("failed sending mail to {}".format(recipient_email))
            sys.stdout.flush()
            return recipient_email


def zip_dir(to_zip_dir_name, purpose):
    execution_mode = os.environ.get('EXECUTION_MODE')
    out_dir = "./generated_certificates/zipped/" if (execution_mode == 'test') else "src/scripts/generated_certificates/zipped/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    file_paths = []
    for root, directories, files in os.walk(to_zip_dir_name):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    out_file_path = out_dir + purpose + '.zip'
    with ZipFile(out_file_path, 'w') as zip_file:
        for file in file_paths:
            zip_file.write(file, os.path.basename(file))

    return out_file_path


def mail_zip(zipped_file_path, recipient_email, purpose, subject_line, plain_content_string, html_content_string, mail_not_send_csv_path, csv_file_path):
    load_dotenv()
    port = 465
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    # "alternative" for using plain/html alternatively based on client.
    message = MIMEMultipart("alternative")
    message["subject"] = subject_line
    # message["From"] = os.environ.get('APP_NAME')
    message["From"] = formataddr((str(Header(os.environ.get('APP_NAME'), 'utf-8')), 'ieee@gecskp.ac.in'))
    message["To"] = recipient_email

    # converting content to respective MIMEText objects
    plain_part = MIMEText(plain_content_string, "plain")
    html_part = MIMEText(html_content_string, "html")

    # attaching html and plain parts to MIMEMultipart object.
    message.attach(plain_part)
    message.attach(html_part)

    # Open PDF file in binary mode
    with open(zipped_file_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        attachment_part = MIMEBase("application", "zip")
        attachment_part.set_payload(attachment.read())

    # 'Content-Disposition' Response header because content is expected to be locally downloadable
    # filename parameter specifies the filename of the file received by the recipient.
    attachment_part.add_header("Content-Disposition", "attachment", filename='{}.zip'.format(purpose))

    # Encodes the payload into base64 form and sets the Content-Transfer-Encoding header to base64
    encoders.encode_base64(attachment_part)

    # Add attachment to message and convert message to string
    message.attach(attachment_part)

    if mail_not_send_csv_path is not None:
        with open(mail_not_send_csv_path, "rb") as attachment:
            attachment_part = MIMEBase("application", "csv")
            attachment_part.set_payload(attachment.read())

        # 'Content-Disposition' Response header because content is expected to be locally downloadable
        # filename parameter specifies the filename of the file received by the recipient.
        attachment_part.add_header("Content-Disposition", "attachment", filename='mail_not_send.csv')

        # Encodes the payload into base64 form and sets the Content-Transfer-Encoding header to base64
        encoders.encode_base64(attachment_part)

        # Add attachment to message and convert message to string
        message.attach(attachment_part)

    if csv_file_path is not None:
        with open(csv_file_path, "rb") as attachment:
            attachment_part = MIMEBase("application", "csv")
            attachment_part.set_payload(attachment.read())

        # 'Content-Disposition' Response header because content is expected to be locally downloadable
        # filename parameter specifies the filename of the file received by the recipient.
        attachment_part.add_header("Content-Disposition", "attachment", filename='recipientData.csv')

        # Encodes the payload into base64 form and sets the Content-Transfer-Encoding header to base64
        encoders.encode_base64(attachment_part)

        # Add attachment to message and convert message to string
        message.attach(attachment_part)

    # creates an ssl context and verifies its certificates
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as gmail_smtp_server:
        try:
            gmail_smtp_server.login(sender_email, sender_password)
            gmail_smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        except Exception as e:
            sys.stderr.write("Cert Mail Zip: {}".format(e))
            sys.stderr.flush()


def notify(dir_name, auth_user_email, auth_user_name, purpose, successfully_completed, action_time, error_email_list, csv_file_path):
    execution_mode = os.environ['EXECUTION_MODE']

    sys.stdout.write("notifying action to authorities...")
    sys.stdout.flush()

    zipped_file_path = zip_dir(dir_name, purpose)
    recipient_emails = [os.environ.get('MAINTAINER_EMAIL')]
    recipient_emails.append(os.environ.get('CHAIR_EMAIL')) if (os.environ.get('DB_MODE') == "production") else None
    recipient_names = [os.environ.get('MAINTAINER_NAME'), os.environ.get('CHAIR_NAME')]
    recipient_names.append(os.environ.get('CHAIR_NAME')) if (os.environ.get('DB_MODE') == "production") else None

    mail_not_send = {
        "Mail not sent to": error_email_list
    }

    mail_not_send = pd.DataFrame(mail_not_send)
    mail_not_send_csv_path = './generated_certificates/mail_not_send.csv' if execution_mode == 'test' else 'src/scripts/generated_certificates/mail_not_send.csv'
    mail_not_send.to_csv(mail_not_send_csv_path)

    for recipient_email, recipient_name in zip(recipient_emails, recipient_names):
        subject_line = "{} | {} | {}".format(os.environ.get('APP_NAME'), purpose, "Notification")

        plain_content_string = """\
                    Hii {},

                    {} - issued{}.

                    -----------------------------
                    Action Authenticated by {}
                    Action Time: {}
                    Action Successfully Completed: {}
                    ------------------------------

                    Please find the Zipped Backup as attachment.
                    
                    Regards,
                    ACGAM.
                    ,
                    .
                    """.format(recipient_name, purpose, "" if successfully_completed else ", but incomplete", auth_user_name, action_time, successfully_completed)

        html_content_string = """\
                    <html>
                      <body>
                        <p>Hii, <strong>{}</strong><br><br>
                            {} - issued{}.<br><br>
                            -----------------------------<br>
                            Action Authenticated by {}.<br>
                            Action Time: {}<br>
                            Action Successfully Completed: <span style=\"color:{}\">{}</span><br>
                            -----------------------------<br><br>
                            Please find the Zipped Backup as attachment.<br /><br />
                            Regards,<br />
                            ACGAM.<br /><br />
                        </p>
                      </body>
                    </html>
                    """.format(recipient_name, purpose, "" if successfully_completed else ", but incomplete", auth_user_name, action_time,"green" if successfully_completed else "red", successfully_completed)
        mail_zip(zipped_file_path, recipient_email, purpose, subject_line, plain_content_string, html_content_string, mail_not_send_csv_path if error_email_list else None, csv_file_path)

    sys.stdout.write("sending backup zip...")
    sys.stdout.flush()

    subject_line = "{} | {} | {}".format(os.environ.get('APP_NAME'), purpose, "Backup")

    plain_content_string = """\
                        Hii {},

                        {} - issued{}.

                        -----------------------------
                        Action Time: {}
                        Action Successfully Completed: {}
                        -----------------------------

                        Please find the Zipped Backup as attachment.

                        Regards,
                        ACGAM.
                        """.format(auth_user_name, purpose, "" if successfully_completed else ", but incomplete", action_time, successfully_completed)

    html_content_string = """\
                        <html>
                          <body>
                            <p>Hii, <strong>{}</strong><br><br>
                                {} - issued{}.<br><br>
                                -----------------------------<br>
                                Action Time: {}<br>
                                Action Successfully Completed: <span style=\"color:{}\">{}</span><br>
                                -----------------------------<br><br>
                                Please find the Zipped Backup as attachment.<br /><br />
                                Regards,<br />
                                ACGAM.<br /><br />
                            </p>
                          </body>
                        </html>
                        """.format(auth_user_name, purpose, "" if successfully_completed else ", but incomplete", action_time,"green" if successfully_completed else "red", successfully_completed)
    mail_zip(zipped_file_path, auth_user_email, purpose, subject_line, plain_content_string, html_content_string, mail_not_send_csv_path if error_email_list else None, None)

    sys.stdout.write("backup sent....")
    sys.stdout.flush()
    os.remove(mail_not_send_csv_path)
