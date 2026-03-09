#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import requests
import json
import os
import time
import traceback
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

    SYMBOL = {
        "GBP": "£",
        "JPY": "¥"
    }

    FORMAT = {
        "GBP": ".2f",
        "JPY": ".0f"
    }
    
    ACCESS_TOKEN = open('.access_token').read().strip()
    ACCOUNT_ID   = open('.account_id').read().strip()

    headers = {'Authorization': ACCESS_TOKEN}
    request = requests.get(f'https://api.monzo.com/pots?current_account_id={ACCOUNT_ID}', headers=headers)
    if 'code' in request.json():
        print(f"Request code: {request.json()['code']}")
    try:
        balance = int([item for item in request.json()['pots'] if item['has_virtual_cards']][0]['balance'])/100.0
        if os.path.exists(POT_PATH_ERROR):
            os.remove(POT_PATH_ERROR)
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
                balance_change_gbp = float(new_balance_gbp)-float(old_balance_gbp)
                balance_change_con = float(new_balance_con)-float(old_balance_con)
                balance_change_sign_gbp = '+' if balance_change_gbp > 0 else '-'
                balance_change_sign_con = '+' if balance_change_con > 0 else '-'
                send_message(f"`New balance:`\n`{SYMBOL['GBP']}{new_balance_gbp} ({balance_change_sign_gbp}{SYMBOL['GBP']}{abs(balance_change_gbp):{FORMAT['GBP']}})`\n`{SYMBOL[args.convert]}{new_balance_con} ({balance_change_sign_con}{SYMBOL[args.convert]}{abs(balance_change_con):{FORMAT[args.convert]}})`")
                open(POT_PATH, 'w+').write(f'{new_balance_gbp} GBP ({new_balance_con} {args.convert})')
        except:
            new_balance = f'{new_balance_gbp} GBP ({new_balance_con} {args.convert})'
            open(POT_PATH, 'w+').write(new_balance)
    except Exception as e:
        traceback.print_exc()
        open(POT_PATH_ERROR, 'w+').write('ERROR')
