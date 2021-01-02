# AIO Scraper by ZBK
# Searches for PS5, RTX 3000 Series Stock
# 1/1/2021

import logging
import os
import time
from configparser import ConfigParser, NoOptionError
from datetime import datetime

from scrapers import PlayStation5, RTX3060Ti, RTX3070, RTX3080, R5600x

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66'}
MINUTES = 0.5  # how frequent to check for stock

# Default Flags
PS5_FLAG = RTX3060TI_FLAG = RTX3070_FLAG = RTX3080_FLAG = R5600X_FLAG = 1


def process():
    inventory = 0
    if PS5_FLAG:
        print('{} Searching for PS5 stock...'.format(getTime()))
        ps5 = PlayStation5(HEADERS)
        inventory += ps5.getStock()
    if RTX3060TI_FLAG:
        print('{} Searching for RTX 3060 Ti stock...'.format(getTime()))
        r3060ti = RTX3060Ti(HEADERS)
        inventory += r3060ti.getStock()
    if RTX3070_FLAG:
        print('{} Searching for RTX 3070 stock...'.format(getTime()))
        r3070 = RTX3070(HEADERS)
        inventory += r3070.getStock()

    if RTX3080_FLAG:
        print('{} Searching for RTX 3080 stock...'.format(getTime()))
        r3080 = RTX3080(HEADERS)
        inventory += r3080.getStock()

    if R5600X_FLAG:
        print('{} Searching for R5600X stock...'.format(getTime()))
        r5600x = R5600x(HEADERS)
        inventory += r5600x.getStock()

    if inventory == 0:
        print('{} No stock found. Checking again in {} minutes.'.format(getTime(), MINUTES))
    else:
        print('{} Stock found! Checking again in {} minutes.'.format(getTime(), MINUTES))
    time.sleep(MINUTES * 60)
    return True


def getTime():
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
    print(cfg_file)

    if not os.path.isfile(cfg_file):
        try:
            parser['OPTIONS'] = {"ps5": "1", "rtx3060ti": "1", "rtx3070": "1", "rtx3080": "1", "r5600x": "1"}
            parser['CREDENTIALS'] = {"email": "", "password": "", "from_number": "+1234567890",
                                     "to_number": "+1234567890"}
            with open('stockfinder.ini', 'w') as configfile:
                parser.write(configfile)
        except Exception as e:
            print('Exception creating configuration file: [{}]'.format(e))

    try:
        parser.read(cfg_file)
        PS5_FLAG = parser.getint('OPTIONS', 'ps5')
        RTX3060TI_FLAG = parser.getint('OPTIONS', 'rtx3060ti')
        RTX3070_FLAG = parser.getint('OPTIONS', 'rtx3070')
        RTX3080_FLAG = parser.getint('OPTIONS', 'rtx3080')
        R5600X_FLAG = parser.getint('OPTIONS', 'r5600x')
        configuration = 'Search options: PS5 [{}] 3060 Ti [{}] 3070 [{}] 3080 [{}] 5600X [{}]'.format(PS5_FLAG,
                                                                                                      RTX3060TI_FLAG,
                                                                                                      RTX3070_FLAG,
                                                                                                      RTX3080_FLAG,
                                                                                                      R5600X_FLAG)
        configuration = configuration.replace('[0]', '[N]').replace('[1]', '[Y]')
        print(configuration)
    except(ValueError, NoOptionError, Exception) as e:
        print('Exception reading configuration file: [{}]'.format(e))
    logging.basicConfig(level=logging.DEBUG, filename="scraper_log.txt", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    main()
