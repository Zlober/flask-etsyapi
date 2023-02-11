from flask import Flask, request
application = Flask(__name__)
app = application


@app.route('/')
def index():
    if request.args:
        code = request.args.get('code')
        state = request.args.get('state')
        return f'{code} {state}'
    return 'Hello world'
