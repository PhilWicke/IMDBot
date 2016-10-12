# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 00:24:36 2015

This module contains the functions for the imdb plot bot

@author: Wicke
"""


# load modules
from ftplib import FTP
import io, os, re, gzip, tweepy, datetime



def loot_imdb(data_string):
    """ 
    Fetch plot and rating data from imdb via *ftp.fu-berlin.de*. 
    The **string** you use as argument will download the corresponding list at imdb.com.
    Comlete list can be found at: *ftp://ftp.fu-berlin.de/pub/misc/movies/database/* \n
    Example arguments = what they create: \n
    Argument *plot* = **plot.list.gz** -- Containing all current plots on imdb \n
    Argument *ratings* = *ratings.list.gz** -- Containing all current ratings on imdb
    """
    ftp = FTP('ftp.fu-berlin.de')
    ftp.login()
    ftp.cwd('/pub/misc/movies/database/')
    
    file_name           = data_string + '.list.gz'
    local_file     = open(file_name, 'wb')     
    
    ftp.retrbinary('RETR ' + file_name, local_file.write)
    ftp.quit()
    
    local_file.close()
    print('\''+data_string+'.list.gz\' successfully downloaded.')
    
    
def gzipper(GzFileName,FileName):
    """ 
    Function that unzips a *.gz file \n
    Input: **GzFileName** -- the *.gz file name \n
    **FileName** -- name of the output file
    """
    with gzip.open(GzFileName, 'rb') as f_in:
        with open(FileName,'wb') as f_out:
            f_out.write(f_in.read())
    print(GzFileName+' unzipped to '+FileName)
            
            
def list2txt(listName):
    """
    Function that will transform a *.list file into a *.txt file \n
    Input: **listName** -- file you want to tranfer into **fileName**.txt    
    """
    max_size    = 10000000 #byte
    # aquire prefix name for txt file 
    txtName = listName.split('.list')[1]
    txtName = txtName + '.txt'
    
    with io.open(listName, 'r', encoding='latin-1') as l_in:
        with io.open(txtName, 'w', encoding='utf8') as l_out:
            for line in l_in:
                # aquire size of file to adjust threshold
                file_size = os.stat(txtName).st_size
                if file_size >= max_size : 
                    print('File converted to "%s." Size: %3.2f MB' % (txtName, file_size/1000000))
                    break
                else:
                    l_out.write(line)
           
def getTop250(ratings_file):
    """
    Function which extracts the top 250 titles out of the ratings.list \n
    *Input*: **ratings_file** -- the *ratings.list* file \n
    *Output*: **title_list** -- array with top 250 titles and corresp. dates
    """
    # Constants
    ratings         = ratings_file
    ratings250      = 'ratings250.list'
    
    # Extract 250 titles out of ratings and write into ratings250
    writingON = False;
    
    with io.open(ratings, 'r', encoding='latin-1') as rates:
        with io.open(ratings250, 'w', encoding='latin-1') as rates250:
            for line in rates:
                # The 'New' marks the start of the movie table
                if 'New' in line:
                    writingON = True;
                # Start writing if the top of table is reached
                if writingON:
                    rates250.write(line)
                # Stop writing if the bottom of the table is reached
                if 'BOTTOM' in line:
                    break
                
    # Look at lines which have a dot to extract title
    regexp  = re.compile("\.(.*)$")
    title_list = []
    
    with io.open(ratings250, 'r', encoding='latin-1') as rates250:
        for line in rates250:
            if regexp.search(line) is not None:
                # Divide the string at the dot and
                title_line = line.split(".",1);
                title_line = title_line[1].replace("\n","")
                # access the title which starts 3 chars after the dot
                title_list.append(title_line[3:]);
    
    return title_list
    
    
def getTop250Plots():
    """
    Function which extracts the top 250 plots out of the ratings250.list \n
    *Input*: **ratings250_file** -- the *ratings.list* file \n
    """
    # Constants
    ratings250 = getTop250('ratings.list')
    plots250        = 'plots250.list'
    
    with io.open(plots250, 'w', encoding='latin-1') as plots250:
        for title in ratings250:
            plots250.write(title)
            plots250.write(str(find_plot(title)))
            plots250.write('\n')
            
    
def find_plot(title):
    """
    Function to retrieve the plot, given title (date). Example:  \n
    ** find_plot ** ('The Silence of the Lambs (1991)') \n
    >> *Young FBI agent Clarice Starling is assigned to help* \n
    *find a missing woman to save her from a psychopathic serial...* \n 
    
    """
    # TODO: Plot 32: Casablanca
    # TODO: Plot 64: Citizen Kane
    
    # Writing flag and plot data field
    writeON     = False; 
    plot_line = [];
    
    with io.open('plot.list', 'r', encoding='latin-1') as plot:
        for line in plot:
            # start writing if title could be found
            if title in line and not('qv' in line) and not('VG' in line) and not ('TV' in line) and not('(V)' in line): # and not('TV' in line):
                writeON = True;
                # replace newline, title occurence and MV prefix
                line = line.replace("\n","")
                line = line.replace(title,"")
                line = line.replace("MV: ","")
                line = line.replace("PL: ","")
                plot_line = line
                
            # stop writing of end of plot is reached
            if 'BY:' in line:
                if writeON:
                    plot_line = plot_line + '\n' 
                writeON = False;
                
            # write next line if flag is set
            if writeON:
                line = line.replace("\n","")
                # replace prefix and print
                line = line.replace("MV: ","")
                line = line.replace("PL: "," ") # ,end="")#,flush=True)
                if not('qv' in line): 
                    plot_line = plot_line + line
                
    # return plot_line
    return plot_line
    
def allTopPlots(top250):
    """
    Small helper function \n
    *Input*: **top250** = *getTop250(ratings_file)* \n
    *Output*: **plots** = list of 250 plots
    """
    plots = []
    for title in top250:
        plots.append(find_plot(title))
    return plots

        
def rmvBookmark(title):
    """
    Small helper function to remove bookmarks from a *title* in the *bookmark.txt*.
    """
    bookmarks = open('bookmarks.txt', 'r+',encoding='utf8')
    data      = bookmarks.readlines()
    bookmarks.seek(0)
    
    for line in data:
        if line !=title+'\n':
            bookmarks.write(line)
            
    bookmarks.truncate()
    bookmarks.close()
        
def addBookmark(title):
    """
    Adds the title to the bookmark.txt file.
    """
    with open('bookmarks.txt', 'r+',encoding='utf8') as f_txt:
        # Go to last line of the file        
        for line in f_txt:
            pass
        f_txt.write(title)
        f_txt.write('\n')
        
   
def hasBookmark(title):
    """
    Function which returns *true* if the title has already been bookmarked, *false* if not.
    \n The file for the bookmarks is *bookmarks.txt*, which will be created on first use.
    """
    # Check if the bookmark file does exist, if not create one
    if not(os.path.exists('bookmarks.txt')):
        bookmarks = open('bookmarks.txt','w',encoding='utf8')
        bookmarks.close()
        print('Bookmark list did not exist and has been created.')
        print('This message should only appear at first use of bot!')
    #else:
        #print('Bookmark list found and has been openend.')
        
    # if title is already bookmarked, return 'False', else true and bookmark it
    with open('bookmarks.txt', 'r+',encoding='utf8') as f_txt:
        for line in f_txt:
            if title in line:
                return True
        
        # title not found in bookmark list, return false
        return False
     
def syncTops(topTitles):
    """
    Takes a list of titles and checks if they have already been bookmarked. If so
    the bookmarked titles will be deleted from the **topTitles** input and a synchronized
    list will be returned. \n
    *Input*: - **topTitles** = The list of titles you want to synchronize with 
    *bookmarks.txt* \n
    *Output*: - **syncList** = The updated synchronized list of new titles 
    """
    syncList = list(topTitles)    
    
    for title in range(len(topTitles)):
        tempTitle = topTitles[title]
    
        if hasBookmark(tempTitle):
            syncList.remove(tempTitle)
    return syncList
    
def bookmarkPlot(title01, title02, trial, plot):
    """
    Handling of internal registration of a plot. \n
    *Input*: **title01, title02, trial, plot** = information that will be stored in 
    the bookmark.txt file
    """
    addBookmark('##### Trial Nr.%d has combination:' % trial)
    addBookmark(title01)
    addBookmark(title02)
    addBookmark(plot)
    
def createPlot(title01,title02):
    """
    This is the creative function which takes two titles, finds their plots and merges them.
    \n
    Both plots will be chopped in parts by their sentences (using split('.')). 
    The first plot will act as head, the second as tail. I.e. starting with the first
    sentence of the head and the last sentence of the tail, they will be put together
    only if they have in total under 140 symbols (tweet sign limit) and minimally 20
    symbols (at least 10 each). \n
    
    *Input*: **title01, title02 ** = the titles of the plots you want to merge \n
    *Output*: **ccPlot** = the computationally created plot \n
    *"" empty string* = if the provided plots are incompatible
    
    """
    
    ccPlot = 'Empty'
    
    # head
    plot01      = find_plot(title01)
    plot01      = abbrev(plot01)
    parts       = plot01.split('.')
    parts01     = []
    # hashtag all sentences of first plot and check for empty parts or abbreviations
    for part in parts:      
        if not(part=="") and not(part==" ") and not(part=="\n"): 
            parts01 = parts01 + [hashtag(part)]
    
    #tail
    plot02      = find_plot(title02)
    plot02      = abbrev(plot02)
    parts       = plot02.split('.')
    parts02     = []
    # hashtag all sentences of second plot and check for empty parts or abbreviations
    for part in parts:      
        if not(part=="") and not(part==" ") and not(part=="\n"):            
            parts02 = parts02 + [hashtag(part)]
    
    # set trials
    try01 = 0
    try02 = len(parts02)-1
    
    # check if tweet boundary of 140 and a resonable lower bound is possible
    while len(ccPlot) > 140 or len(ccPlot) <= 10:
        
        # Check boundary for head and boundary for tail        
        if try01 == len(parts01): 
            # print('Incompatible plot segment length for tweet')
            return "" # if both plots won't fit under 140 chars, they are neglected
            
        
        head = parts01[try01] + '.'
        tail = parts02[try02] + '.'     
        ccPlot = head + tail
        
        # Check next sentence of head/tail of current head/tail is to large or small
        if len(ccPlot) > 140 or len(ccPlot) <= 10 or len(head) <= 10 or len(tail) <= 10:
            # Go form last to first sentence in tail
            try02 -= 1
            
            # if you've tested all sentences with tail, check with next head sentence
            # and start with last sentence of tail again
            if try02 < 0:
                try02 = len(parts02)-1  # last sentence of tail
                try01 += 1              # now take the next sentence of head
        else:
            return ccPlot

    return ccPlot   
    
def hashtag(plot):
    """
    Adds a hashtag to the longest word in the given sentence (here: plot). \n
    And returns the hashtagged sentence.
    """
    # find the longest word, by maximizing the split argument with key word 'len'
    idx_longest_word = plot.find(max(plot.split(),key=len))
    return plot[:idx_longest_word] + '#' + plot[idx_longest_word:]
      

def tweet(plot):
    """    
    This function tweets the current plot via the provided twitter account. \n
    *Input*: - **plot** of type *string* will be tweeted \n
    *Only tweets of maximal 140 characters can be tweeted*
    """    
    # Check length of tweet
    if len(plot) > 140:
        plot('Maximum tweet limit of 140 symbols reached!')
        plot('This should not have happened')
        raise Exception('Ooops, something went wrong.')
    
    # at apps.twitter.com -> my applications -> Keys and Access Tokens
    CONSUMER_KEY = 'your_consumer_key'
    CONSUMER_SECRET = 'your_consumer_secret'
    ACCESS_KEY = 'your_access_key'
    ACCESS_SECRET = 'your_access_secret'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    # do the actual tweet
    api.update_status(status=plot)
    
def abbrev(text):
    """
    Takes a string and removes all misleading DOTS belonging to abbreviations.
    """    
    regex1  = re.compile("[A-Z][a-z]?[a-z]?\.")
       
    abbrevs = regex1.findall(str(text))
    for elem in abbrevs:
        text = text.replace(elem,elem[0:-1])
        
    regex2   = re.compile("\$\d+\.")
       
    abbrevs = regex2.findall(str(text)) 
    for elem in abbrevs:
        text = text.replace(elem,elem[0:-1])
        
    return str(text)
    
def write(plot):
    """
    This method will save all generated plots to the *BotOutput.txt* file. \n
    Input: **plot** of type *string* to be saved to the txt file.
    """
    stampDate = str(datetime.date.today())
    fileName  = 'BotOutput'+stampDate+'.txt'    
    
    # Check if BotOutput.txt already exists, else create it
    if not(os.path.exists(fileName)):
        output = open(fileName,'w',encoding='utf8')
        output.close()

    # Write into txt file
    with open(fileName, 'r+',encoding='utf8') as f_txt:
        # Go to last line of the file        
        for line in f_txt:
            pass
        f_txt.write(plot+'\n')

    