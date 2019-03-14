import csv
import glob
import os
from itertools import zip_longest


def zip_equal(*iterables):
    sentinel = object()
    for combo in zip_longest(*iterables, fillvalue=sentinel):
        if sentinel in combo:
            raise ValueError('Iterables have different lengths')
        yield combo


def combineAll(featureDir):
    for fileName in os.listdir(featureDir):
        filePath = os.path.join(featureDir, fileName)
        combine(filePath)


def combine(timingsFilePath):
    print('Combining ' + timingsFilePath)
    callId, _ = os.path.splitext(os.path.basename(timingsFilePath))

    transcriptFilePath = os.path.join('extractData/out', callId + '*.csv')
    transcriptFilePath = glob.glob(transcriptFilePath)[0]
    _, outFileName = os.path.split(transcriptFilePath)
    outPutFilePath = os.path.join('combined', outFileName)

    with open(transcriptFilePath, 'r') as transcriptFile, open(timingsFilePath, 'r') as timingsFile:

        with open(outPutFilePath, 'w') as outFile:
            for trancscipt, timings in zip_equal(transcriptFile, timingsFile):
                timings = ','.join(list(csv.reader([timings]))[0][:3])
                outFile.write(timings + ',' + trancscipt)


if __name__ == '__main__':

    combineAll('extractFeatures/timings')