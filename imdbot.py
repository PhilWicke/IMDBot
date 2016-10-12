# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:37:31 2015

This twitter bot will take the top 20 titles of imdb.com in order
to create new plots out of the given archives by combining them.

The newest plots will be fetched form imdb.com. Internally a bookmark.txt
file will keep track of the already used titles. 

@author: Wicke
"""
import imdpy, random
from sys import stdout

# Number of trials to combine plots in one run of the program / delay of tweets in seconds
trials = 100
delay  = 86400

# loot imdb for current top 250 titles and plots
print('Downloading imdb archives.')
imdpy.loot_imdb('plot')
imdpy.loot_imdb('ratings')

# unzip the downloaded files
imdpy.gzipper('plot.list.gz','plot.list')
imdpy.gzipper('ratings.list.gz','ratings.list')
print('Download of archives successful.')

# read the plots of top titles
top250      = imdpy.getTop250('ratings.list')
topTitles   = imdpy.syncTops(top250)
# now topTitles only includes titles which are not 'bookmarked as used' already
# add all new titles to 'bookmarks as used' as well

# TODO: Fix these plots!!!
if 'Casablanca (1942)' in topTitles: topTitles.remove('Casablanca (1942)')   
if 'Citizen Kane (1941)' in topTitles: topTitles.remove('Citizen Kane (1941)')
        
print('Starting creative process:')
for trial in range(trials):
    
    # Choose a random title of the synched database
    title01 = random.choice(topTitles)
    title02 = random.choice(topTitles)    
    while title02 == title01:
        title02 = random.choice(topTitles)
      
    # create a plot which is empty if both titles won't fit together
    ccPlot = imdpy.createPlot(title01,title02)
    
    if ccPlot:
        # if the two plots are to be used, remove them from topTitles pool
        # so you cannot draw them randomly anymore, bookmark that they have been used
        imdpy.bookmarkPlot(title01,title02, trial, ccPlot)
        topTitles.remove(title01)
        topTitles.remove(title02)
        
        # tweet the created plot and wait
        print(ccPlot)
		imdpy.tweet(ccPlot)   
		time.sleep(delay)
        
    progress = round((trial/trials)*100)
    stdout.write('\r%d%%' % progress)
    stdout.flush()
    if len(top250) <= 1:
        break
    
print('All current plots used to create more plots, try again later.')