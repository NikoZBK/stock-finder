import re
import webbrowser
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import stockfinder
from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class RTX3060Ti:
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
        URL = 'https://www.newegg.com/p/pl?d=3060+ti&LeftPriceRange=399+530'  # Price Range: $399 - $530
        try:
            page = requests.get(URL, headers=self.HEADERS)
            soup = BeautifulSoup(page.content, 'html.parser')
            rtx_elems = soup.find_all(class_='item-container')
            inventory = 0
            totalinventory = len(rtx_elems)
            for rtx_elem in rtx_elems:
                if rtx_elem.__eq__(None):
                    totalinventory -= 1
                    continue
                in_stock = rtx_elem.find(class_='item-button-area').text.lower().strip().__contains__('add')
                if in_stock:
                    inventory += 1
                    link = rtx_elem.find('a')['href']
                    if self.LINK_FLAG:
                        webbrowser.open_new_tab(link)
                    if self.EMAIL_FLAG or self.SMS_FLAG:
                        Alert('3060Ti', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} 3060 Ti found: {}'.format(getTime(), link))
                    # writeToFile(link)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve Newegg data [{}]'.format(e))
        # return 0

    def getBestBuy(self):
        print('Checking BestBuy...\t', end='', flush='True')
        URL = 'https://www.bestbuy.com/site/searchpage.jsp?st=%223060+Ti%22&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys'
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
                        Alert('3060Ti', link, self.EMAIL_FLAG, self.SMS_FLAG)
                    print('\n{} 3060 Ti found: {}'.format(getTime(), link))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0
