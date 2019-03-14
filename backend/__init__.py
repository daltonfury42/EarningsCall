import glob
import random

from flask import Flask, render_template
import os
import csv
import re

app = Flask(__name__)
backendDir = os.path.dirname(__file__)

@app.route('/call/<string:callId>')
def results(callId):
    title, timeData, texts, emotionSet, topicSet = getData(callId)
    print(emotionSet)
    return render_template('result.html', callId=callId, timeData=timeData,
                           texts=texts, title=title, emotionSet=emotionSet, topicSet=topicSet)

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

    timeData, texts, emotionSet, topicSet = [], [], set(), set()

    with open(transcriptFilePath) as csvFile:
        spamreader = csv.reader(csvFile)
        for row in spamreader:
            if (row[3] == "qna"):
                continue
            splitId, startTime, endTime, _, speaker, text, emotion, topic = row
            text = text.decode('utf-8')
            timeData.append({'splitId': splitId, 'startTime': startTime, 'endTime': endTime})
            texts.append({'splitId': splitId, 'speaker': speaker, 'text': text,
                          'emotion': emotion, 'topic': topic})

            emotionSet.add(emotion)
            topicSet.add(topic)

    return  title, timeData, texts, list(emotionSet), list(topicSet)

if __name__ == "__main__":
    app.run()
