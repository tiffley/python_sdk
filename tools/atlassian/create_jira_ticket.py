from requests.auth import HTTPBasicAuth
import requests
import json


li = [
    {"summary": "page1", "description": "created by jira api"},
    {"summary": "page2", "description": "page2"}
]

usr = ''
pw = ''

jira_url = "https://jira.com"
endpoint = "jira/rest/api/2/issue"

class PageGenerator:
    def __init__(self, user: str, password: str, project=""):
        self.url = f'{jira_url}/{endpoint}'
        self.auth = HTTPBasicAuth(user, password)
        self.headers = {'Content-Type': 'application/json'}
        self.project = project

    def create_issue(self, summary, description, issuetype="Task", priority="Major") -> None:
        data = {
            "fields": {
                "project": {
                    "key": self.project
                },
                "summary": summary,
                "issuetype": {
                    "name": issuetype
                },
                "priority": {
                    "name": priority
                },
                "description": description
               }
            }
        try:
            r = requests.post(url=self.url, data=json.dumps(
                data), headers=self.headers, auth=self.auth)
            if not r.status_code // 100 == 2:
                print("Error: Unexpected response {}".format(r.text))
            else:
                print(f'Page Created! {jira_url}/jira/browse/{json.loads(r.text)["key"]}')
        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))

if __name__ == '__main__':
    cls = PageGenerator(usr, pw)
    for di in li:
        cls.create_issue(**di)
