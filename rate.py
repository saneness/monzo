#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import traceback
from forex_python.converter import CurrencyRates

from config import *

def args():
    parser   = argparse.ArgumentParser(description="Wrapper for Forex exchange rates.")
    parser.add_argument("-b", "--base", metavar="\b", default="GBP", help="Base currency to convert from. (default: GBP)")
    parser.add_argument("-c", "--convert", metavar="\b", default="JPY", help="Additional currency to convert to. (default: JPY)")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = args()

    try:
        rate = CurrencyRates().get_rate(f'{args.base}', f'{args.convert}')
        open(f'{RATE_PATH}', 'w+').write(f'{rate}')
    except Exception as e:
        traceback.print_exc()
        open(RATE_PATH_ERROR, 'w+').write('ERROR')
