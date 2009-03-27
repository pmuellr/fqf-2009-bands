#!/usr/bin/env python

import os
import sys
import re
import time

re_entry = re.compile(r"^(\d{2}):(\d{2}) - (\d{2}):(\d{2}) (.*?)(http\S*)?$")

ifile_name = "2009-fqf-bands.txt"

ifile = open(ifile_name, "r")
lines = ifile.readlines()
ifile.close()

id = 0
for line in lines:
    line = line.rstrip()

    # a new block
    match = re_entry.match(line)
    if not match:
        print line
        continue
    
    line = "%02.2x %s" % (id,line)
    print line
    
    id += 1