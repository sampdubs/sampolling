from flask import Flask, url_for, redirect, render_template, make_response, request
import json, datetime
app = Flask(__name__)

polls = {}

@app.route("/poll/create/")
def create():
    return render_template("create.html")

@app.route("/poll/")
def poll():
    return redirect(url_for('create'))

@app.route("/")
def index():
    return redirect(url_for('create'))

@app.route("/poll/<id>/results/", methods=['POST', 'GET'])
def results(id):
    if request.method == 'POST':
        result = request.form
        if 'question1' in result:
            poll = []
            i = 0
            while True:
                i += 1
                if f'question{i}' in result:
                    tpoll = {}
                    tpoll['question'] = result[f'question{i}']
                    tpoll['choices'] = []
                    tpoll['answers'] = {}
                    tpoll['responses'] = 0.0
                    for name in result:
                        if f'answer{i}_' in name:
                            if len(result[name]) > 0: 
                                tpoll['choices'].append(result[name])
                                tpoll['answers'][result[name]] = 0
                    poll.append(tpoll)
                else:
                    break
            polls[id] = poll
        else:
            polls[id][0]['answers'][result['answer'].replace("****SPACE****", " ")] += 1
            polls[id][0]['responses'] += 1
    return render_template('results.html', poll=polls[id], round=round)

@app.route("/poll/<id>/")
def take_redirect(id):
    return redirect(request.path + "1/")

@app.route("/poll/<id>/<qnumber>/", methods=['POST', 'GET'])
def take(id, qnumber):
    qnumber = int(qnumber) - 1
    if  request.method == 'POST':
        result = request.form
        polls[id][qnumber - 1]['answers'][result['answer'].replace("****SPACE****", " ")] += 1
        polls[id][qnumber - 1]['responses'] += 1
        if qnumber >= len(polls[id]):
            return redirect(url_for('results', id=id))
    cook = request.cookies.get('taken')
    if cook != None:
        cook = json.loads(cook)
    else:
        cook = {}
    if id in cook:
        taken = cook[id]
    else:
        taken = False
        cook[id] = {}
        for i in range(len(polls[id])):
            cook[id][str(i + 1)] = False
        cook[id][qnumber] = True
        resp = make_response(render_template("answer.html", poll=polls[id][qnumber], id=id))
        resp.set_cookie('taken', json.dumps(cook), expires=(datetime.datetime.now()+datetime.timedelta(days=10)))
        return resp
    if taken:
        return 'You have already answered this question'
    for i in range(len(polls[id])):
        cook[id][str(i + 1)] = False
    cook[id][qnumber] = True
    resp = make_response(render_template("answer.html", poll=polls[id][qnumber], id=id))
    resp.set_cookie('taken', json.dumps(cook), expires=(datetime.datetime.now()+datetime.timedelta(days=10)))
    return resp

if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)