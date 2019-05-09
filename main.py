from flask import Flask, url_for, redirect, render_template, make_response, request
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
        if 'question' in result:
            poll = {}
            poll['question'] = result['question']
            poll['choices'] = []
            poll['answers'] = {}
            poll['responses'] = 0.0
            for name in result:
                if 'answer' in name:
                    if len(result[name]) > 0: 
                        poll['choices'].append(result[name])
                        poll['answers'][result[name]]  = 0
            polls[id] = poll
        else:
            polls[id]['answers'][result['answer']] += 1.0
            polls[id]['responses'] += 1
    return render_template('results.html', poll=polls[id], round=round)

@app.route("/poll/<id>/")
def take(id):
    return render_template("answer.html", poll=polls[id], id=id)

if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)