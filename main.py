import os
import random
import datetime
import threading
import time
import logger
import tweet_thread
import follow_thread
import settings
import startup
import twitter.twitter as twitter
import imgur.imgur as imgur
import database.database as database
import debug.debug as debug
import database.query as query

def start(log, db, twit, imgr):
    twitterThread = tweet_thread.TweetThread(log, db, twit, imgr)

    tweetThread = threading.Thread(target=twitterThread.run)
    tweetThread.daemon = True
    tweetThread.start()
    
    followThread = threading.Thread(target=follow_thread.run, args=(log, db, twit, imgr, ))
    followThread.daemon = True
    followThread.start()

    log.log(logger.LogLevel.INFO, 'tiBot is running')
    maintenance(log, db, twit, imgr, tweetThread, followThread)

def maintenance(log, db, twit, imgr, tweetThread, followThread):
    timePast = 0
    lastUpdateDay = None
    while settings.RunBot:
        # Updates twitter statistics to database
        if time.strftime("%H") == settings.TWITTER_UPDATE_STAT_HOUR:
            if lastUpdateDay is not datetime.datetime.now().day:
                update_user_stats(log, db, twit)
                lastUpdateDay = datetime.datetime.now().day
                log.log(logger.LogLevel.INFO, 'Updated user statistics')

        #Every hour
        if (timePast % 12) == 0 and timePast != 0:
            if tweetThread.is_alive() is False or followThread.is_alive() is False:
                log.log(logger.LogLevel.CRITICAL, 'tweetThread Status: %s | %s' % (tweetThread, tweetThread.isAlive()))
                log.log(logger.LogLevel.CRITICAL, 'followThread Status: %s | %s' % (followThread, followThread.isAlive()))
                settings.RunTweetThread = False
                settings.RunFollowThread = False
                settings.RunBot = False
                log.log(logger.LogLevel.CRITICAL, 'Getting ready to stop threads')

        #Every 6hours
        if (timePast % 72) == 0 and timePast != 0:
            timePast = 0 # Resetting timer
        timePast += 5
        time.sleep(60*5)
    
    shutdown = True
    while shutdown:
        time.sleep(60*5)
        if tweetThread.is_alive() is False and followThread.is_alive() is False:
            shutdown = False
            log.log(logger.LogLevel.CRITICAL, 'Shutting down and restarting')
            settings.RunTweetThread = True
            settings.RunFollowThread = True
            settings.RunBot = True
            startup.startup()            


def update_user_stats(log, db, twit):
    followers, tweets, friends, favorites = twit.get_user_stats()
    dbQuery = db.query_commit(query.QUERY_INSERT_STATS(), (datetime.datetime.now(), followers, tweets, friends, favorites, ))
    if dbQuery:
        log.log(logger.LogLevel.INFO, 'Inserted user statistics to database')
    else:
        log.log(logger.LogLevel.INFO, 'Failed to update user statistics to database') 