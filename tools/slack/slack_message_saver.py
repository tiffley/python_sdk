from slack_api_client import SlackAPI
import pandas
from datetime import datetime

is_test = False

tg_channels = [
    'channel1',
    'channel2'
]
cursor = None
pagenation_limit = 1


users = {}
def get_user(uid):
    if not users.get(uid, None):
        users[uid] = sl.get_user_name_from_id(uid)
    return users.get(uid, 'unknown user')


def fetch_channel(tg_channel):
    # [ {'user_name': , 'posted_date': , 'text': , 'is_reply': }, ... ]
    msgs = sl.get_all_msg_and_replies(tg_channel, pagenation_limit, cursor)
    li = []
    parent_msg_id = 0
    for li_msg in msgs:
        parent_msg_id += 1
        for i, msg in enumerate(li_msg):
            is_reply = False if i == 0 else True
            user_name = get_user(msg['user']) if msg.get('user', None) else "unknown user"
            posted_date = datetime.fromtimestamp(float(msg.get('ts', 0)))
            li.append({'user_name': user_name, 'posted_date': posted_date, 'text': msg.get('text', ""), 'is_reply': is_reply, "thread_id": parent_msg_id})
    return li


def export(msgs, channel):
    di = {'user_name': [], 'posted_date': [], 'text': [], 'is_reply': [], 'thread_id': []}
    for msg in msgs:
        for k in di.keys():
            di[k].append(msg[k])
    df = pandas.DataFrame(di)
    df.to_csv(f'output/{channel}.csv')


if __name__ == '__main__':
    main_token = 'xoxb-'
    sl = SlackAPI(main_token)

    if is_test:
        tg_channel = ""
        res = fetch_channel(tg_channel)
        print(res)
        exit()

    for channel in tg_channels:
        msgs = fetch_channel(channel)
        export(msgs, channel)
