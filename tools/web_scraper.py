import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

'''
contents = soup.findAll("p", {"class": 'fm01'})
for x in contents:
    val = x.contents[0]
    attr_val = x.find('a')['href']
'''

def get_soup_from_url(url, user=None, pw=None):
    response = requests.get(url, auth=HTTPBasicAuth(user, pw)) if user else requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_soup_from_url_with_codec(url, dec="shift-jis", user=None, pw=None):
    response = requests.get(url, auth=HTTPBasicAuth(user, pw)) if user else requests.get(url)
    html = response.content.decode(dec)
    return BeautifulSoup(html, 'html.parser')


class DynamicWebPageScraper:
    """request module can't get JS generated html. So use this"""
    def __init__(self, url, select_sleep=False):
        self.url = url
        self.driver = webdriver.Chrome()
        self.select_sleep = select_sleep

    def get_soup(self):
        return BeautifulSoup(self.get_html(), 'html.parser')

    def get_html(self):
        self.driver.get(self.url)
        if self.select_sleep:
            self.select_sleep = False
            sleep(15)
        html = self.driver.page_source
        return html


