#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import argparse
import re
import requests
import json


def translate(lang='  DE', text=None):
    """
    takes text, as a string, tries to detect the language and uses DEEPL inofficial API to translate it
    """

    ### TODO: try to detect language
    lang = None

    if not lang:
        lang = 'DE'

    sp = re.compile("([^\.!\?;]+[\.!\?;]*)")
    sentences = [s for s in sp.split(text) if len(s) > 0]

    payload = {
        "jsonrpc": "2.0", "method": "LMT_handle_jobs", "id": 1,
        "params": {
            "jobs": [{"kind": "default", "raw_en_sentence": s} for s in sentences],
            "lang": {"user_preferred_langs": ["EN", "DE"],
                     "source_lang_user_selected": "auto",
                     "target_lang": lang},
            "priority": 1}}


    r = requests.post('https://deepl.com/jsonrpc', data=json.dumps(payload))
    translations = json.loads(r.text)['result']['translations']
    for translation in translations:
        print(sorted(translation['beams'], key=lambda b: -1 * b['score'])[0]['postprocessed_sentence'], end=" ")

    print()
    return translations

if __name__ == '__main__':
    text = translate(text = 'mal schauen, was denn da passiert? wenn man das einfach so probiert! vielleicht kommt dabei ja etwas heraus.')
    print(text)

    for beam in text:
        print(beam)
        for proposed in beam['beams']:
            print(proposed)