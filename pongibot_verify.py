from __future__ import print_function

import json
import os

def lambda_handler(event, context):
    print(event)
    mode = event.get('hub.mode', '')
    token = event.get('hub.verify_token', '')
    os_token = os.environ["VERIFY_TOKEN"]
    chg = event.get('hub.challenge', '')
    
    if mode == 'subscribe' and token == os_token:
        return chg    
    else:
        return 'Invalid Validation'

