#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import requests

from config import *

def args():
    parser   = argparse.ArgumentParser(description="Wrapper for Monzo API requests.")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = args()
    
    REFRESH_TOKEN = open('.refresh_token').read()

    data = {'grant_type': 'refresh_token', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'refresh_token': REFRESH_TOKEN}
    request = requests.post(f'https://api.monzo.com/oauth2/token', data=data)
    
    response = request.json()
    print(response)

    access_token  = response['access_token']
    refresh_token = response['refresh_token']

    open('.access_token', 'w+').write('Bearer ' + access_token)
    open('.refresh_token', 'w+').write(refresh_token)