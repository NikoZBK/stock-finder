from twilio.rest import Client
import smtplib
import ssl


def sendEmail(product, url):
    port = 465

    sender_email = ""
    receiver_email = ""
    email_password = ""
    message = """\
        Subject: STOCK ALERT ({})

        STOCK FOUND: {}""".format(product, url)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print('Exception caught sending email: [{}]'.format(e))


def sendSMS(product, url):
    to_number = '+1234567890'
    from_number = '+1234567890'
    account_sid = 'twilioapi'
    auth_token = 'twilioapi'
    try:
        client = Client(account_sid, auth_token)
        client.messages.create(to=to_number,
                               from_=from_number,
                               body="{} stock found: {}".format(product, url))
    except Exception as e:
        print('Exception caught sending SMS: [{}]'.format(e))


def sendAlerts(product, url):
    sendSMS(product, url)
    sendEmail(product, url)


class Alert:
    def __init__(self, product, url):
        sendAlerts(product, url)
