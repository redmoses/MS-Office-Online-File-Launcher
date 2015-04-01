import dropbox
import ConfigParser


def load_auth_info():
    config = ConfigParser.ConfigParser()
    config.read('.config')
    app_key = config.get('Auth', 'APP_KEY')
    app_secret = config.get('Auth', 'APP_SECRET')
    return app_key, app_secret


def connect():
    app_key, app_secret = load_auth_info()
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)
    db_client = dropbox.client.DropboxClient(access_token)
    return db_client


if __name__ == '__main__':
    client = connect()
