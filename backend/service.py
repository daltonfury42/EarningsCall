import re
import csv
import os
import glob
from collections import defaultdict, OrderedDict
from enum import Enum

print('Here')

class Emotions(Enum):
    ALL = 'All'
    HAPPY = 'Happy'
    NEUTRAL = 'Neutral'
    SAD = 'Sad'
    ANALYTICAL = 'Analytical'
    STRATEGICAL = 'Strategical'


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

    highlightsDict, highlights_flat, tags_dict, emotion_dict = getResults(callId, .7)

    data = {}

    with open(transcriptFilePath) as csvFile:
        spamreader = csv.reader(csvFile)
        for row in spamreader:
            if (row[3] == "qna"):
                continue
            splitId, startTime, endTime, _, speaker, text, _, topic = row
            # text = text.decode('utf-8')
            emotion = emotion_dict[splitId]
            topic = topic.strip().title()
            data[splitId] = {'startTime': float(startTime), 'endTime': float(endTime), 'speaker': speaker,
                         'text': text, 'emotion': emotion, 'topic': topic, 'tags': list(tags_dict[splitId])}

    return title, data, highlightsDict, highlights_flat

def getResults(callId, threshold):
    attentionTagsDir = os.path.join(backendDir, 'data/attention_tags')
    attentionTagsFilePath = os.path.join(attentionTagsDir, callId + '.csv')

    highlights_dict = defaultdict(lambda : [])
    tags_dict = defaultdict(lambda: set())
    emotion_dict = {}
    try:
        with open(attentionTagsFilePath) as csvFile:
            spamReader = csv.reader(csvFile)
            next(spamReader, None)
            for _, id, sentence, attention, emotion, tags in spamReader:
                emotion_dict[id] = emotion
                tags_dict[id] = tags_dict[id].union(set(tags.split()))
                if float(attention) > threshold and emotion != Emotions.NEUTRAL.value:
                    hightlight = (sentence.capitalize(), float(attention), id)
                    highlights_dict[emotion].append(hightlight)
    except IOError:
        pass

    for emotion in highlights_dict.keys():
        highlights_dict[emotion] = sorted(highlights_dict[emotion], key=lambda highlight: highlight[1], reverse=True)


    highlights_flat = highlights_dict.get(Emotions.HAPPY.value, []) + highlights_dict.get(Emotions.ANALYTICAL.value, []) \
                      + highlights_dict.get(Emotions.STRATEGICAL.value, [])

    highlights_flat = highlights_flat[:15]

    return highlights_dict, highlights_flat, tags_dict, emotion_dict


if __name__ == '__main__':
    getHighlightsAndTags('4239008', .7)