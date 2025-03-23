#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import requests
from currency_converter import CurrencyConverter

def args():
    parser   = argparse.ArgumentParser(description="Wrapper for Monzo API requests.")
    parser.add_argument("-c", "--convert", metavar="\b", default="JPY", help="Additional currency to convert to. (default: JPY)")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = args()
    
    ACCESS_TOKEN = open('.access_token').read()
    ACCOUNT_ID   = open('.account_id').read()

    headers = {'Authorization': ACCESS_TOKEN}
    request = requests.get(f'https://api.monzo.com/pots?current_account_id={ACCOUNT_ID}', headers=headers)
    balance = int([item for item in request.json()['pots'] if item['has_virtual_cards'] == True][0]['balance'])/100.0
    converted = round(CurrencyConverter().convert(balance, 'GBP', f'{args.convert}'), 2)
    print(f'{balance} GBP ({converted} {args.convert})')
