from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        code = request.args.get('code')
        state = request.args.get('state')
        return f'{code} {state}'
    return 'Hello world'
