import webbrowser
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class R5600x:
    def __init__(self, headers):
        self.headers = headers
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

        URL = 'https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666?Description=ryzen%205600x&cm_re=ryzen_5600x-_-19-113-666-_-Product'
        try:
            page = requests.get(URL, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            product = soup.find(class_='product-buy-box')
            inventory = 0
            totalinventory = 1
            in_stock = not soup.find(class_='btn btn-message btn-wide').text.lower().strip().__contains__('sold')
            if in_stock:
                inventory += 1
                webbrowser.open_new_tab(URL)
                Alert('5600X', URL)
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
        try:
            page = requests.get(URL, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            inventory = 0
            totalinventory = 1
            in_stock = not soup.find(class_='fulfillment-add-to-cart-button').text.lower().__contains__('sold')
            if in_stock:
                inventory += 1
                webbrowser.open_new_tab(URL)
                Alert('5600X', URL)
                print('\n{} 5600X found: {}'.format(getTime(), URL))
                # writeToFile(URL)
                # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0
