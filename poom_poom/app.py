import ConfigParser
import sys

import os
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest




# create a blank config file if it doesn't exist
def create_config():
    try:
        # create and open the configuration file
        config_file = open(config_file_path, 'w')
        # add required sections
        config.add_section('Auth')
        config.add_section('General')
        # add the required attributes
        config.set('Auth','app_key')
        config.set('Auth','app_secret')
        config.set('Auth','access_token')
        # the url for opening file through dropbox in Microsoft Office Online
        config.set('General','office_url', 'https://www.dropbox.com/ow/msft/edit/home/Apps/Poom-Poom/')
        # write the configurations to the file
        config.write(config_file)
        config_file.close()
    except (IOError, ConfigParser.Error) as e:
        print 'Error: %s' % e


# load configurations in the global 'config' variable
# if configuration file doesn't exist create one
def load_config():
    global config
    config = ConfigParser.ConfigParser()
    if os.path.isfile(config_file_path):
        try:
            config.read(config_file_path)
        except ConfigParser.Error, e:
            print 'Error: %s' % e
    else:
        create_config()


# save token to config file for future use
def save_token():
    try:
        config_file = open(config_file_path, 'w')
        config.set('Auth', 'access_token', access_token)
        config.write(config_file)
        config_file.close()
    except (IOError, ConfigParser.Error) as e:
        print 'Error: %s' % e


# if it fails to connect to dropbox then ask the user whether they want to try again
def try_again():
    answer = raw_input('Do you want to try again? (y/n): ').strip()
    if answer == 'y':
        connect()
    else:
        quit(0)


# authenticate the client with dropbox and generate the access_token
# save the acess_token in a global variable
def connect():
    global access_token
    # load the required configurations
    app_key = config.get('Auth', 'app_key')
    app_secret = config.get('Auth', 'app_secret')
    access_token = config.get('Auth', 'access_token')
    # if access_token doesn't exist authenticate
    if access_token == '':
        # start the flow with app_key and app_secret from config file
        auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = auth_flow.start()
        # ask the user to do their part in the process
        print '1. Go to: ' + authorize_url
        print '2. Click \'Allow\' (you might have to log in first).'
        print '3. Copy the authorization code.'
        auth_code = raw_input('Enter the authorization code here: ').strip()
        # use the auth code to get the access_token
        try:
            access_token, user_id = auth_flow.finish(auth_code)
        except dbrest.ErrorResponse, e:
            'Error: %s' % e
            try_again()
        finally:
            save_token()
    else:
        # if access token exists then try to get the account info to test if its still valid
        try:
            dc = DropboxClient(access_token).account_info()
        except dbrest.ErrorResponse, e:
            'Error: %s' % e
            access_token = ''
            save_token()
            try_again()


# upload file to dropbox
def upload_file(file_path):
    dc = DropboxClient(access_token)
    try:
        f = open(file_path, 'rb')
        file_name = os.path.basename(file_path)
        dc.put_file(file_name, f)
        f.close()
    except IOError:
        print 'Error: can\'t find file or read data'
    except dbrest.ErrorResponse, e:
        print 'Error: %s' % e


# open file in Microsoft Office Online
def open_file_in_ms_office(file_path):
    # get the online office url
    office_url = config.get('General', 'office_url')
    # upload the file to dropbox to this app's directory
    upload_file(file_path)
    # open the default system browser with the link
    url = office_url + os.path.basename(file_path)
    url_open_cmd = 'xdg-open \'%s\' > /dev/null 2>&1 &' % (url)
    os.system(url_open_cmd)


# the entry point function for the app
def run():
    global config_file_path
    config_file_path = '~/.poom-poom.config'
    load_config()
    connect()
    file = sys.argv[1]
    if file != '':
        open_file_in_ms_office(file)


if __name__ == '__main__':
    run()
