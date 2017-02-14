#!/usr/bin/env python

import os
import sys

import unicodedata
from OTXv2 import OTXv2
from datetime import datetime, timedelta
import IndicatorTypes

# Add your own OTX API key within the quotes on the next line.
otx = OTXv2("")

# This is the file where the hashes are stored.
# If you change this, remember to change the Perl script as well.
hash_file = '/var/tmp/known_hashes.txt'

# Todo: Make the number of days a variable.


# --- You should not need to edit anything below here. ---
mtime = (datetime.now() - timedelta(days=31)).isoformat()

hash_list = []

for pulse in otx.getsince(mtime):
    pulse_id = pulse['id']
    for indicator in pulse["indicators"]:
        type_ = indicator["type"]
        if type_ == IndicatorTypes.FILE_HASH_MD5.name:
            string='{MD5}:'+indicator["indicator"]+':'+pulse['id']
            hash_list.append(string)
        if type_ == IndicatorTypes.FILE_HASH_SHA1.name:
            string='{SHA1}:'+indicator["indicator"]+':'+pulse['id']
            hash_list.append(string)

f = open(hash_file, 'w')
for hash in hash_list:
    f.write("{0}\n".format(hash))
f.close()

