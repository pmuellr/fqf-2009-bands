#!/usr/bin/env python

import os
import sys
import re

ifile_name = os.path.expanduser("~/Documents/2009-fqf-bands.txt")
ifile = open(ifile_name, "r")
lines = ifile.readlines()
ifile.close()

re_day   = re.compile(r"^\S.*day$")
re_entry = re.compile(r"^(\d{2}):(\d{2}) - (\d{2}):(\d{2}) (.*?)(http\S*)?$")
re_color = re.compile(r"^\*color/s*(/S{3})$")
re_color = re.compile(r"^\*color(.*)$")

color    = "FFF"
in_block = False

for line in lines:
	line = line.rstrip()
	
	if line == "": 
		if in_block:
			in_block = False
			print "</div>"
			print
			continue
		
		print line
		continue

	if re_day.match(line):
		print "<h1>%s</h1>" % line
		continue

	match = re_color.match(line)
	if match:
		color = match.group(1).strip()
		continue
		
	match = re_entry.match(line)
	if match:
		time1 = "%s:%s" % (match.group(1), match.group(2))
		time2 = "%s:%s" % (match.group(3), match.group(4))
		name  = match.group(5).strip()
		url   = match.group(6)
		
		if url:
			print "%s to %s <a href='%s'>%s</a><br>" % (time1, time2, url, name)
		else:
			print "%s to %s %s<br>" % (time1, time2, name)
		
		continue

	in_block = True		
	print "<div style='background-color: #%s'>" % color
	print "<h2>%s</h2>" % line

if in_block:
	print "</div>"