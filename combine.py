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


def combine(featureFilePath):
    print('Combining ' + featureFilePath)
    callId, _ = os.path.splitext(os.path.basename(featureFilePath))

    transcriptFilePath = os.path.join('extractData/out', callId + '.csv')
    outPutFilePath = os.path.join('combined', callId + '.csv')

    with open(transcriptFilePath, 'r') as transcriptFile, open(featureFilePath, 'r') as featureFile:
        next(transcriptFile)    #Skip Header

        with open(outPutFilePath, 'w') as outFile:
            for trancscipt, feature in zip_equal(transcriptFile, featureFile):
                trancscipt = trancscipt.strip()
                outFile.write(trancscipt + ',' + feature)


if __name__ == '__main__':

    combineAll('extractFeatures/features')