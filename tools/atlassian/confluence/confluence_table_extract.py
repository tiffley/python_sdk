import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
import pandas as pd

space = "DITD"
title = "aaa"

config_path = "config.json"
filename = "output.csv"

def get_url(space, title):
    content_url = f"https://confluence.rakuten-it.com/confluence/rest/api/content?spaceKey={space}&title={title}&expand=body.storage"
    return content_url

def get_confluence_content(usr, pw):
    content_url = get_url(space, title)
    response = requests.get(content_url, auth=HTTPBasicAuth(usr, pw))
    if response.status_code != 200:
        print('access error')
        return False
    return response.json()["results"]

def get_html():
    di = json.load(open(config_path))
    usr = di.get("user")
    pw = di.get("pw")
    return get_confluence_content(usr, pw)[0]["body"]["storage"]["value"]

# pandas style
def df_style(html):
    dfs = pd.io.html.read_html(html)
    i=0
    for df in dfs:
        i=i+1
        df.to_csv("items/"+str(i)+filename)

# bs style
def bs_style(html):
    bsObj = BeautifulSoup(html, "html.parser")
    tables = bsObj.findAll("table")
    for table in tables:
        rows = table.findAll("tr")
        print(rows)

def main():
    html = get_html()
    df_style(html)
    # bs_style()


if __name__ == '__main__':
    main()
