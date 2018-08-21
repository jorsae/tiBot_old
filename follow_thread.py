"""
settings.TWITTER_ADD_TWEETS_MIN = 20
settings.TWITTER_ADD_TWEETS_MAX = 50000
settings.TWITTER_ADD_FRIENDS_MIN = 25
settings.TWITTER_ADD_FRIENDS_MAX = 2000
settings.TWITTER_ADD_FOLLOWERS_MIN = 30
settings.TWITTER_ADD_FOLLOWERS_MAX = 2000
settings.TWITTER_ADD_FAVORITES_MIN = 0
settings.TWITTER_ADD_FAVORITES_MAX = 500

statuses[]
    -> user
        -> id
        -> screen_name
        -> followers_count | x follow screen_name
        -> friends_count | screen_name follows x
        -> favourites_count | likes
        -> statuses_count | total tweets
"""
import random
import time
import datetime
import logger
import twitter.twitter as twitter
import imgur.imgur as imgur
import database.database as database
import database.query as query
import settings

class TwitterAccount():
    def __init__(self, screenName, followers, friends, favorites, tweets):
        self.screenName = screenName
        self.followers = followers
        self.friends = friends
        self.favorites = favorites
        self.tweets = tweets

    def to_string(self):
        return '%s: %d %d %d %d' % (self.screenName, self.followers, self.friends, self.favorites, self.tweets)

def run(log, db, twit, imgr):
    log.log(logger.LogLevel.INFO, 'follow_thread.run() is now running: %s' % settings.RunFollowThread)
    while settings.RunFollowThread:
        # Find a person
        q = get_search_q()
        result = twit.search(q, 100)
        if result is None:
            log.log(logger.LogLevel.ERROR, 'follow_thread.run(): No result when searching \'%s\'' % q)
        personList = get_person_list(result)
        person = get_person(db, personList)

        # Follow person
        if person is None:
            log.log(logger.LogLevel.ERROR, 'Did not find anyone to follow out of: %d' % len(personList))
        else:
            followed = twit.follow_by_name(person.screenName)
            if followed:
                q = db.query_commit(query.QUERY_INSERT_FOLLOWS(), (person.screenName, datetime.datetime.now(), 1))
                if q:
                    log.log(logger.LogLevel.DEBUG, 'Added %s to database' % person.screenName)
                else:
                    log.log(logger.LogLevel.INFO, 'Failed to add %s to database' % person.screenName)
            else:
                log.log(logger.LogLevel.ERROR, 'Failed to follow: %s' % person.to_string())
        
        # Unfollow person
        endDate = datetime.datetime.now() - settings.TWITTER_UPDATE_UNFOLLOW_AFTER
        personList = db.query_fetchall(query.QUERY_GET_FOLLOWS_UPDATE_QUEUE(), (endDate, ))
        for person in personList:
            screenName = person[0]
            unfollowed = twit.unfollow_by_name(screenName)
            if unfollowed:
                dbResult = db.query_commit(query.QUERY_UPDATE_FOLLOWS(), (screenName, ))
                if dbResult:
                    log.log(logger.LogLevel.DEBUG, 'Updated database: %s are we not following anymore' % screenName)
                else:
                    log.log(logger.LogLevel.WARNING, 'Unable to update followingNow status on person: %s' % screenName)
            else:
                log.log(logger.LogLevel.ERROR, 'Failed to unfollow: %s' % screenName)

        log.log(logger.LogLevel.INFO, 'follow_thread.run() sleeping for: %d' % settings.TWITTER_FOLLOW_PERSON_DELAY.total_seconds())
        time.sleep(settings.TWITTER_FOLLOW_PERSON_DELAY.total_seconds())

def get_person(db, personList):
    for person in personList:
        if db.query_exists(query.QUERY_GET_FOLLOWS(), (person.screenName, )):
            continue
        
        validStats = person_valid_stats(person)
        if validStats:
            return person
    return None

def person_valid_stats(ta):
    """ checks if the person fits statistics criteria """
    if ta.tweets < settings.TWITTER_ADD_TWEETS_MIN or ta.tweets > settings.TWITTER_ADD_TWEETS_MAX:
        return False
    if ta.friends < settings.TWITTER_ADD_FRIENDS_MIN or ta.friends > settings.TWITTER_ADD_FRIENDS_MAX:
        return False
    if ta.followers < settings.TWITTER_ADD_FOLLOWERS_MIN or ta.followers > settings.TWITTER_ADD_FOLLOWERS_MAX:
        return False
    if ta.favorites < settings.TWITTER_ADD_FAVORITES_MIN or ta.favorites > settings.TWITTER_ADD_FAVORITES_MAX:
        return False
    return True

def get_person_list(r):
    personList = []
    for status in r.json()['statuses']:
        screen_name = status['user']['screen_name']
        followers = status['user']['followers_count']
        friends_count = status['user']['friends_count']
        favourites_count = status['user']['favourites_count']
        statuses_count = status['user']['statuses_count']
        a = TwitterAccount(screen_name, followers, friends_count, favourites_count, statuses_count)
        personList.append(a)
    return set(personList)

def get_search_q():
    hashTags = settings.HASH_TAGS.split(' ')
    return hashTags[random.randint(0, len(hashTags) - 1)]