import requests
from requests.auth import HTTPBasicAuth
import json

ticket = ""

usr = ''
pw = ''

jira_url = "https://jira.com"
endpoint = "jira/rest/api/2/issue"

def get_jira_ticket_status(ticket_number):
    url = f"{jira_url}/{endpoint}/{ticket_number}"
    res = requests.get(url, auth=HTTPBasicAuth(usr, pw))
    r = res.text
    j = json.loads(r)
    # for k,v in j.items():
    #     print(f'{k} -> {v}')
    for k,v in j['fields'].items():
        if k.startswith('status'):
            di = v['statusCategory']
            status = di['name']
            return status

status = get_jira_ticket_status(ticket)
