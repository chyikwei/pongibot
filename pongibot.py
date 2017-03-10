#!/usr/bin/python
 # -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import json
import requests
from tuling_utils import send_reuqest

FB_POST_URL = "https://graph.facebook.com/v2.8/me/messages"

# TODO: will be replaced later
TEST_USER_ID = "123456"

DEFAULT_RESPONSE = "I don't understand... QQ"

NUMBER_RESPONSE = {
    '1': u'1什麼1，鉛筆1',
    '2': u'2什麼2，鴨鴨2',
    '3': u'3什麼3，蝴蝶3',
    '4': u'4什麼4，帆船4',
    '5': u'5什麼5，鉤鉤5',
    '6': u'6什麼6，哨子6',
    '7': u'7什麼7，拐杖7',
    '8': u'8什麼8，眼鏡8',
    '9': u'9什麼9，氣球9',
    '10': u'10什麼10，一根棒子打棒球',
    'default': u"不會!!",
}

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


def number_response_handler(user_id, req_text):
    default = NUMBER_RESPONSE['default']
    return NUMBER_RESPONSE.get(req_text, default)


def response_dispatcher(req_text):
    if re.match(r'^\d+$', req_text):
        return number_response_handler
    else:
        return tuling_response_wrapper


def lambda_handler(event, context):
    print(event)

    body = event.get('body', {})
    if not body:
        return {"success": False}

    ret = True
    if body['object'] == 'page':
        for entry in body['entry']:
            for msg in entry.get('messaging', []):
                if 'delivery' in msg:
                    continue
                msg_txt = msg['message']['text']
                sender_id = msg['sender']['id']
                res_func = response_dispatcher(msg_txt)
                res_text = res_func(TEST_USER_ID, msg_txt)
                send_message(sender_id, res_text)
    
    return {"success": ret}

