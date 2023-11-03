import requests
from requests.auth import HTTPBasicAuth
import json

ticket = ""
status_id = 2

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

def change_ticket_status(ticket_number, status):
    '''
    :param ticket_number: SPDBPIPE-xxx
    :param status: int
    :return: api response
    status
    2: CLOSED
    3: REOPENED - valid only if the status is closed or resolved
    4: In Progress - invalid if the status is closed or resolved
    5: RESOLVED
    status change is valid this way
    [open, reopened] -> [in progress] -> [closed, resolved]
    '''
    url = f"{jira_url}/{endpoint}/{ticket_number}/transitions"
    payload = json.dumps({
        "transition": {"id": int(status)}
    })
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    res = requests.post(url, auth=HTTPBasicAuth(usr, pw), data=payload, headers=headers)
    return res

def change_ticket_summary(ticket_number, title):
    url = f"{jira_url}/{endpoint}/{ticket_number}"
    payload = json.dumps({
        "update": {
            "summary": [
                {
                  "set": title
                }
            ]
        }
    })
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    res = requests.put(url, auth=HTTPBasicAuth(usr, pw), data=payload, headers=headers)
    return res


status = get_jira_ticket_status(ticket)
print(status)
res = change_ticket_status(ticket, status_id)
print(res)
print(res.text)
status = get_jira_ticket_status(ticket)
print(status)

