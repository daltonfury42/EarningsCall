import glob
import random

from flask import Flask, render_template
import os
import csv
import re

app = Flask(__name__)

@app.route('/call/<string:callId>')
def results(callId):
    title, timeData, texts = getData(callId)
    return render_template('result.html', callId=callId, timeData=timeData, texts=texts, title=title)

@app.route('/call/')
def calls():

    dataList = getAvailableData()

    return render_template('calls.html', dataList=dataList)

def getAvailableData():
    availData = []
    dataDir = 'data/transcripts'
    for fileName in os.listdir(dataDir):
        base, _ = os.path.splitext(fileName)
        base = base.split('-')
        callId = base[0]
        title = ' '.join(base[1:])
        title = title.title()
        availData.append({'callId': callId, 'title': title})

    return availData[:5]

def getData(callId):
    transcriptFilePath = os.path.join('data/transcripts', callId + '*.csv')
    transcriptFilePath = glob.glob(transcriptFilePath)[0]

    base, _ = os.path.splitext(transcriptFilePath)
    header = base.split('-')[1:]
    header = ' '.join(header).title()

    header = re.sub('Earnings Call Transcript$', '', header)

    title = re.sub(r'Ceo[ A-Za-z]*', 'Q', header)

    timeData, texts = [], []

    with open(transcriptFilePath) as csvFile:
        spamreader = csv.reader(csvFile)
        for row in spamreader:
            splitId, startTime, endTime, _, speaker, text = row[0], row[1], row[2], row[3], row[4], row[5]
            text = text.decode('utf-8')
            timeData.append({'splitId': splitId, 'startTime': startTime, 'endTime': endTime})
            texts.append({'splitId': splitId, 'speaker': speaker, 'text': text,
                          'emotion': random.choice(['happy', 'sad', 'neutral'])})

    return  title, timeData, texts