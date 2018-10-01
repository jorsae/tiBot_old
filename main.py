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

def start(log, setting, db, twit, imgr):
    twitterThread = tweet_thread.TweetThread(log, setting, db, twit, imgr)

    if setting.runTweetThread:
        tweetThread = threading.Thread(target=twitterThread.run)
        tweetThread.daemon = True
        tweetThread.start()
    
    if setting.runFollowThread:
        followThread = threading.Thread(target=follow_thread.run, args=(log, setting, db, twit, imgr, ))
        followThread.daemon = True
        followThread.start()

    log.log(logger.LogLevel.INFO, 'tiBot is running')
    maintenance(log, setting, db, twit, imgr, tweetThread, followThread)

def maintenance(log, setting, db, twit, imgr, tweetThread, followThread):
    timePast = 0
    lastUpdateDay = None
    while setting.runBot:
        # Updates twitter statistics to database
        if time.strftime("%H") == setting.updateStatHour:
            if lastUpdateDay is not datetime.datetime.now().day:
                update_user_stats(log, db, twit)
                lastUpdateDay = datetime.datetime.now().day
                log.log(logger.LogLevel.INFO, 'Updated user statistics')

        #Every hour
        if (timePast % 12) == 0 and timePast != 0:
            if tweetThread.is_alive() is False or followThread.is_alive() is False:
                log.log(logger.LogLevel.CRITICAL, 'tweetThread Status: %s | %s' % (tweetThread, tweetThread.isAlive()))
                log.log(logger.LogLevel.CRITICAL, 'followThread Status: %s | %s' % (followThread, followThread.isAlive()))
                setting.runTweetThread = False
                setting.runFollowThread = False
                setting.runBot = False
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
            setting.runTweetThread = True
            setting.runFollowThread = True
            setting.runBot = True
            startup.startup(setting.settingsFile)            


def update_user_stats(log, db, twit):
    followers, tweets, friends, favorites = twit.get_user_stats()
    dbQuery = db.query_commit(query.QUERY_INSERT_STATS(), (datetime.datetime.now(), followers, tweets, friends, favorites, ))
    if dbQuery:
        log.log(logger.LogLevel.INFO, 'Inserted user statistics to database')
    else:
        log.log(logger.LogLevel.INFO, 'Failed to update user statistics to database') 