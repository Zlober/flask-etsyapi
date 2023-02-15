from flask import Flask, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session
import dotenv
import os
import base64
import re
import hashlib


application = Flask(__name__)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
dotenv.load_dotenv(dotenv.find_dotenv())
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
auth_base_url = 'https://www.etsy.com/oauth/connect'
token_url = 'https://api.etsy.com/v3/public/oauth/token'
scope = 'transactions_r%20transactions_w'
redirect_uri = 'https://flask-etsyapi-production.up.railway.app/callback'
code_challenge_method = 'S256'
code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")



@application.route('/')
def index():
    etsy = OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        scope=scope,
    )
    auth_url, state = etsy.authorization_url(
        auth_base_url,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )
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
