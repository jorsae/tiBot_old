import datetime
import logger
import json
import os

"""
    Can maybe remove:
        overall -> RunBot
        Twitter -> TempFile
        Twitter -> FollowItems
        imgur -> MaxImageSize
        imgur -> MaxVideoSize
"""
class Settings():
    def __init__(self, settingsFile):
        self.settingsFile = settingsFile
        if os.path.isfile(self.settingsFile) is False:
            print('%s does not exist. Exiting')
            exit()
        try:
            settingsData = open(self.settingsFile)
            data = json.load(settingsData)
            self.runBot = data["overall"]["runBot"]
            self.runTweetThread = data["overall"]["runTweetThread"]
            self.runFollowThread = data["overall"]["runFollowThread"]
            self.database = data["overall"]["database"]

            self.logFileName = data["logger"]["logFileName"]
            self.LOGGER_PRINT_LEVEL = self.get_logger_print_level(data["logger"]["lOGGER_PRINT_LEVEL"])
            self.logFolder = data["logger"]["logFolder"]
            self.logSize = data["logger"]["logSize"]

            self.consumerKey = data["twitter"]["consumerKey"]
            self.consumerSecret = data["twitter"]["consumerSecret"]
            self.accessToken = data["twitter"]["accessToken"]
            self.accessSecret = data["twitter"]["accessSecret"]
            self.twitterName = data["twitter"]["twitterName"]
            self.tempFile = data["twitter"]["tempFile"]
            self.hashTags = data["twitter"]["hashTags"]
            self.followTweetsMin, self.followTweetsMax = self.read_2values_array(data["twitter"]["followTweets"])
            self.followFriendsMin, self.followFriendsMax = self.read_2values_array(data["twitter"]["followFriends"])
            self.followFollowersMin, self.followFollowersMax = self.read_2values_array(data["twitter"]["followFollowers"])
            self.followFavoritesMin, self.followFavoritesMax = self.read_2values_array(data["twitter"]["followFavorites"])
            
            self.followItems = data["twitter"]["followItems"]
            self.updateStatHour = data["twitter"]["updateStatHour"]
            self.updateTweetAfter = self.read_datetime_array(data["twitter"]["updateTweetAfter"])
            self.followNewPerson = self.read_datetime_array(data["twitter"]["followNewPerson"])
            self.unfollowPersonAfter = self.read_datetime_array(data["twitter"]["unfollowPersonAfter"])

            self.imgurHeaders = {'authorization':'Client-Id %s' % data["imgur"]["clientId"]}
            self.authLink = data["imgur"]["authLink"]
            self.tagLink = data["imgur"]["tagLink"]
            self.postBaseurl = data["imgur"]["postBaseurl"]
            self.downloadBaseurl = data["imgur"]["downloadBaseurl"]
            self.imgurTags = data["imgur"]["tags"]
            self.maxImageSize = data["imgur"]["maxImageSize"]
            self.maxVideoSize = data["imgur"]["maxVideoSize"]
        except Exception as e:
            print('Exception: %s' % e)

    def check_all_settings(self):
        if type(self.updateTweetAfter) != datetime.timedelta:
            return False
        if type(self.followNewPerson) != datetime.timedelta:
            return False
        if type(self.unfollowPersonAfter) != datetime.timedelta:
            return False
        if type(self.followTweetsMin) != int:
            return False
        if type(self.followTweetsMax) != int:
            return False
        if type(self.followFriendsMin) != int:
            return False
        if type(self.followFriendsMax) != int:
            return False
        if type(self.followFollowersMin) != int:
            return False
        if type(self.followFollowersMax) != int:
            return False
        if type(self.followFavoritesMin) != int:
            return False
        if type(self.followFavoritesMax) != int:
            return False
        if type(self.followItems) != int:
            return False
        return True

    def get_logger_print_level(self, printLevel):
        if printLevel == "debug":
            return logger.LogLevel.DEBUG
        elif printLevel == "info":
            return logger.LogLevel.INFO
        elif printLevel == "warning":
            return logger.LogLevel.WARNING
        elif printLevel == "error":
            return logger.LogLevel.ERROR
        elif printLevel == "critical":
            return logger.LogLevel.CRITICAL
        else:
            return logger.LogLevel.DEBUG

    def read_2values_array(self, arr):
        try:
            return arr[0], arr[1]
        except:
            return None, None

    def read_datetime_array(self, arr):
        try:
            return datetime.timedelta(days=arr[0], hours=arr[1])
        except:
            return None, None