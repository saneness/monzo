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
    
    auth = f'https://auth.monzo.com/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&state={STATE_TOKEN}'
    print(auth)

    AUTH_CODE = open('.auth_code').read()
    token = f'http --form POST "https://api.monzo.com/oauth2/token" "grant_type=authorization_code" "client_id={CLIENT_ID}" "client_secret={CLIENT_SECRET}" "redirect_uri={REDIRECT_URI}" "code={AUTH_CODE}"'
    print(token)