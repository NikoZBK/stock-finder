import os
from configparser import ConfigParser, NoOptionError

try:
    parser = ConfigParser()
    cfg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stockfinder' + '.ini')
    parser.read(cfg_file)
except(FileExistsError, Exception) as e:
    print('Exception reading settings file: [{}]'.format(e))


def get_email():
    try:
        return parser.get('CREDENTIALS', 'email')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving email address: [{}]'.format(e2))


def get_email_password():
    try:
        return parser.get('CREDENTIALS', 'password')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving email password: [{}]'.format(e2))


def get_to_number():
    try:
        return parser.get('CREDENTIALS', 'to_number')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving to-number: [{}]'.format(e2))


def get_from_number():
    try:
        return parser.get('CREDENTIALS', 'from_number')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving from-number: [{}]'.format(e2))


def get_account_sid():
    try:
        return parser.get('CREDENTIALS', 'account_sid')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving account sid: [{}]'.format(e2))


def get_auth_token():
    try:
        return parser.get('CREDENTIALS', 'auth_token')
    except(ValueError, NoOptionError, Exception) as e2:
        print('Exception retrieving auth token: [{}]'.format(e2))
