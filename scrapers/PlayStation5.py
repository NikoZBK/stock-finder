import re
import webbrowser
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import stockfinder
from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class PlayStation5:
    def __init__(self, link_flag, email_flag, sms_flag):
        self.HEADERS = stockfinder.HEADERS
        self.LINK_FLAG = link_flag
        self.EMAIL_FLAG = email_flag
        self.SMS_FLAG = sms_flag
        self.stock = 0
        self.getAmazon()
        self.getWalmart()
        self.getBestBuy()
        self.getNewEgg()
        self.getGameStop()

    def getStock(self):
        return self.stock

    # def writeToFile(URL):
    #     with open('ps5stock.txt', 'w') as f:
    #         print(f'{PS5_FOUND} {URL}', file=f)

    # TODO: Target
    def getTarget(self):
        print('Checking Target...\t', end='', flush='True')

        URL = 'https://www.target.com/c/playstation-5-video-games/-/N-hj96dZ5zja9?Nao=0'

        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            ps5_elem = soup.find('div', {'data-test': 'product-card-default'})
            print(ps5_elem)

        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve target store data [{}]'.format(e))

        return 0

    def getSamsClub(self):
        print('Checking Sams Club...\t', end='', flush='True')

        URL = 'https://www.samsclub.com/b/Playstation%205/1206?clubId=6636&offset=0&rootDimension=pcs_availability%253AOnlinepipsymbprice%253A%255B500%2520TO%2520750%255D&searchCategoryId=1206&selectedFilter=all&sortKey=relevance&sortOrder=1'

        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            ps5_elems = soup.find_all(class_='sc-pc-medium-desktop-card sc-plp-cards-card')
            inventory = 0
            totalinventory = len(ps5_elems)
            for ps5_elem in ps5_elems:
                in_stock = not ps5_elem.find('button',
                                             class_='sc-btn sc-btn-primary sc-btn-block sc-pc-action-button sc-pc-add-to-cart').has_attr(
                    'disabled')
                if in_stock:
                    inventory += 1
                    link = 'https://www.samsclub.com' + ps5_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('PS5', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} PS5 found: {}'.format(getTime(), link))
                    # writeToFile(link)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory

        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve Sam\'s club data [{}]'.format(e))

        return 0

    def getNewEgg(self):
        print('Checking Newegg...\t', end='', flush='True')

        URL = 'https://www.newegg.com/p/pl?nm_mc=AFC-RAN-COM&cm_mmc=AFC-RAN-COM&utm_medium=affiliates&utm_source=afc' \
              '-GameSpot&AFFID=2424817&AFFNAME=GameSpot&ACRID=1&ASUBID=gs-gs11006475811-dtp-en%7Cxid%3Afr1605967179676ech' \
              '&ASID=https%3A%2F%2Fwww.gamespot.com%2F&ranMID=44583&ranEAID=2424817&ranSiteID=VZfI20jEa0c' \
              '-qpsf9RpsZIMhmwLtRMkO0w&N=101696840%204021 '
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            ps5_elems = soup.find_all(class_='item-container')
            inventory = 0
            totalinventory = len(ps5_elems)
            for ps5_elem in ps5_elems:
                in_stock = ps5_elem.find(class_='item-button-area').text.lower().strip().__contains__('add')
                if in_stock:
                    inventory += 1
                    link = ps5_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.SMS_FLAG or self.EMAIL_FLAG:
                        Alert('PS5', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} PS5 found: {}'.format(getTime(), link))
                    # writeToFile(link)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve Newegg data [{}]'.format(e))
        # return 0

    def getGameStop(self):
        print('Checking GameStop...\t', end='', flush='True')
        URL = 'https://www.gamestop.com/video-games/playstation-5/consoles'
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            ps5_elems = soup.findAll(class_='add-to-cart-plp-buttons')
            inventory = 0
            totalinventory = len(ps5_elems)
            for ps5_elem in ps5_elems:
                in_stock = ps5_elem.text.lower().__contains__('add')
                if in_stock:
                    inventory += 1
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(URL)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('PS5', URL, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} PS5 found: {}'.format(getTime(), URL))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve gamestop data. [{}]'.format(e))
        # return 0

    # Walmart PS5 pages currently down
    def getWalmart(self):
        print('Checking Walmart...\t', end='', flush='True')
        try:
            # PS5 Digital Edition
            URL = 'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815'
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            inventory = 0
            totalinventory = 2
            in_stock = not soup.find('span', class_='prod-product-cta-add-to-cart display-inline-block').__eq__(None)
            if in_stock:
                inventory += 1
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(URL)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('PS5 Digital', URL, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} PS5 found: {}'.format(getTime(), URL))
                # writeToFile(URL)
                # return 1
            # PS5 Disc Edition
            URL = 'https://www.walmart.com/ip/PlayStation-5-Console/363472942'
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            in_stock = not soup.find('span', class_='prod-product-cta-add-to-cart display-inline-block').__eq__(None)
            if in_stock:
                inventory += 1
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(URL)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('PS5', URL, self.EMAIL_FLAG, self.SMS_FLAG)
                print('{} PS5 found: {}'.format(getTime(), URL))
                # writeToFile(URL)
                # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve walmart data. [{}]'.format(e))
        # return 0

    def getBestBuy(self):
        print('Checking BestBuy...\t', end='', flush='True')
        URL = 'https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973'
        stock_available = re.compile('add|see details')
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            ps5_elems = soup.find_all(class_='fulfillment-add-to-cart-button')
            inventory = 0
            totalinventory = len(ps5_elems)
            for ps5_elem in ps5_elems:
                add_to_cart_text = ps5_elem.text.lower()
                in_stock = re.search(stock_available, add_to_cart_text)
                if in_stock:
                    inventory += 1
                    link = 'https://www.bestbuy.com' + ps5_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('PS5', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} PS5 found: {}'.format(getTime(), link))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0

    def getAmazon(self):
        # Amazon requires a special header
        amazon_headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        print('Checking Amazon...\t', end='', flush='True')
        URL = 'https://www.amazon.com/PlayStation-5-Digital/dp/B08FC6MR62/ref=sr_1_7?crid=GPI3HCDC7U4D&dchild=1&keywords=ps5+digital+edition&qid=1609975951&sprefix=ps5+d%2Caps%2C172&sr=8-7'
        stock_text = re.compile('currently unavailable|available from these')
        try:
            page = requests.get(URL, headers=amazon_headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            inventory = 0
            totalinventory = 2
            # Digital
            unavailable_text = soup.select("span.a-size-medium")[0].text.lower().strip()
            in_stock = not re.search(stock_text, unavailable_text)
            if in_stock:
                inventory += 1
                link = URL
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(link)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('PS5', link, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} PS5 found: {}'.format(getTime(), link))
                # writeToFile(URL)
                # return 1
            # Disc
            URL = 'https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=sr_1_4?dchild=1&keywords=ps5&qid=1609975756&sr=8-4'
            page = requests.get(URL, headers=amazon_headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            unavailable_text = soup.select("span.a-size-medium")[0].text.lower().strip()
            in_stock = not re.search(stock_text, unavailable_text)
            if in_stock:
                inventory += 1
                link = URL
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(link)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('PS5', link, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} PS5 found: {}'.format(getTime(), link))
                # writeToFile(URL)
                # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve amazon data. [{}]'.format(e))
    # return 0
