import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

# https://minkabu.jp/news/3637268
# https://minkabu-jp.translate.goog/news/3637268?_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp
# https://toyokeizai.net/articles/-/668776?page=3
# https://toyokeizai-net.translate.goog/articles/-/668776?page=3&_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp

class GoogleTranslateRedirect:
    def __init__(self, driver=None):
        self.driver = driver if driver else webdriver.Chrome()
        self.soup = None
        self.url = None

    def set_url(self, url, transform=True):
        self.url = self.generate_ggl_url_from_original_url(url) if transform else url

    def generate_ggl_url_from_original_url(self, url):
        suffix = '_x_tr_sl=ja&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp'
        tg = url.split('://')
        li = tg[1].split('/')
        core_url = f"{tg[0]}://{li[0].replace('.','-')}.translate.goog/{'/'.join(li[1:])}"
        if '?' in li[-1]:
            return f"{core_url}&{suffix}"
        return f"{core_url}?{suffix}"

    def update_soup(self, sec=0):
        flag = True
        while flag:
            try:
                self.driver.get(self.url)
                flag = False
            except:
                print('retry - timeout?')
                sleep(5)
        sleep(sec)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')

if __name__ == '__main__':
    cls = GoogleTranslateRedirect()
    url = 'https://minkabu.jp/news/3637268'
    url = 'https://toyokeizai.net/articles/-/668776?page=3'

    # res = cls.generate_ggl_url_from_original_url(url)
    # print(res)
    # exit()

    cls.set_url(url)
    cls.update_soup()

