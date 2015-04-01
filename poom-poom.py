import ConfigParser
import sys

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest


def load_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


def connect():
    auth = load_config('.auth')
    app_key = auth.get("Auth", "APP_KEY")
    app_secret = auth.get("Auth", "APP_SECRET")
    global access_token, user_id

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

        try_again = raw_input("Do you want to try again? (y/n): ").strip()
        if try_again == 'y':
            connect()
        else:
            quit(0)

        return


if __name__ == '__main__':
    connect()
    office_file = sys.argv[1]

    dc = DropboxClient(access_token)
    link = dc.share('_public')
    print link.url
    # office_file = sys.argv[1]

