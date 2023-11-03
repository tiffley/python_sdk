import slackweb
import requests
import json


class Slack:
    def __init__(self, url="https://hooks.slack.com/services/xxx"):
        self.url = url

    def send_by_api(self, txt):
        slack = slackweb.Slack(url=self.url)
        slack.notify(text=txt)

    def send_by_post(self, txt):
        payload = {"text": txt}
        r = requests.post(self.url, data=json.dumps(payload))
        print(r.text)


if __name__ == '__main__':
    sl = Slack()
    txt = "test message from python"
    sl.send_by_api(txt+"-api")
    # sl.send_by_post(txt+"-post")

