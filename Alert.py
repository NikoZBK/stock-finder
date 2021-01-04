import smtplib
import ssl

from twilio.rest import Client

import credentials


def sendEmail(self):
    port = 465

    sender_email = credentials.get_email()
    receiver_email = sender_email
    email_password = credentials.get_email_password()
    message = """\
        Subject: STOCK ALERT ({})

        STOCK FOUND: {}""".format(self.product, self.url)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print('Exception caught sending email: [{}]'.format(e))


def sendSMS(self):
    to_number = credentials.get_to_number()
    from_number = credentials.get_from_number()
    account_sid = credentials.get_account_sid()
    auth_token = credentials.get_auth_token()
    try:
        client = Client(account_sid, auth_token)
        client.messages.create(to=to_number,
                               from_=from_number,
                               body="{} stock found: {}".format(self.product, self.url))
    except Exception as e:
        print('Exception caught sending SMS: [{}]'.format(e))


def sendAlerts(self):
    if self.email_flag:
        sendEmail(self)
    if self.sms_flag:
        sendSMS(self)


class Alert:
    def __init__(self, product, url, email_flag, sms_flag):
        self.product = product
        self.url = url
        self.email_flag = email_flag
        self.sms_flag = sms_flag
        sendAlerts(self)
