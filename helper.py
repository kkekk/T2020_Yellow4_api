import requests
from collections import defaultdict

DBS_URL = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com'

HEADERS = {
    'identity': 'Group18',
    'token': '806ba7f9-963a-4761-badd-3242f56552a3'
}

def summarize(id, month):
    """Summarize account transactions"""
    if month == 'three':
        since = '04-30-2018'
        halve = 7
    elif month == 'one':
        since = '08-30-2018'
        halve = 9

    params = {
        'from': since,
        'to': '10-31-2018'
    }

    res = requests.get(f"{DBS_URL}/transactions/{id}", params=params, headers=HEADERS)

    if res.status_code != 200:
        return {'error': 'Account probably doesnt exist, or dates are wrong'}

    first_debit_tag_count = defaultdict(int)
    first_debit_tag_sum = defaultdict(float)
    first_credit_tag_count = defaultdict(int)
    first_credit_tag_sum = defaultdict(float)

    second_debit_tag_count = defaultdict(int)
    second_debit_tag_sum = defaultdict(float)
    second_credit_tag_count = defaultdict(int)
    second_credit_tag_sum = defaultdict(float)

    for j in res.json():
        date = int(j['date'][5:7])
        if date <= halve:
            if j['type'] == 'CREDIT':
                first_credit_tag_count[j['tag']] += 1
                first_credit_tag_sum[j['tag']] += float(j['amount'])
            else:
                first_debit_tag_count[j['tag']] += 1
                first_debit_tag_sum[j['tag']] += float(j['amount'])
        else:
            if j['type'] == 'CREDIT':
                second_credit_tag_count[j['tag']] += 1
                second_credit_tag_sum[j['tag']] += float(j['amount'])
            else:
                second_debit_tag_count[j['tag']] += 1
                second_debit_tag_sum[j['tag']] += float(j['amount'])


    return {
        'debit': {
            'debit_tag_count': second_debit_tag_count,
            'debit_tag_sum': second_debit_tag_sum
        },
        'credit': {
            'credit_tag_count': second_credit_tag_count,
            'credit_tag_sum': second_credit_tag_sum
        }
    }

def summarize2(ids):
    """Summarize account transactions"""
    params = {
        # check one month ago
        'from': '09-30-2018',
        'to': '10-31-2018'
    }

    jsons = []

    debit_tag_count = defaultdict(int)
    debit_tag_sum = defaultdict(float)
    credit_tag_count = defaultdict(int)
    credit_tag_sum = defaultdict(float)

    for id in ids:
        res = requests.get(f"{DBS_URL}/transactions/{id}", params=params, headers=HEADERS)

        if res.status_code != 200:
            return {'error': 'Account probably doesnt exist, or dates are wrong'}

        jsons.extend(res.json())


    for j in jsons:
        if j['type'] == 'CREDIT':
            credit_tag_count[j['tag']] += 1
            credit_tag_sum[j['tag']] += float(j['amount'])
        else:
            debit_tag_count[j['tag']] += 1
            debit_tag_sum[j['tag']] += float(j['amount'])


    for k in debit_tag_sum:
        debit_tag_sum[k] = '%.2f' % debit_tag_sum[k]

    for k in credit_tag_sum:
        credit_tag_sum[k] = '%.2f' % credit_tag_sum[k]

    return{
        'debit': {
            'debit_tag_count': debit_tag_count,
            'debit_tag_sum': debit_tag_sum
        },
        'credit': {
            'credit_tag_count': credit_tag_count,
            'credit_tag_sum': credit_tag_sum
        }
    }
