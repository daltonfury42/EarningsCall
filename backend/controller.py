import random

from flask import Flask, render_template
import os
import csv

app = Flask(__name__)

@app.route('/call/<string:callId>')
def results(callId):
    timeData, texts = getData(callId)
    return render_template('result.html', callId=callId, timeData=timeData, texts=texts)

@app.route('/call')
def calls():

    dataList = getAvailableData()

    return render_template('calls.html', dataList=dataList)

def getAvailableData():
    availData = []
    dataDir = 'data/transcripts'
    for fileName in os.listdir(dataDir):
        print(fileName)
        callId, _ = os.path.splitext(fileName)
        availData.append({'callId': callId, 'title': 'Title goes here'})

    return availData

def getData(callId):
    transcriptFilePath = os.path.join('data/transcripts', callId + '.csv')

    timeData, texts = [], []

    with open(transcriptFilePath) as csvFile:
        spamreader = csv.reader(csvFile)
        for row in spamreader:
            speaker, text, splitId, startTime, endTime = row[0], row[1], row[2], row[3], row[4]
            text = text.decode('utf-8')
            timeData.append({'splitId': splitId, 'startTime': startTime, 'endTime': endTime})
            texts.append({'splitId': splitId, 'speaker': speaker, 'text': text,
                          'emotion': random.choice(['happy', 'sad', 'neutral'])})

    return  timeData, texts