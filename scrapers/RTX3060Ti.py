from bs4 import BeautifulSoup
import requests
import webbrowser
from datetime import datetime
from Alert import Alert
from colorama import init, Fore


class RTX3060Ti:
    def __init__(self, headers):
        init(autoreset=True)
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

        URL = 'https://www.newegg.com/p/pl?d=3060+ti&LeftPriceRange=399+450'  # Price Range: $399 - $450
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
                    Alert('3060Ti', link)
                    print(Fore.GREEN + '{} 3060 Ti found: {}'.format(self.getTime(), link))
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
                    Alert('3060Ti', link)
                    print(Fore.GREEN + '{} 3060 Ti found: {}'.format(self.getTime(), link))
                    # writeToFile(URL)
                    # return 1
            print('[{} / {}]'.format(inventory, totalinventory))
            self.stock += inventory
        except(ConnectionError, Exception) as e:
            print('Exception trying to retrieve bestbuy data. [{}]'.format(e))
        # return 0

    def getTime(self):
        return '[{}]'.format(datetime.now().strftime("%H:%M:%S"))
