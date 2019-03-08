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

                audioFilePath = os.path.join('forcedAlignment/mp3_segments', callId + '_' + splitId + '.mp3')

                features = getMFCC(audioFilePath)

                row = [splitId, startTime, endTime] + features
                writer.writerow(row)





def getMFCC(audioFilePath):
    y, sr = librosa.load(audioFilePath)
    mfcc = list(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=1)[0])

    return mfcc
