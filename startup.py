import argparse
import logger
import settings
import main
import twitter.twitter as twitter
import imgur.imgur as imgur
import database.database as database
import debug.debug as debug

def startup(debugMode = False):
    """ tiBot starting, that checks database, twitter and imgur """
    if debugMode:
        logSettings = logger.Logger(settings.LOGFILE_NAME, settings.LOG_FOLDER, maxSize=settings.LOG_SIZE, printLevel=logger.LogLevel.INFO)
    else:
        logSettings = logger.Logger(settings.LOGFILE_NAME, settings.LOG_FOLDER, maxSize=settings.LOG_SIZE, printLevel=settings.LOGGER_PRINT_LEVEL)
    logSettings.log(logger.LogLevel.INFO, 'tiBot is starting up', forcePrint=True)

    db = check_database(logSettings)
    if db is None:
        logSettings.log(logger.LogLevel.CRITICAL, 'Database is not set up correctly. Exiting..')
        return

    twit = twitter.Twitter(logSettings)
    twit.authenticated = twit.authenticate()
    if twit.authenticated is False:
        logSettings.log(logger.LogLevel.CRITICAL, 'Twitter is not authenticated. Exiting..')
        return
        
    imgr = imgur.Imgur(logSettings)
    imgr.authenticated = imgr.authenticate()
    if imgr.authenticated is False:
        logSettings.log(logger.LogLevel.CRITICAL, 'Imgur is not authenticated. Exiting..')
        return
    
    if debugMode:
        logSettings.log(logger.LogLevel.INFO, 'Everything is set up, starting tiBot in debug mode..')
        debug.debug(logSettings, db, twit, imgr)
    else:
        logSettings.log(logger.LogLevel.INFO, 'Everything is set up, starting tiBot..')
        main.start(logSettings, db, twit, imgr)
    
def check_database(logSettings):
    db = database.Database(logSettings)
    checkDB = db.check_database()
    if checkDB is False:
        logSettings.log(logger.LogLevel.CRITICAL, 'Database is not set up correctly')
        return None
    return db

def check_imgur(logSettings):
    i = imgur.Imgur(logSettings)
    i.authenticated = i.authenticate()
    return i

def parse_arguments():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', help='Whether to start in debug mode')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    if args.debug:
        startup(True)
    else:
        startup()

if __name__ == '__main__':
    parse_arguments()
