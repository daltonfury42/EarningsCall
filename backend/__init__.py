import glob
from collections import defaultdict, OrderedDict

from flask import Flask, render_template
import os
import csv
import re

app = Flask(__name__)
backendDir = os.path.dirname(__file__)

@app.route('/call/<string:callId>')
def results(callId):
    title, timeData, texts, emotionCount, topicCount = getData(callId)
    return render_template('result.html', callId=callId, timeData=timeData,
                           texts=texts, title=title, emotionCount=emotionCount, topicCount=topicCount)

@app.route('/')
def calls():

    dataList = getAvailableData()

    return render_template('calls.html', dataList=dataList)

def getAvailableData():
    availData = []
    dataDir = os.path.join(backendDir, 'data/transcripts')
    for fileName in os.listdir(dataDir):
        base, _ = os.path.splitext(fileName)
        base = base.split('-')
        callId = base[0]
        title = ' '.join(base[1:])
        title = title.title()
        availData.append({'callId': callId, 'title': title})

    return availData[:5]

def getData(callId):
    transcriptsDir = os.path.join(backendDir, 'data/transcripts')
    transcriptFilePath = os.path.join(transcriptsDir, callId + '*.csv')
    transcriptFilePath = glob.glob(transcriptFilePath)[0]

    base, _ = os.path.splitext(transcriptFilePath)
    header = base.split('-')[1:]
    header = ' '.join(header).title()

    header = re.sub('Earnings Call Transcript$', '', header)

    title = re.sub(r'Ceo[ A-Za-z]*', 'Q', header)

    timeData, texts, topicCount = [], [], defaultdict(lambda: 0)

    emotionCount = OrderedDict()
    emotionCount['All'] = 0
    emotionCount['Happy'] = 0
    emotionCount['Neutral'] = 0
    emotionCount['Sad'] = 0
    emotionCount['Analytical'] = 0
    emotionCount['Strategy'] = 0

    with open(transcriptFilePath) as csvFile:
        spamreader = csv.reader(csvFile)
        for row in spamreader:
            if (row[3] == "qna"):
                continue
            splitId, startTime, endTime, _, speaker, text, emotion, topic = row
            text = text.decode('utf-8')
            emotion = emotion.strip()
            topic = topic.strip().title()
            timeData.append({'splitId': splitId, 'startTime': startTime, 'endTime': endTime})
            texts.append({'splitId': splitId, 'speaker': speaker, 'text': text,
                          'emotion': emotion, 'topic': topic})

            emotionCount[emotion] = emotionCount[emotion] + 1
            emotionCount['All'] += 1
            topicCount[topic] = topicCount[topic] + 1
            topicCount['All'] += 1

    return title, timeData, texts, emotionCount, topicCount

if __name__ == "__main__":
    app.run()
