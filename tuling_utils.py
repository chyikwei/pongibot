from __future__ import print_function

import requests
from hanziconv import HanziConv

TULING_123_URL = "http://www.tuling123.com/openapi/api"
TIMEOUT = 10.0

def send_reuqest(user_id, req_text, api_key):

    req_data = {
        "key": api_key,
        "info": HanziConv.toSimplified(req_text),
        #"loc": ""
        "userid": user_id
    }

    ret_data = {
        "success": False,
    }
    try:
        ret = requests.post(TULING_123_URL, data=req_data, timeout=TIMEOUT)
        if ret.status_code == 200:
            ret_data["success"] = True
            ret_data.update(ret.json())
            if 'text' in ret_data:
                txt = ret_data['text']
                ret_data['text'] = HanziConv.toTraditional(txt)
        else:
            print(ret.text)
    except requests.RequestException:
        pass

    return ret_data
