import csv
import os
from pydub import AudioSegment

def splitAllInDir(dirName):
    for csvFileName in os.listdir(dirName):
        filePath = os.path.join(dirName, csvFileName)
        split(filePath)

def split(csvFilePath):
    print('Splitting ' + csvFilePath)
    callId, _ = os.path.splitext(os.path.basename(csvFilePath))
    audioFilePath = os.path.join('forcedAlignment/mp3', callId + '.mp3')
    audio = AudioSegment.from_mp3(audioFilePath)

    with open(csvFilePath) as csvFile:
        csvreader = csv.reader(csvFile)
        for splitId, startTime, endTime, _ in csvreader:
            saveFilePath = os.path.join('forcedAlignment/mp3_segments', callId + '_' + splitId + '.mp3')
            if os.path.exists(saveFilePath):
                print('Skipping ' + saveFilePath)
                continue

            startTime = float(startTime) * 1000
            endTime = float(endTime) * 1000
            segment = audio[startTime:endTime]
            segment.export(saveFilePath, format='mp3')

            del segment

    import gc
    del audio
    gc.collect()