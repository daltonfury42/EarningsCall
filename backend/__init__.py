from flask import Flask, render_template

from backend import service

app = Flask(__name__)

@app.route('/call/<string:callId>')
def results(callId):
    title, timeData, texts, emotionCount, topicCount, highlights = service.getData(callId)
    return render_template('result.html', callId=callId, timeData=timeData,
                           texts=texts, title=title, emotionCount=emotionCount,
                           topicCount=topicCount, hightlights=highlights)

@app.route('/')
def calls():

    dataList = service.getAvailableData()

    return render_template('calls.html', dataList=dataList)


if __name__ == "__main__":
    app.run()
