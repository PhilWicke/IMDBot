#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:15:04 2016

This is the simplified imdplotbot script for a web-server.
It will take the latest batch of generated plots from the offline plotbot.

@author: Wicke
"""

import glob, datetime, os, sys, plotBotLib

# Constants
prefix = 'BotOutput'
suffix = '.txt'

# Scan the plot updates
files = glob.glob(prefix+'*') 
dates = []

for file in files:
    date = file.replace(prefix,"")
    date = date.replace(suffix,"")
    dates.append(datetime.datetime.strptime(date, '%Y-%m-%d'))

# and seek the latest file
now     = datetime.datetime.now()
latest  = max(dt for dt in dates if dt < now)
latest  = datetime.datetime.strftime(latest, '%Y-%m-%d')

curr_file = prefix+latest+suffix

# Open the latest archive
if not(os.path.exists(curr_file)):
    raise ValueError('Something went terribly wrong!')

# Read all plots from current txt file
with open(curr_file, 'r+',encoding='utf8') as f_txt:
    content = f_txt.readlines()
    
# Clear content from "dot" fragments (some plots add a DOT, as they end on a "?"/"!")
while ".\n" in content:
    content.remove(".\n")
    
# if there is no further content that could be tweeted, end yourself.
if not content:
    plotBotLib.alertMail(0)
    sys.exit()

# if there are less then 5 plots available, send an alert Mail
status = len(content)
if status <= 6:
    plotBotLib.alertMail(status)

# write all plots into txt file except the one you will tweet
with open(curr_file, 'w',encoding='utf8') as f_txt:
    for idx in range(1,len(content)):
        f_txt.write(content[idx])

# tweet the current plot on twitter
plotBotLib.tweet(content[0])


        



