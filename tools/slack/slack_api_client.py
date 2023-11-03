import requests
import json
from time import sleep

# if response is { "ok": false, "error": "not_in_channel" }
# type below in slack channel
# /invite @Powerful app

class SlackAPI:
    def __init__(self, token):
        self.core_url = 'https://slack.com/api/'
        self.token = token
        self.channel_ids = {}

    def _post_request(self, url, di_params=None):
        headers = {
            'Authorization': f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        # print(di_params)
        return requests.post(url, headers=headers, json=di_params)

    def _get_request(self, url, di_params=None):
        headers = {
            'Authorization': f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        return requests.get(url, headers=headers, params=di_params)

    def _get_response(self, url, di_opt):
        retry = 0
        while True:
            try:
                return self._get_request(url, di_opt)
            except:
                retry += 1
                if retry > 3:
                    return None


    def get_channel_list(self, di_opt=None):
        """
        [{...},{...}]
        dict_keys(
        ['id', 'name', 'is_channel', 'is_group', 'is_im', 'is_mpim', 'is_private', 'created', 'is_archived', 'is_general', 'unlinked', 'name_normalized', 'is_shared', 'is_org_shared', 'is_pending_ext_shared', 'pending_shared', 'context_team_id', 'updated', 'parent_conversation', 'creator', 'is_ext_shared', 'shared_team_ids', 'pending_connected_team_ids', 'is_member', 'topic', 'purpose', 'previous_names', 'num_members'])
        :param di_opt:
        di_opt = {
            "limit": 1000,
            "types": "public_channel"
        }
        """
        url = self.core_url + 'conversations.list'
        r = self._get_response(url, di_opt)
        return json.loads(r.text)['channels'] if r else "NA"

    def _get_channel_id(self, channel_name):
        if self.channel_ids.get(channel_name, None):
            return self.channel_ids.get(channel_name, None)
        di_opt = {
            "limit": 400,
            "types": "private_channel"
        }
        for row in self.get_channel_list(di_opt):
            if row['name'] == channel_name:
                self.channel_ids[channel_name] = row['id']
                return row['id']

        di_opt['types'] = "public_channel"
        for row in self.get_channel_list(di_opt):
            if row['name'] == channel_name:
                self.channel_ids[channel_name] = row['id']
                return row['id']
        raise Exception('channel not found')

    def get_conversation_hist(self, channel_name, opts={}):
        """ https://api.slack.com/methods/conversations.history
        [
            {...}, - di_msg
        ...]
        response di keys sample
        ['client_msg_id', 'type', 'text', 'user', 'ts', 'blocks', 'team', 'thread_ts', 'reply_count', 'reply_users_count', 'latest_reply', 'reply_users', 'is_locked', 'subscribed']
        """
        url = self.core_url + 'conversations.history'
        di_opt = {"channel": self._get_channel_id(channel_name), "limit": 1000}
        if opts:
            for k,v in opts.items():
                di_opt[k] = v
        r = self._get_response(url, di_opt)
        return json.loads(r.text)['messages'] if r else "<<< err failed to fetch message >>>"

    def get_all_conv_hist(self, channel_name, pagenation_limit=10, cursor=None):
        # inclusive: Include messages with oldest or latest timestamps in results. Ignored unless either timestamp is specified.
        # latest: Only messages before this Unix timestamp will be included in results. Default is the current time.
        url = self.core_url + 'conversations.history'
        di_opt = {"channel": self._get_channel_id(channel_name), "limit": 1000}
        if cursor:
            di_opt['cursor'] = cursor

        i = 0
        li_res = []
        while True:
            i += 1
            print(f'poking #{i}')
            res = self._get_response(url, di_opt)
            if not res:
                print(">>> poking err, break")
                break
            res = json.loads(res.text)
            li_res.extend(res['messages'])
            next_cursor = res.get('response_metadata',{}).get('next_cursor', None)
            print(f"next >>> {next_cursor}")
            if not next_cursor or i > pagenation_limit:
                print('poke finished, break')
                break
            di_opt['cursor'] = next_cursor
        return li_res

    def _get_replies(self, channel_name, ts):
        url = self.core_url + 'conversations.replies'
        di_opt = {
            "channel": self._get_channel_id(channel_name),
            "ts": ts
        }
        r = self._get_response(url, di_opt)
        return json.loads(r.text) if r else {'messages':[]}

    def get_all_msg_and_replies(self, channel_name, pagenation_limit=2, cursor=None):
        """
        [
            [{...}], - msg w/o reply
            [{},{},...], - msg w/ reply
        ...]
        """
        li = []
        itr = self.get_all_conv_hist(channel_name, pagenation_limit, cursor)
        # for row in self.get_conversation_hist(channel_name):
        for i, row in enumerate(itr):
            print(f"processing {i} out of {len(itr)}")
            try:
                get_success = False
                res = self._get_replies(channel_name, row['ts'])
                get_success = True
                li.append(res['messages'])
            except:
                err = f'get_success:{get_success} - err at {res}' if get_success else f'get_success:{get_success} - err at {row["ts"]}'
                print(err)
                if get_success and res['error'] == "ratelimited":
                    print('retry after 1 min')
                    sleep(61)
                    try:
                        res = self._get_replies(channel_name, row['ts'])
                        li.append(res['messages'])
                        print('recover success')
                    except:
                        print('failed again')
                        pass

        return li

    def get_replies(self, channel_name, di_msg):
        """
        [
            {...}, - di_msg
        ...]
        :param di_msg: same as get_conversation_hist
        """
        return self._get_replies(channel_name, di_msg['ts'])['messages']

    def get_user_name_from_id(self, user_id):
        """
        dict_keys(['id', 'team_id', 'name', 'deleted', 'color', 'real_name', 'tz', 'tz_label', 'tz_offset', 'profile', 'is_admin', 'is_owner', 'is_primary_owner', 'is_restricted', 'is_ultra_restricted', 'is_bot', 'is_app_user', 'updated', 'is_email_confirmed', 'has_2fa', 'who_can_share_contact_card'])
        """
        url = self.core_url + 'users.info'
        di_opt = {"user": user_id}
        r = self._get_response(url, di_opt)
        return json.loads(r.text)['user']['name'] if r else "NA"

    def get_token_user_info(self, di_opt=None):
        """
            ok -> True
            user -> {'name': 'Takaakira Yamauchi', 'id': 'UTR2SJYDD'}
            team -> {'id': 'TGJ8HQA69'}
        """
        url = self.core_url + 'users.identity'
        r = self._get_response(url, di_opt)
        return json.loads(r.text) if r else {}

    def publish_message(self, channel, msg, user=None):
        '''
        POST https://slack.com/api/chat.postMessage
        Content-type: application/json
        Authorization: Bearer xoxb-your-token
        {
          "channel": "YOUR_CHANNEL_ID",
          "text": "Hello world :tada:"
        }
        '''
        url = self.core_url + 'chat.postMessage'
        di_opt = {
            "channel": channel,
            "text": msg
        }
        if user:
            di_opt['username'] = user
        r = self._post_request(url, di_opt)
        return r

    def reply_to_msg(self, channel, reply_msg_txt, ts, user=None):
        '''
        POST https://slack.com/api/chat.postMessage
        Content-type: application/json
        Authorization: Bearer xoxb-your-token
        {
          "channel": "YOUR_CHANNEL_ID",
          "thread_ts": "PARENT_MESSAGE_TS",
          "text": "Hello again!"
        }
        '''
        url = self.core_url + 'chat.postMessage'
        di_opt = {
            "channel": channel,
            "text": reply_msg_txt,
            "thread_ts": ts
        }
        if user:
            di_opt['username'] = user
        r = self._post_request(url, di_opt)
        return r



