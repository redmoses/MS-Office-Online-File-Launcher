import ConfigParser
import sys
import os
from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest


def load_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


def save_token(config):
    config_file = open('.auth', 'w')
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

    auth = load_config('.auth')
    app_key = auth.get("Auth", "app_key")
    app_secret = auth.get("Auth", "app_secret")
    access_token = auth.get("Auth", "access_token")

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
            if e.status == 400:
                print('Error: It seems your authorization code is invalid.')
            else:
                print("Error: %s" % (e,))

            try_again()

            return
        finally:
            save_token(auth)
    else:
        try:
            dc = DropboxClient(access_token).account_info()
        except dbrest.ErrorResponse, e:
            print("Error: %s" % (e,))
            access_token = ''
            save_token(auth)
            try_again()

            return


def upload_file(file_path):
    dc = DropboxClient(access_token)
    f = open(file_path, 'rb')
    file_name = os.path.basename(file_path)
    response = dc.put_file(file_name, f)
    f.close()

    print dc.media(file_name)


if __name__ == '__main__':
    connect()
    file = sys.argv[1]
    if file != '':
        upload_file(file)


