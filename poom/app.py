import configparser
import time
import sys
import logging
import webbrowser

from tzlocal import get_localzone
import pytz
from dateutil.parser import parse
import os
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest






# initialize everything
def initialize():
    global logger, config_file_path
    app_dir = os.path.expanduser('~') + '/.poom'
    if not os.path.isdir(app_dir):
        os.makedirs(app_dir)
    config_file_path = app_dir + '/settings.ini'
    log_file = app_dir + '/poom.log'
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logger = logging.getLogger(__name__)


# create a blank config file if it doesn't exist
def create_config():
    try:
        # create and open the configuration file
        config_file = open(config_file_path, 'w')
        # add required sections
        config.add_section('Auth')
        config.add_section('General')
        # add the required attributes
        config.set('Auth', 'access_token', '')
        # the url for opening file through dropbox in Microsoft Office Online
        config.set('General', 'office_url', 'https://www.dropbox.com/ow/msft/edit/home/Apps/Poom/')
        # write the configurations to the file
        config.write(config_file)
        config_file.close()
    except (IOError, configparser.Error) as e:
        logger.error(e)


# load configurations in the global 'config' variable
# if configuration file doesn't exist create one
def load_config():
    global config
    config = configparser.ConfigParser()
    if os.path.isfile(config_file_path):
        try:
            config.read(config_file_path)
        except configparser.Error as e:
            logger.error(e)
    else:
        create_config()


# save token to config file for future use
def save_token():
    try:
        config_file = open(config_file_path, 'w')
        config.set('Auth', 'access_token', access_token)
        config.write(config_file)
        config_file.close()
    except (IOError, configparser.Error) as e:
        logger.error(e)


# if it fails to connect to dropbox then ask the user whether they want to try again
def try_again():
    answer = input(
        'It seems the app cannot connect to Dropbox at the moment. Do you want to try again? (y/n): ').strip()
    if answer == 'y':
        connect()
    else:
        quit(0)


# authenticate the client with dropbox and generate the access_token
# save the access_token in a global variable
def connect():
    global access_token
    # load the required configurations
    app_key = 'f0biclwqhiz4ctt'
    app_secret = 'wc0p641zbl3hfiv'
    access_token = config.get('Auth', 'access_token')

    # if access_token doesn't exist authenticate
    if access_token == '':
        # start the flow with app_key and app_secret from config file
        auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        try:
            authorize_url = auth_flow.start()
        except Exception as e:
            logger.error(e)
            try_again()

        # ask the user to do their part in the process
        print('1. Go to: ' + authorize_url)
        print('2. Click \'Allow\' (you might have to log in first).')
        print('3. Copy the authorization code.')
        auth_code = input('Enter the authorization code here: ').strip()
        # use the auth code to get the access_token
        try:
            access_token, user_id = auth_flow.finish(auth_code)
        except dbrest.ErrorResponse as e:
            logger.error(e)
            try_again()
        finally:
            save_token()
    else:
        # if access token exists then try to get the account info to test if its still valid
        try:
            dc = DropboxClient(access_token)
            account = dc.account_info()
            logger.info('User %s successfully authorized.' % account['display_name'])
        except dbrest.ErrorResponse as e:
            logger.error(e)
            access_token = ''
            save_token()
            try_again()
        except KeyboardInterrupt as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
            try_again()


# check if file is to be synced or uploaded
def to_be_synced(file_path):
    dc = DropboxClient(access_token)
    # check if file exists on Dropbox
    file_name = os.path.basename(file_path)
    tmp_file = open(file_path + '.poom', 'wb+')

    try:
        with dc.get_file('/' + file_name) as f:
            tmp_file.write(f.read())

        f.close()
        tmp_file.close()
        logger.debug("Comparing files...")
        # get dropbox file info
        dr_file_data = dc.metadata('/' + file_name)
        # get dropbox file last modified time in UTC
        dr_time = parse(dr_file_data['modified'])
        # get local file last modified time
        file_localtime = parse(time.ctime(os.path.getmtime(file_path)))
        # convert local time to utc
        local_dt = get_localzone().localize(file_localtime, is_dst=None)
        loc_time = local_dt.astimezone(pytz.utc)
        # compare the last modified times
        if dr_time > loc_time:
            logger.debug("Newer version on dropbox")
            os.remove(file_path)
            logger.debug("Removed file from disk")
            os.rename(file_path + '.poom', file_path)
        else:
            logger.debug("Newer version on local disk")
            return False

        return True
    except dbrest.ErrorResponse as e:
        if e.status == 404:
            return False


# upload file to dropbox
def upload_file(file_path):
    dc = DropboxClient(access_token)
    try:
        f = open(file_path, 'rb')
        file_name = os.path.basename(file_path)
        dc.put_file(file_name, f, overwrite=True)
        f.close()
    except IOError:
        logger.error('Error: can\'t find file or read data')
    except dbrest.ErrorResponse as e:
        logger.error(e)


# open file in Microsoft Office Online
def open_file_in_ms_office(file_path):
    # get the online office url
    office_url = config.get('General', 'office_url')
    # upload the file to dropbox to this application's directory
    if not to_be_synced(file_path):
        upload_file(file_path)
    # open the default system browser with the link
    url = office_url + os.path.basename(file_path)
    webbrowser.open(url)


# the entry point function for the app
def run():
    initialize()
    load_config()
    connect()
    file_path = sys.argv[1]
    if file_path != '':
        if os.path.isfile(file_path):
            open_file_in_ms_office(file_path)
        else:
            print("The file doesn't exist")
    else:
        print("You haven't provided any file path")


# for running inside ide
if __name__ == '__main__':
    run()