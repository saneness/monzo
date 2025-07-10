#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import requests
import json
import os
import time
from currency_converter import CurrencyConverter

from config import *

def args():
    parser   = argparse.ArgumentParser(description="Wrapper for Monzo API requests.")
    parser.add_argument("-c", "--convert", metavar="\b", default="JPY", help="Additional currency to convert to. (default: JPY)")
    args = parser.parse_args()
    return args

def send_message(text):
    for chat_id in CHAT_IDS:
        data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": 'markdown', "disable_notification": True})
        cmd = f"curl -X POST 'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage' -H 'Content-Type: application/json' -d '{data}'"
        os.system(cmd)
        time.sleep(1)

if __name__ == '__main__':
    args = args()
    
    ACCESS_TOKEN = open('.access_token').read()
    ACCOUNT_ID   = open('.account_id').read()

    headers = {'Authorization': ACCESS_TOKEN}
    request = requests.get(f'https://api.monzo.com/pots?current_account_id={ACCOUNT_ID}', headers=headers)
    balance = int([item for item in request.json()['pots'] if item['has_virtual_cards']][0]['balance'])/100.0
    if args.convert in ["JPY"]:
        converted = int(round(CurrencyConverter().convert(balance, 'GBP', f'{args.convert}'), 0))
    else:
        converted = round(CurrencyConverter().convert(balance, 'GBP', f'{args.convert}'), 2)
    new_balance_gbp = f'{balance}'
    new_balance_con = f'{converted}'

    try:
        old_balance_gbp = open(POT_PATH).read().strip().split()[0]
        old_balance_con = open(POT_PATH).read().strip().split()[2][1:]
        if new_balance_gbp != old_balance_gbp:
            open(POT_PATH, 'w+').write(f'{new_balance_gbp} GBP ({new_balance_con} {args.convert})')
            send_message(f"`GBP: {old_balance_gbp} -> {new_balance_gbp}`\n`{args.convert}: {old_balance_con} -> {new_balance_con}`")
    except:
        new_balance = f'{new_balance_gbp} GBP ({new_balance_con} {args.convert})'
        open(POT_PATH, 'w+').write(new_balance)
