from flask import Flask, request
from flask_cors import CORS
from helper import summarize, summarize2
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hi'


@app.route('/summary')
def summary():
    """ Args: accountIds, months

    from, to are str in format MM-DD-YYYY
    """
    accIds = request.args.getlist('accountIds')
    if not accIds:
        return {'error': 'accountIds required'}, 400

    try:
        accIds = map(lambda x: int(x), accIds)
    except:
        return {'error': 'invalid acc id'}, 400

    payload = {}
    # assuming the date string is valid is okay
    for i in accIds:
        payload[str(i)] = {
            'one_month': summarize(i, 'one'),
            'three_month': summarize(i, 'three')
        }

        for k in payload[str(i)]:
            if payload[str(i)][k].get('error'):
                return payload[str(i)][k], 400

    return payload

@app.route('/summary2')
def summary2():
    """ Args: accountIds, months

    from, to are str in format MM-DD-YYYY
    """
    accIds = request.args.getlist('accountIds')
    if not accIds:
        return {'error': 'accountIds required'}, 400

    try:
        accIds = map(lambda x: int(x), accIds)
    except:
        return {'error': 'invalid acc id'}, 400

    # assuming the date string is valid is okay
    payload = summarize2(accIds)
    if payload.get('error'):
        return payload, 400

    return payload
