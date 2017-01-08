from __future__ import print_function

import os
import json
import requests
from tuling_utils import send_reuqest

FB_POST_URL = "https://graph.facebook.com/v2.8/me/messages"

# TODO: will be replaced later
TEST_USER_ID = "123456"

DEFAULT_RESPONSE = "I don't understand... QQ"


def send_message(recipient_id, message_text):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    r = requests.post(FB_POST_URL,
                      params=params,
                      headers=headers,
                      data=data)
    
    if r.status_code != 200:
        print('post Failed: {}'.format(r.text))


def tuling_response_wrapper(user_id, req_text):
    ret = send_reuqest(user_id, req_text, os.environ['TULING_APIKEY'])
    if ret['success']:
        res_text = ret.get('text', u"no ret text for %r" % req_text)
    else:
        res_text = DEFAULT_RESPONSE
    return res_text


def lambda_handler(event, context):
    print(event)

    body = event.get('body', {})
    if not body:
        return {"success": False}

    ret = True
    if body['object'] == 'page':
        for entry in body['entry']:
            for msg in entry.get('messaging', []):
                msg_txt = msg['message']['text']
                sender_id = msg['sender']['id']
                res_text = tuling_response_wrapper(TEST_USER_ID, msg_txt)
                send_message(sender_id, res_text)
    
    return {"success": ret}

