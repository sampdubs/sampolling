from flask import Flask, url_for, redirect, render_template, make_response, request
import json
import datetime
app = Flask(__name__)

polls = {}


@app.route("/poll/create/", methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        return render_template(f"{request.form['type']}.html")
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
                    tpoll['responses'] = 0
                    for name in result:
                        if f'answer{i}_' in name:
                            if len(result[name]) > 0:
                                tpoll['choices'].append(result[name])
                                tpoll['answers'][result[name]] = 0
                    poll.append(tpoll)
                else:
                    break
            polls[id] = poll
        elif "num" in result:
            poll = []
            achoices = []
            for name in result:
                if 'answer' in name:
                    if len(result[name]) > 0:
                        achoices.append(result[name])
            for i in range(result["num"]):
                tpoll = {}
                tpoll['question'] = f"Question {i + 1}"
                tpoll['choices'] = []
                tpoll['answers'] = {}
                tpoll['responses'] = 0
                for choice in achoices:
                    tpoll['choices'].append(choice)
                    tpoll['answers'][choice] = 0
                poll.append(tpoll)
            polls[id] = poll
        else:
            polls[id][0]['answers'][result['answer'].replace(
                "****SPACE****", " ")] += 1
            polls[id][0]['responses'] += 1
        return f'Yay! you made a poll click <a href="{request.path}">here</a> to view the results'
    if id not in polls:
        return "Sorry, that poll doesn't exit..."
    return render_template('results.html', poll=polls[id], round=round, enumerate=enumerate)


@app.route("/poll/<id>/")
def take_redirect(id):
    return redirect(request.path + "1/")


@app.route("/poll/<id>/<qnumber>/", methods=['POST', 'GET'])
def take(id, qnumber):
    if id not in polls:
        return "Sorry, that poll doesn't exit..."
    if not qnumber.isdigit():
        qnumber  = "1"
    qnumber = int(qnumber) - 2
    if request.method == 'POST':
        result = request.form
        polls[id][qnumber]['answers'][result['answer'].replace(
            "****SPACE****", " ")] += 1
        polls[id][qnumber]['responses'] += 1
    qnumber += 1
    if qnumber >= len(polls[id]):
        return redirect(url_for('results', id=id))
    cook = request.cookies.get(id)
    if cook != None:
        cook = json.loads(cook)
    else:
        cook = []
    if len(cook) > 0:
        taken = cook[qnumber]
    else:
        taken = False
        for i in range(len(polls[id])):
            cook.append(False)
        cook[qnumber] = True
        resp = make_response(render_template(
            "answer.html", poll=polls[id][qnumber], id=id))
        resp.set_cookie(id, json.dumps(cook), expires=(
            datetime.datetime.now() + datetime.timedelta(days=1)))
        return resp
    if taken:
        return 'You have already answered this question, click <a href=../results>here</a> to go to the results page'
    cook[qnumber] = True
    resp = make_response(render_template(
        "answer.html", poll=polls[id][qnumber], id=id))
    resp.set_cookie(id, json.dumps(cook), expires=(
        datetime.datetime.now() + datetime.timedelta(days=1)))
    return resp


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
