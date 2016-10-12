#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:36:25 2016

This class contains two methods that handle the external routines. Firstly the
email access that will send status alerts if the bot runs out of plots. Secondly
the twitter handle access.

@author: Wicke
"""
import tweepy, smtplib

def alertMail(status):
    """
    This function takes the number of available content and sends a warning via mail 
    informing about the left content. \n
    Mail will be sent from **sammyjekins@googlemail.com** to **philippwicke@web.de** \n
    Input: *status* = the number of left content that can be used (of type *integer*)
    """
    # Configuration
    sender_address   = "your_email_address"
    sender_pwd      = "your_email_password"
    receiver_address = "your_receipient_address"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_address, sender_pwd)
    
    if status > 0: 
        subject = "Status Alert for \"imdplotbot\"."
        text    = "The Twitter Bot \"imdplotbot\" has only "+str(status)+" plot(s) left! \n Consider updating the plot database via pythonanywhere.com \n"
    else: 
        subject = "ALERT! The \"imdplotbot\" ran out of plots."
        text    = "Update the plots on pythonanywhere.com for the \"imdplotbot\"."
    
    msg = 'Subject: %s\n\n%s' % (subject, text)
    server.sendmail(sender_address, receiver_address, msg)
    server.quit()    
    
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
    
    