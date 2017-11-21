from flask import Flask
import json
import requests
import config

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/md5/<path:inp>')
def hash(inp):
    import md5
    m = md5.new()
    m.update(inp.encode('utf-8'))
    out =  m.hexdigest()
    return json.dumps({"input":inp, "output":out})


@app.route('/factorial/<string:inp>/')
def factorial(inp):
    try:
        out = int(inp)
        if inp <= 0:
            raise ValueError()
    except ValueError:
        return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"}) 
    else:
        for i in range(2,out):
            out *= i
        return json.dumps({"input":inp, "output":out})


@app.route('/fibonacci/<string:inp>/')
def fibonacci(inp):
    try:
        final = int(inp)
        if final <= 0:
            raise ValueError()
    except ValueError:
        return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"}) 
    else:
        out = [1, 1]
        i = 0
        while (out[-1]+out[-2]) <= final:
            i = out[-1] + out[-2] 
            out.append(i)
        return json.dumps({"input":inp, "output":out})


@app.route('/is-prime/<string:inp>/')
def isPrime(inp):
    try:
        num = int(inp)
        if num <= 0:
            raise ValueError()
    except ValueError:
        return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"}) 
    else:
        check = 1
        for i in range(2, num-1):
            if num % i == 0:
                check = 0
        if check:
            return json.dumps({"input":inp, "output":True})
        else:
            return json.dumps({"input":inp, "output":False})

@app.route('/slack-alert/<string:inp>/')
def slackAlert(inp):
    try:
        url = config.hook
        r = requests.post(url, data=json.dumps({'text':inp}),headers={'Content-Type': 'application/json'})
        return json.dumps({"input":inp, "output":True})
    except Exception as err:
        print(err)
        return json.dumps({"input":inp, "output":False})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')