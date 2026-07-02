#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import os
import requests
import traceback
from forex_python.converter import CurrencyRates

from config import *

def args():
    parser   = argparse.ArgumentParser(description="Wrapper for currency rates.")
    parser.add_argument("-b", "--base", metavar="\b", default="GBP", help="Base currency to convert from. (default: GBP)")
    parser.add_argument("-c", "--convert", metavar="\b", default="JPY", help="Additional currency to convert to. (default: JPY)")
    args = parser.parse_args()
    return args

def forex(base, convert):
    return CurrencyRates().get_rate(base, convert)

def currencyapi(base, convert):
    rates = requests.get(f'https://currencyapi.net/api/v2/rates?base=USD&output=json&key={CURRENCYAPI_KEY}').json()['rates']
    return rates[convert] / rates[base]

if __name__ == '__main__':
    args = args()

    try:
        rate = currencyapi(base=args.base, convert=args.convert)
        if os.path.exists(RATE_PATH_ERROR):
            os.remove(RATE_PATH_ERROR)
        open(f'{RATE_PATH}', 'w+').write(f'{rate:.2f}')
    except Exception as e:
        traceback.print_exc()
        open(RATE_PATH_ERROR, 'w+').write('ERROR')
