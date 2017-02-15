#!/usr/bin/env python

import argparse
import os
import sys

import unicodedata
from OTXv2 import OTXv2
from datetime import datetime, timedelta
import IndicatorTypes


# This is the file where the hashes are stored.
# If you change this, remember to change the Perl script as well.
hash_file = '/var/tmp/known_hashes.txt'

# --- You should not need to edit anything below here. ---

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True,help="Your OTX API key (https://otx.alienvault.com/api)")
    parser.add_argument("--days", required=False,type=int,default=14,help="Data age (in days)")
    parser.add_argument("--destination-directory", "-dd", required=False, type=argparse.FileType('w'),
                        help="The destination directory for the generated file")
    return parser.parse_args()

args = getArgs()
otx = OTXv2(api_key=args.key)
mtime = (datetime.now() - timedelta(days=args.days)).isoformat()

hash_list = []

for pulse in otx.getsince(mtime):
    pulse_id = pulse['id']
    for indicator in pulse["indicators"]:
        type_ = indicator["type"]
        if type_ == IndicatorTypes.FILE_HASH_MD5.name:
            string='MD5:'+indicator["indicator"]+':'+pulse['id']
            hash_list.append(string)
        if type_ == IndicatorTypes.FILE_HASH_SHA1.name:
            string='SHA1:'+indicator["indicator"]+':'+pulse['id']
            hash_list.append(string)

f = open(hash_file, 'w')
for hash in hash_list:
    f.write("{0}\n".format(hash))
f.close()

