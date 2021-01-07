import re
import webbrowser
from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup

import stockfinder
from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class R5600x:
    def __init__(self, link_flag, email_flag, sms_flag):
        self.HEADERS = stockfinder.HEADERS
        self.LINK_FLAG = link_flag
        self.EMAIL_FLAG = email_flag
        self.SMS_FLAG = sms_flag
        self.stock = 0
        self.getAmazon()
        self.getBestBuy()
        self.getNewEgg()

    def getStock(self):
        return self.stock

    # def writeToFile(URL):
    #     with open('ps5stock.txt', 'w') as f:
    #         print(f'{PS5_FOUND} {URL}', file=f)

    def getNewEgg(self):
        print('Checking Newegg...\t', end='', flush='True')

        URL = 'https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666?Description=ryzen%205600x&cm_re=ryzen_5600x-_-19-113-666-_-Product'
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            product = soup.find(class_='product-buy-box')
            inventory = 0
            totalinventory = 1
            price = Decimal(re.sub(r'[^\d.]', '', product.find('li', class_='price-current').text.strip()))
            in_stock = product.find(class_='btn btn-primary btn-wide') and price < 310
            if in_stock:
                inventory += 1
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(URL)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('5600X', URL, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} 5600X found: {}'.format(getTime(), URL))
                # writeToFile(link)
                # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve Newegg data [{}]'.format(e))
        # return 0

    def getBestBuy(self):
        print('Checking BestBuy...\t', end='', flush='True')
        URL = 'https://www.bestbuy.com/site/amd-ryzen-5-5600x-4th-gen-6-core-12-threads-unlocked-desktop-processor-with-wraith-stealth-cooler/6438943.p?skuId=6438943'
        stock_available = re.compile('add|see details')
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            inventory = 0
            totalinventory = 1
            in_stock = not soup.find(class_='fulfillment-add-to-cart-button').text.lower().__contains__('sold')
            if in_stock:
                inventory += 1
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(URL)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('5600X', URL, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} 5600X found: {}'.format(getTime(), URL))
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
        URL = 'https://www.amazon.com/AMD-Ryzen-5600X-12-Thread-Processor/dp/B08166SLDF?ref_=ast_sto_dp'
        stock_text = re.compile('currently unavailable|available from these')
        try:
            page = requests.get(URL, headers=amazon_headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            inventory = 0
            totalinventory = 1
            # Digital
            unavailable_text = soup.select("span.a-size-medium")[0].text.lower().strip()
            in_stock = not re.search(stock_text, unavailable_text)
            if in_stock:
                inventory += 1
                link = URL
                if self.LINK_FLAG:
                    webbrowser.open_new_tab(link)
                if self.EMAIL_FLAG or self.SMS_FLAG:
                    Alert('R5600X', link, self.EMAIL_FLAG, self.SMS_FLAG)
                print('\n{} R5600X found: {}'.format(getTime(), link))
                # writeToFile(URL)
                # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve amazon data. [{}]'.format(e))
# return 0
