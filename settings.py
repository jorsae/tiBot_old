"""
    === SETTINGS EXAMPLE ===
    Need to change the following to make it work:
        Twitter Settings:
            CONSUMER_KEY
            CONSUMER_SECRET
            ACCESS_TOKEN
            ACCESS_SECRET
            TWITTER_NAME
            HASH_TAGS
        Imgur Settings:
            IMGUR_HEADER
    HIGHLY RECCOMMENDED
        Twitter Settings:
            HASH_TAGS
        Imgur Settings:
            IMGUR_TAGS
"""
import datetime
import logger

""" ########################## """
""" Program settings """
""" ########################## """
RunBot = True # Runs tiBot
RunTweetThread = True # Runs the thread that tweets
RunFollowThread = True # Runs the thread that follows/unfollows people

""" ########################## """
""" logging settings """
""" ########################## """
LOGFILE_NAME = 'tiBot'
LOGGER_PRINT_LEVEL = logger.LogLevel.DEBUG
LOG_FOLDER = 'logFolder'
LOG_SIZE = 3000

""" ########################## """
""" database settings """
""" ########################## """
DATABASE_FILE = 'tiBot.db'

""" ########################## """
""" Twitter settings """
""" ########################## """
CONSUMER_KEY = '<CONSUMER_KEY>'
CONSUMER_SECRET = '<CONSUMER_SECRET>'

ACCESS_TOKEN = '<ACCESS_TOKEN>'
ACCESS_SECRET = '<ACCESS_SECRET>'

TWITTER_NAME = '<TWITTER_NAME>'

TEMP_FILE = 'temp'
HASH_TAGS = '#example #hashtags' #Gets tweeted after every tweet

# Criteria to follow a user
# FRIENDS = user follows x
# FOLLOWERS = x follow users
TWITTER_ADD_TWEETS_MIN = 20
TWITTER_ADD_TWEETS_MAX = 50000
TWITTER_ADD_FRIENDS_MIN = 25
TWITTER_ADD_FRIENDS_MAX = 2000
TWITTER_ADD_FOLLOWERS_MIN = 30
TWITTER_ADD_FOLLOWERS_MAX = 2000
TWITTER_ADD_FAVORITES_MIN = 0
TWITTER_ADD_FAVORITES_MAX = 500

# Amount of persons getting, when looking for someone to follow
TWITTER_FOLLOW_ITEMS = 100

# The hour we update twitter user statistics
TWITTER_UPDATE_STAT_HOUR = '00'
# How long after a tweet we update the stats(favorites, retweets)
TWITTER_UPDATE_TWEET_AFTER = datetime.timedelta(days=1)
# How long before we follow another person
TWITTER_FOLLOW_PERSON_DELAY = datetime.timedelta(hours=6)
# How long after following a person, we unfollow
TWITTER_UPDATE_UNFOLLOW_AFTER = datetime.timedelta(days=7)

""" ########################## """
""" Imgur settings """
""" ########################## """
IMGUR_HEADER = {'authorization': 'Client-Id <CLIENT_ID>'}

IMGUR_AUTH_LINK = 'https://api.imgur.com/3/gallery/r/a'
IMGUR_TAG_LINK = 'https://api.imgur.com/3/gallery/t/'
IMGUR_POST_BASEURL = 'https://imgur.com/gallery/'
IMGUR_VIDEO_BASEURL = 'https://imgur.com/download/'

#Get's images from https://api.imgur.com/3/gallery/t/IMGUR_TAGS
IMGUR_TAGS = ['example_tag']

IMGUR_MAX_IMAGE_SIZE = 5000000 # 5MB is max image size for twitter API
IMGUR_MAX_VIDEO_SIZE = 15000000 # 15MB is max video size for twitter API
