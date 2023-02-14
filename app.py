from flask import Flask, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session
import dotenv
import os


application = Flask(__name__)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
dotenv.load_dotenv(dotenv.find_dotenv())
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
auth_base_url = 'https://www.etsy.com/oauth/connect'
token_url = 'https://api.etsy.com/v3/public/oauth/token'


@application.route('/')
def index():
    etsy = OAuth2Session(client_id)
    auth_url, state = etsy.authorization_url(auth_base_url)
    session['oauth_state'] = state
    return redirect(auth_url)


@application.route('/callback', methods=["GET"])
def callback():
    etsy = OAuth2Session(client_id, state=session['oauth_state'])
    token = etsy.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['oauth_token'] = token
    return redirect(url_for('.profile'))


@application.route('/profile', methods=['GET'])
def profile():
    return session


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    application.run(debug=True)
