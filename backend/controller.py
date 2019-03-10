from flask import Flask, render_template
app = Flask(__name__)

@app.route('/call/<string:call_id>')
def hello_world(call_id):
    return render_template('result.html', call_id=call_id)

