from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def index():
    code = request.args.get('code')
    state = request.args.get('state')
    return code, state
