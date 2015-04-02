import ConfigParser
import sys
import os
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest


def load_config():
    global config
    config = ConfigParser.ConfigParser()
    config.read('settings.ini')


def save_token():
    config_file = open('settings.ini', 'w')
    config.set("Auth", "access_token", access_token)
    config.write(config_file)
    config_file.close()


def try_again():
    answer = raw_input("Do you want to try again? (y/n): ").strip()
    if answer == 'y':
        connect()
    else:
        quit(0)


def connect():
    global access_token, user_id
    app_key = config.get("Auth", "app_key")
    app_secret = config.get("Auth", "app_secret")
    access_token = config.get("Auth", "access_token")

    if access_token == '':
        auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        authorize_url = auth_flow.start()
        print "1. Go to: " + authorize_url
        print "2. Click \"Allow\" (you might have to log in first)."
        print "3. Copy the authorization code."
        auth_code = raw_input("Enter the authorization code here: ").strip()
        try:
            access_token, user_id = auth_flow.finish(auth_code)
        except dbrest.ErrorResponse, e:
            print("Error: %s" % (e,))
            try_again()

            return
        finally:
            save_token()
    else:
        try:
            dc = DropboxClient(access_token).account_info()
        except dbrest.ErrorResponse, e:
            print("Error: %s" % (e,))
            access_token = ''
            save_token()
            try_again()

            return


def upload_file(file_path):
    dc = DropboxClient(access_token)
    try:
        f = open(file_path, 'rb')
        file_name = os.path.basename(file_path)
        dc.put_file(file_name, f, overwrite=True)
        f.close()
        shared_file = dc.share(file_name)
        return shared_file['url']
    except IOError:
        print "Error: can\'t find file or read data"
    except dbrest.ErrorResponse, e:
        print ("Error: %s" % (e,))


def open_file_in_ms_office(file_path):
    ms_office = config.get("General", "ms_office")
    dropbox_url = upload_file(file_path)
    url = ms_office + dropbox_url
    url_open_cmd = 'xdg-open \"%s\" > /dev/null 2>&1 &' % (url)
    print(url_open_cmd)
    #os.sysconf(url_open_cmd)


if __name__ == '__main__':
    load_config()
    connect()
    file = sys.argv[1]
    if file != '':
        open_file_in_ms_office(file)