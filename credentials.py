import os
from configparser import ConfigParser, NoOptionError

parser = ConfigParser()
cfg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stockfinder' + '.ini')


def get_email():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'email')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving email address: [{}]'.format(e))


def get_email_password():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'password')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving email password: [{}]'.format(e))


def get_to_number():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'to_number')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving to-number: [{}]'.format(e))


def get_from_number():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'from_number')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving from-number: [{}]'.format(e))


def get_account_sid():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'account_sid')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving account sid: [{}]'.format(e))


def get_auth_token():
    try:
        parser.read(cfg_file)
        return parser.get('CREDENTIALS', 'auth_token')
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception retrieving auth token: [{}]'.format(e))
