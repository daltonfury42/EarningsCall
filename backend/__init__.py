from flask import Flask, render_template
import json
from backend import service

app = Flask(__name__)

@app.route('/call/<string:callId>')
def results(callId):
    title, data, highlights_dict, highlights_flat = service.getData(callId)
    return render_template('result.html', callId=callId, data=json.dumps(data), title=title,
                           highlights_dict=highlights_dict, highlights_flat=highlights_flat)

@app.route('/')
def calls():

    dataList = service.getAvailableData()

    return render_template('calls.html', dataList=dataList)


if __name__ == "__main__":
    app.run()
