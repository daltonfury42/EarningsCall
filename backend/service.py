import re
import csv
import os
import glob
from collections import defaultdict, OrderedDict


backendDir = os.path.dirname(__file__)

def getAvailableData():
    availData = []
    metaFile = os.path.join(backendDir, 'data/meta/data.csv')
    with open(metaFile) as file:
        spamreader = csv.reader(file)

        for fileName, companyName, date, color in spamreader:
            base, _ = os.path.splitext(fileName)
            callId = base.split('-')[0]
            availData.append({'callId': callId, 'title': companyName + ' ' + date + ' Results', 'color': color})

    return availData

def getTitleFromFileName(filePath):
    base, _ = os.path.splitext(filePath)
    header = base.split('-')[1:]
    header = ' '.join(header).title()

    header = re.sub('Earnings Call Transcript$', '', header)

    title = re.sub(r'Ceo[ A-Za-z]*', 'Q', header)

    return title

def getData(callId):
    transcriptsDir = os.path.join(backendDir, 'data/transcripts')
    transcriptFilePath = os.path.join(transcriptsDir, callId + '*.csv')
    transcriptFilePath = glob.glob(transcriptFilePath)[0]

    title = getTitleFromFileName(transcriptFilePath)

    timeData, texts, topicCount = [], [], defaultdict(lambda: 0)

    emotionCount = OrderedDict()
    emotionCount['All'] = 0
    emotionCount['Happy'] = 0
    emotionCount['Neutral'] = 0
    emotionCount['Sad'] = 0
    emotionCount['Analytical'] = 0
    emotionCount['Strategical'] = 0

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
            if topic != 'Notopic':
                topicCount[topic] = topicCount[topic] + 1
                topicCount['All'] += 1

    highlights = getHighlights(callId, .7)

    return title, timeData, texts, emotionCount, topicCount, highlights

def getHighlights(callId, threshold):
    attentionTagsDir = os.path.join(backendDir, 'data/attention_tags')
    attentionTagsFilePath = os.path.join(attentionTagsDir, callId + '.csv')

    highlightsDict = defaultdict(lambda : [])

    with open(attentionTagsFilePath) as csvFile:
        spamReader = csv.reader(csvFile)
        next(spamReader, None)
        for _, id, sentence, attention, emotion, tags in spamReader:
            if float(attention) > threshold:
                highlightsDict[emotion].append((sentence, float(attention)))

    for emotion in highlightsDict.keys():
        highlightsDict[emotion] = sorted(highlightsDict[emotion], key=lambda highlight: highlight[1], reverse=True)

    return highlightsDict
