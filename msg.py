#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

import argparse
import requests
import json
import os
import time
import traceback
from forex_python.converter import CurrencyRates

from config import *

def send_message(text):
    for chat_id in CHAT_IDS:
        data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": 'markdown', "disable_notification": True})
        cmd = f"curl -X POST 'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage' -H 'Content-Type: application/json' -d '{data}'"
        os.system(cmd)
        time.sleep(1)

if __name__ == '__main__':
    message = open("msg").read()
    send_message(message)
