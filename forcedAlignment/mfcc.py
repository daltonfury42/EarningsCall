import csv
import os
import librosa

def extractAllInDir(dirName):
    for csvFileName in os.listdir(dirName):
        filePath = os.path.join(dirName, csvFileName)
        extract(filePath)

def extract(csvFilePath):
    print('Extracting from ' + csvFilePath)
    callId, _ = os.path.splitext(os.path.basename(csvFilePath))
    audioFilePath = os.path.join('forcedAlignment/mp3', callId + '.mp3')

    with open(csvFilePath) as csvReadFile:
        csvreader = csv.reader(csvReadFile)

        saveFilePath = os.path.join('forcedAlignment/features', callId + '.csv')
        if os.path.exists(saveFilePath):
            print('Skipping ' + saveFilePath)
            return

        with open(saveFilePath, 'w') as csvWriteFile:
            writer = csv.writer(csvWriteFile, delimiter=',')
            for row in csvreader:
                splitId, startTime, endTime = row[0], row[1], row[2]
                features = getMFCC(audioFilePath, startTime, endTime)

                row = [splitId, startTime, endTime] + features
                writer.writerow(row)





def getMFCC(audioFilePath, startTime, endTime):
    startTime, endTime = float(startTime), float(endTime)
    duration = endTime - startTime

    y, sr = librosa.load(audioFilePath, offset=startTime, duration=duration)
    mfcc = list(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=1)[0])

    return mfcc
