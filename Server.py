import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)
db = []


@app.route("/")
def hello():
    return "Hello, User! You can check status here ---> <a href='/status'>Статус</a>"


@app.route("/status")
def status():
    dn = datetime.now()
    return {
        'status': True,
        'name': 'Messenger',
        'time': dn.strftime('%d.%m.%Y %H:%M:%S'),
        'users': len(set(message['name'] for message in db)),
        'messages': len(db)
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json
    db.append({
        'id': len(db),
        'name': data['name'],
        'text': data['text'],
        'timestamp': time.time()
    })

    return {'ok': True}


@app.route("/messages")
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit > max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit

    after_id = 0
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        after_id += 1

    return {'messages': db[after_id:after_id + limit]}


app.run()
