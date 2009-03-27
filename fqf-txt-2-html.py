#!/usr/bin/env python

#--------------------------------------------------------------------
# program to generate nice HTML from a text file containing band
# information for the 2009 French Quarter Festival
#--------------------------------------------------------------------
# maintained at http://github.com/pmuellr/fqf-2009-bands/tree/master
#--------------------------------------------------------------------

#--------------------------------------------------------------------
#            DO WHAT THE F*CK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004 
#
# Copyright (C) 2009 Patrick Mueller
#
# Everyone is permitted to copy and distribute verbatim or modified 
# copies of this license document, and changing it is allowed as long 
# as the name is changed. 
#
#            DO WHAT THE F*CK YOU WANT TO PUBLIC LICENSE 
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#  0. You just DO WHAT THE F*CK YOU WANT TO. 
#--------------------------------------------------------------------

import os
import sys
import re
import time

#--------------------------------------------------------------------
#  globals
#--------------------------------------------------------------------
time_start = 11
time_stop  =  9

#--------------------------------------------------------------------
# convert an hours number to something nicer for print
#--------------------------------------------------------------------
def hour_to_print(hour):
    hour = hour % 12
    if not hour: hour = 12
    
    if hour == 12:
        return "noon"
    elif hour > 10:
        return "%dam" % hour
    else:
        return "%dpm" % hour

#--------------------------------------------------------------------
# convert hh:mm to a unit measurement based on: 
#    12 units/hour, starting at some time_start hour value
#--------------------------------------------------------------------
def time_to_units(hh, mm):
    return ((hh - time_start) * 12 ) + (mm / 5)
        
#--------------------------------------------------------------------
# model a set of blocks
#--------------------------------------------------------------------
class Day:

    #----------------------------------------------------------------
    # constructor
    #----------------------------------------------------------------
    def __init__(self, name):
        self.name    = name
        self.blocks  = []
    
    #----------------------------------------------------------------
    # add a block to the day
    #----------------------------------------------------------------
    def add_block(self, block):
        self.blocks.append(block)
        return self
        
    #----------------------------------------------------------------
    # return the list of blocks
    #----------------------------------------------------------------
    def get_blocks(self):
        return self.blocks[:]
        
#--------------------------------------------------------------------
# model a block of entries
#--------------------------------------------------------------------
class Block:

    #----------------------------------------------------------------
    # constructor
    #----------------------------------------------------------------
    def __init__(self, name, color):
        self.name    = name
        self.color   = color
        self.entries = []

    #----------------------------------------------------------------
    # add an entry to a block
    #----------------------------------------------------------------
    def add_entry(self, entry):
        self.entries.append(entry)
        return self
        
    #----------------------------------------------------------------
    # return the list of entries
    #----------------------------------------------------------------
    def get_entries(self):
        return self.entries[:]
        
    #----------------------------------------------------------------
    # convert a block into HTML as a <tr>
    #----------------------------------------------------------------
    def to_html_tr(self, ofile):
        print >>ofile, "<tr>"
        print >>ofile, "<td class='table_header' align='center' style='background-color: #%s' class='round-rect entry'>%s</td><td class='clear'></td>" % (self.color, self.name)
        
        entries = self.get_entries()
        
        if entries[0].units_start != 0:
            cols = entries[0].units_start
            print >> ofile, "<td colspan='%d' class='clear'></td>" % cols
        
        
        for i, entry in enumerate(entries):
            cols = entry.units_stop - entry.units_start
            time = "%02.2d:%02.2d-%02.2d:%02.2d" % (entry.hh1,entry.mm1,entry.hh2,entry.mm2)
            if entry.descr:
                descr = 'title="%s - %s"' % (time, entry.descr.replace('"',"&quot;"))
            else:
                descr = ""
                
            print >>ofile, "<td %s colspan='%d' align='center' style='background-color: #%s' class='round-rect entry'>" % (descr, cols, self.color),
            entry.to_html(ofile, self.color)
            print >>ofile, "</td>"

            if i < len(entries) - 1:
                units_empty = entries[i+1].units_start - entry.units_stop
                if units_empty > 0:
                    print >>ofile, "<td colspan='%d' class='clear'></td>" % units_empty
            
        print >>ofile, "</tr>"
        
    #----------------------------------------------------------------
    # convert a block into HTML
    #----------------------------------------------------------------
    def to_html(self, ofile):
    
        print >>ofile, "<div style='background-color: #%s'>" % self.color
        print >>ofile, "<h2>%s</h2>" % self.name
        
        for entry in self.get_entries():
            entry.to_html(ofile)
            print >>ofile, ""
            
        print >>ofile, "</div>"
        print >>ofile

#--------------------------------------------------------------------
# model a single entry in a block of entries
#--------------------------------------------------------------------
class Entry:

    #----------------------------------------------------------------
    # constructor
    #----------------------------------------------------------------
    def __init__(self, id, hh1, mm1, hh2, mm2, name, link):
    
        self.id    = id
        self.hh1   = int(hh1.strip())
        self.mm1   = int(mm1.strip())
        self.hh2   = int(hh2.strip())
        self.mm2   = int(mm2.strip())
        self.name  = name.strip()
        self.link  = link
        self.descr = None
        
        if self.hh1 < 10: self.hh1 += 12
        if self.hh2 < 10: self.hh2 += 12
        
        self.units_start  = time_to_units(self.hh1, self.mm1)
        self.units_stop   = time_to_units(self.hh2, self.mm2)
        self.units_length = self.units_stop - self.units_start 
        
        if self.link: self.link = self.link.strip()
        
    #----------------------------------------------------------------
    # convert an entry into HTML
    #----------------------------------------------------------------
    def to_html(self, ofile, color):
        fav_link = "<a style='text-decoration:none' href='javascript:toggle_favorite_entry(\"%s\")'><span class='heart' id='%s-c' style='color:#fff''>&#9825;</span></a>" % (self.id, self.id)
        if self.link:
#           print >>ofile, "<span class='entry'><a target='fqf-band' href='%s'>%s</a></span>" % (self.link, self.name),
            print >>ofile, "%s <a href='%s'>%s</a>" % (fav_link, self.link, self.name),
            return
            
        print >>ofile, "%s %s" % (fav_link, self.name),

#--------------------------------------------------------------------
# main program
#--------------------------------------------------------------------

units_stop = time_to_units(9,0)
        
#--------------------------------------------------------------------
# read the input file
#--------------------------------------------------------------------
ifile_name = "2009-fqf-bands.txt"
ofile_name = "2009-fqf-bands.html"

ifile = open(ifile_name, "r")
lines = ifile.readlines()
ifile.close()

re_day   = re.compile(r"^\S.*day$")
re_entry = re.compile(r"^(\S{2}) (\d{2}):(\d{2}) - (\d{2}):(\d{2}) (.*?)(http\S*)?$")
re_color = re.compile(r"^\*color(.*)$")
re_descr = re.compile(r"^=(.*)$")

color    = "FFF"
days = []
day   = None
block = None
for line in lines:
    line = line.rstrip()

    # empty line    
    if line == "": 
        block = None
        continue

    # color command
    match = re_color.match(line)
    if match:
        color = match.group(1).strip()
        continue
        
    # a new day
    if re_day.match(line):
        day = Day(line)
        days.append(day)
        continue

    # a new entry description
    match = re_descr.match(line)
    if match:
        descr = match.group(1).strip()
        if descr != "": entry.descr = match.group(1)
        continue
        
    # a new block
    match = re_entry.match(line)
    if not match:
        block = Block(line, color)
        day.add_block(block)
        continue
    
    # a new entry
    id   = match.group(1)
    hh1  = match.group(2)
    mm1  = match.group(3)
    hh2  = match.group(4)
    mm2  = match.group(5)
    name = match.group(6)
    link = match.group(7)
    
    entry = Entry(id, hh1, mm1, hh2, mm2, name, link)
    block.add_entry(entry)
        
#--------------------------------------------------------------------
# write the output
#--------------------------------------------------------------------
ofile = open(ofile_name, "w")

#--------------------------------------------------------------------
# things run from 11 - 9, 10 total hours
# 5 minute increments, 12 increments per hour
# 10 hours * 12 increments per hour = 120 total increments
#--------------------------------------------------------------------

blocks_per_table = 8

program_name = os.path.basename(sys.argv[0])

#--------------------------------------------------------------------
# comment to go at the beginning of the output file
#--------------------------------------------------------------------
html_comment = """<!--
generated by %s on %s
-->""" % (program_name, time.asctime())

#--------------------------------------------------------------------
# header of the output file
#--------------------------------------------------------------------
html_header = """
<html>
<head>
<title>2009 French Quarter Festival Bands</title>
<style type="text/css">
h1 {
    margin-top:    0em;
    margin-bottom: 0em;
}
.table_header {
    font-weight: bold;
    font-size:   120%;
}
.clear {
   background-color: #FFF;
}
.day_div {
    border-width:          4;
    border-style:          solid;
    margin:                1em;
    padding:               1em;
    -moz-border-radius:    10px;
    -webkit-border-radius: 10px;
    page-break-before:     always;
}
.entry {
    font-weight: bold;
    font-size:   90%;
}
.round-rect {
    -moz-border-radius:    10px;
    -webkit-border-radius: 10px;
    border:                0px solid #000;
    padding-top:           3px;
    padding-bottom:        3px;
}
:link {
    color: #000;
}
:visited {
    color: #000;
}
:hover {
    color: #000;
    text-shadow: #AA0 0.2em 0.2em 0.2em;
}
</style>
<script src="jquery-1.3.2.min.js" type="text/javascript"></script>
<script type="text/javascript">

var search_text      = null
var favorites_toggle = null

function search_filter(index) {
    if (!this.title) return false
    var title = this.title.toUpperCase()
    if (-1 != title.indexOf(search_text)) return true
    var content = $(this).text().toUpperCase()
    return -1 != content.indexOf(search_text)
}

function is_hearted(index) {
    var char = this.innerHTML 
    return char == "\u2665"
}

function favorite_toggled() {
    if (favorites_toggle.val().length == 0) {
        $(".entry").css("opacity", "1.0").css("-moz-opacity", "1.0")
        $("#selected-count").html("All")
        return
    }
    
    $(".entry").css("opacity", "0.2").css("-moz-opacity", "0.2")
    var selected = $(".heart").filter(is_hearted).parent().parent().css("opacity", "1.0").css("-moz-opacity", "1.0").size()
    $("#selected-count").html("" + selected)
}

$(document).ready(function() {
    favorites_toggle = $("#favorites-toggle")
    favorites_toggle.click(favorite_toggled)
    
    var search_box = $("#search-box")
    
    search_box.keyup(function() {
        search_text = search_box.val().toUpperCase()
        
        if (search_text == "") {
            // opacity: -moz-opacity:
            $(".entry").css("opacity", "1.0").css("-moz-opacity", "1.0")
            $("#selected-count").html("All")
        }
        else {
            favorites_toggle.val([])
            $(".entry").css("opacity", "0.2").css("-moz-opacity", "0.2")
            var selected = $(".entry").filter(search_filter).css("opacity", "1.0").css("-moz-opacity", "1.0").size()
            $("#selected-count").html("" + selected)
        }
    })
})

function toggle_favorite_entry(id) {
    var element = $("#" + id + "-c")
    var c = element.html()
    if (c == "\u2661") {
        element.html("\u2665")
    }
    else {
        element.html("\u2661")
    }
    favorite_toggled()
}

</script>
</head>
<body>
<div class="day_div">
<h1>2009 French Quarter Festival Bands</h1>
<p>The 'Official' French Quarter Festival site here:
<tt><b><a href="http://www.fqfi.org/frenchquarterfest/">http://www.fqfi.org/frenchquarterfest/</a></b></tt>
<p>Search: <input id="search-box" type="text" size="20"">
<input id='favorites-toggle' type="checkbox"> Only show favorites<br>
Selected: <span id='selected-count'>All</span></p>
</div>
<div class="day_div">
<span style='color:#D00; font-size:200%'><b>Favorites are not currently remembered!</b></span>
</div>

"""

#--------------------------------------------------------------------
# trailer of the output file
#--------------------------------------------------------------------
html_trailer = """
<div class="day_div">
Generated on %s using 
<a href="fqf-txt-2-html.py"><tt><b>fqf-txt-2-html.py</b></tt></a>
using data file
<a href="2009-fqf-bands.txt"><tt><b>2009-fqf-bands.txt</b></tt></a>,
all of which is maintained at
<a href="http://github.com/pmuellr/fqf-2009-bands/tree/master">GitHub</a>.
</div>
</body>
</html>
""" % (time.asctime())

#--------------------------------------------------------------------
# write the comment and header
#--------------------------------------------------------------------
print >>ofile, html_comment
print >>ofile, html_header

#--------------------------------------------------------------------
# write each day
#--------------------------------------------------------------------
for day in days:
    print >>ofile, ""
    print >>ofile, "<div class='day_div'>"
    print >>ofile, "<h1>%s</h1>" % day.name
    print >>ofile, "<hr>"
    print >>ofile, "<table cellpadding='2' cellspacing='1'>"
    
    size_line = "<tr><td width='20%'></td>"
    for i in xrange(0, 120):
        size_line += "<td width='0.8%'></td>"
    size_line += "</tr>"
    
    date_line = "<tr><td width='20%'></td>"
    for i in xrange(time_start, time_stop + 12):
        date_line += "<td width='8%%'colspan='12'><span style='color:#00F'>|</span> %s</td>" % hour_to_print(i)
    date_line += "</tr>"
    
    print >>ofile, size_line
    blocks = day.get_blocks()
    for i, block  in  enumerate(blocks):
        if not i % 4: print >>ofile, date_line
        block.to_html_tr(ofile)
        
    print >>ofile, "</table>"
    print >>ofile, "</div>"

#--------------------------------------------------------------------
# write the trailer and close
#--------------------------------------------------------------------
print >>ofile, html_trailer
        
ofile.close()