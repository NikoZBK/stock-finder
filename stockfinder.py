# AIO Scraper by ZBK
# Searches for PS5, RTX 3000 Series Stock
# 1/3/2021

import os
import re
import time
from configparser import ConfigParser, NoOptionError
from datetime import datetime

from scrapers import PlayStation5, RTX3060Ti, RTX3070, RTX3080, R5600x

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def process():
    inventory = 0
    if PS5_FLAG:
        print('{} Searching for PS5 stock...'.format(get_time()))
        ps5 = PlayStation5(LINK_FLAG, EMAIL_FLAG, SMS_FLAG)
        inventory += ps5.getStock()
    if RTX3060TI_FLAG:
        print('{} Searching for RTX 3060 Ti stock...'.format(get_time()))
        r3060ti = RTX3060Ti(LINK_FLAG, EMAIL_FLAG, SMS_FLAG)
        inventory += r3060ti.getStock()
    if RTX3070_FLAG:
        print('{} Searching for RTX 3070 stock...'.format(get_time()))
        r3070 = RTX3070(LINK_FLAG, EMAIL_FLAG, SMS_FLAG)
        inventory += r3070.getStock()

    if RTX3080_FLAG:
        print('{} Searching for RTX 3080 stock...'.format(get_time()))
        r3080 = RTX3080(LINK_FLAG, EMAIL_FLAG, SMS_FLAG)
        inventory += r3080.getStock()

    if R5600X_FLAG:
        print('{} Searching for R5600X stock...'.format(get_time()))
        r5600x = R5600x(LINK_FLAG, EMAIL_FLAG, SMS_FLAG)
        inventory += r5600x.getStock()

    if inventory == 0:
        print('{} No stock found. Checking again in {} minutes.'.format(get_time(), MINUTES))
    else:
        print('{} Stock found! Checking again in {} minutes.'.format(get_time(), MINUTES))
        # return False
    time.sleep(MINUTES * 60)
    return True


def get_time():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


def main():
    doAgain = True
    while doAgain:
        doAgain = process()
    continue_search = input("Search again? [y/N]: ").lower().strip().startswith('y')
    if continue_search:
        main()


if __name__ == '__main__':
    print('Stock Finder AIO 1.0 by ZBK')
    parser = ConfigParser()
    suffix = '.ini'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cfg_file = os.path.join(dir_path, 'stockfinder' + suffix)

    if not os.path.isfile(cfg_file):
        try:
            parser['SETTINGS'] = {"timer": "1"}
            parser['OPTIONS'] = {"ps5": "1", "rtx3060ti": "1", "rtx3070": "1", "rtx3080": "1", "r5600x": "1"}
            parser['ALERTS'] = {"link": "0", "email": "0", "sms": "0"}
            parser['CREDENTIALS'] = {"email": "", "password": "", "from_number": "+12345678912",
                                     "to_number": "+12345678912", "account_sid": "", "auth_token": ""}
            with open('stockfinder.ini', 'w') as configfile:
                parser.write(configfile)
        except Exception as e:
            print('Exception creating configuration file: [{}]'.format(e))

    try:
        parser.read(cfg_file)
        MINUTES = parser.getfloat('SETTINGS', 'timer')
        PS5_FLAG = parser.getint('OPTIONS', 'ps5')
        RTX3060TI_FLAG = parser.getint('OPTIONS', 'rtx3060ti')
        RTX3070_FLAG = parser.getint('OPTIONS', 'rtx3070')
        RTX3080_FLAG = parser.getint('OPTIONS', 'rtx3080')
        R5600X_FLAG = parser.getint('OPTIONS', 'r5600x')
        LINK_FLAG = parser.getint('ALERTS', 'link')
        EMAIL_FLAG = parser.getint('ALERTS', 'email')
        SMS_FLAG = parser.getint('ALERTS', 'sms')
        configuration = 'Search interval: [{}]\n' \
                        'Search options: PS5 [{}] 3060 Ti [{}] 3070 [{}] 3080 [{}] 5600X [{}]\n' \
                        'Alerts: Link [{}] Email [{}] SMS [{}]'.format(MINUTES,
                                                                       PS5_FLAG,
                                                                       RTX3060TI_FLAG,
                                                                       RTX3070_FLAG,
                                                                       RTX3080_FLAG,
                                                                       R5600X_FLAG,
                                                                       LINK_FLAG, EMAIL_FLAG, SMS_FLAG)

        configuration = re.sub(r'\[[^1]\]', '[N]', configuration)
        configuration = re.sub(r'\[1\]', '[Y]', configuration)
        print(configuration)
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception reading configuration file: [{}]'.format(e))
    main()
