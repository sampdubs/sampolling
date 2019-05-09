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
        poll = {}
        poll['question'] = result['question']
        poll['choices'] = []
        for name in result:
            if 'answer' in name:
                poll['choices'].append(result[name])
        polls[id] = poll
    return render_template('results.html')

@app.route("/poll/<id>/")
def take(id):
    return f"take {id}"

if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)