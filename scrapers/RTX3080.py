import webbrowser
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from Alert import Alert


def getTime():
    return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))


class RTX3080:
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

        URL = 'https://www.newegg.com/p/pl?d=rtx+3080&LeftPriceRange=699.99+750'  # Price Range: $699 - $750
        try:
            page = requests.get(URL, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            rtx_elems = soup.find_all(class_='item-container')
            inventory = 0
            totalinventory = len(rtx_elems)
            for rtx_elem in rtx_elems:
                product_name = rtx_elem.find(class_='item-title').text.strip()
                in_stock = rtx_elem.find(class_='item-button-area').text.lower().strip().__contains__('add')
                if in_stock:
                    inventory += 1
                    link = rtx_elem.find('a')['href']
                    webbrowser.open_new_tab(link)
                    Alert('3080', link)
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
        try:
            page = requests.get(URL, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            rtx_elems = soup.find_all(class_='fulfillment-add-to-cart-button')
            inventory = 0
            totalinventory = len(rtx_elems)
            for rtx_elem in rtx_elems:
                in_stock = rtx_elem.text.lower().__contains__('add')
                if in_stock:
                    inventory += 1
                    link = 'https://www.bestbuy.com' + rtx_elem.find('a')['href']
                    webbrowser.open_new_tab(link)
                    Alert('3080', link)
                    print('\n{} 3080 found: {}'.format(getTime(), link))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0
