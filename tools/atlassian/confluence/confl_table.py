import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import pandas as pd
import json
import pandas as pd
import datetime

now = datetime.date.today()

username = "takaakira.yamauchi"
password = ""
file_path = "table.csv"


############  Get the confluence data via confluence api
def get_confluence_content():
    content_url = "https://confluence.rakuten-it.com/confluence/rest/api/content?spaceKey=TD&title=20190603+RPMM+OSAKA+-+Attendees+List&expand=body.storage".format(
        now.year, '{:02d}'.format(now.month))
    response = requests.get(content_url, auth=HTTPBasicAuth(username, password))
    return response.json()["results"]


###########   Create the table data from confluence to csv
def create_data_tb_csv():
    confluence_content = get_confluence_content()
    html_data = confluence_content[0]["body"]["storage"]["value"]

    ###########  Get the table from the html body
    table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(html_data, "lxml")("tr")]
    table_list = []

    table_header = [[cell.text for cell in row("th")] for row in BeautifulSoup(html_data, "lxml")("tr")]
    table_header_list = []

    to_remove = ['Green', 'Yellow']

    ########### Ignore the empty list from the list
    for data in table_data:
        if len(data) != 0:
            data = list(map(lambda x: x.replace('Green', '').replace('Yellow', ''), data))
            print(data)
            table_list.append(data)

    ########### Ignore the empty list from the list
    for data in table_header:
        if len(data) != 0:
            table_header_list.append(data)

    ########## Convert the result into csv and create a file
    df = pd.DataFrame(table_list)
    # df.columns = table_header_list[0]
    df.to_csv(file_path, index=None, header=table_header_list[0], encoding='utf-8')


def main():
    res = get_confluence_content()
    print(res)
    create_data_tb_csv()

if __name__ == '__main__':
    main()