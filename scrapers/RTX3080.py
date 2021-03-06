import re
import webbrowser
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import stockfinder
from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class RTX3080:
    def __init__(self, link_flag, email_flag, sms_flag):
        self.HEADERS = stockfinder.HEADERS
        self.LINK_FLAG = link_flag
        self.EMAIL_FLAG = email_flag
        self.SMS_FLAG = sms_flag
        self.stock = 0
        self.getBestBuy()
        self.getNewEgg()

    def getStock(self):
        return self.stock

    # def writeToFile(URL):
    #     with open('ps5stock.txt', 'w') as f:
    #         print(f'{PS5_FOUND} {URL}', file=f)

    def getNewEgg(self):
        print('Checking Newegg...\t', end='', flush='True')

        URL = 'https://www.newegg.com/p/pl?d=rtx+3080&LeftPriceRange=699+900'  # Price Range: $699 - $900
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            rtx_elems = soup.find_all(class_='item-button-area')
            inventory = 0
            totalinventory = len(rtx_elems)
            for rtx_elem in rtx_elems:
                if rtx_elem.__eq__(None):
                    totalinventory -= 1
                    continue
                in_stock = rtx_elem.text.lower().strip().__contains__('add')
                if in_stock:
                    inventory += 1
                    link = rtx_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('3080', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} 3080 found: {}'.format(getTime(), link))
                    # writeToFile(link)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve Newegg data [{}]'.format(e))
        # return 0

    def getBestBuy(self):
        print('Checking BestBuy...\t', end='', flush='True')
        URL = 'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&iht=y&keys=keys&ks=960&list=n&qp=currentprice_facet%3DPrice~699.99%20to%20750&sc=Global&st=rtx%203080&type=page&usc=All%20Categories'
        stock_available = re.compile('add|see details')
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            rtx_elems = soup.find_all(class_='fulfillment-add-to-cart-button')
            inventory = 0
            totalinventory = len(rtx_elems)
            for rtx_elem in rtx_elems:
                add_to_cart_text = rtx_elem.text.lower()
                in_stock = re.search(stock_available, add_to_cart_text)
                if in_stock:
                    inventory += 1
                    link = 'https://www.bestbuy.com' + rtx_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('3080', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} 3080 found: {}'.format(getTime(), link))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0
