import csv
import os
import subprocess
import librosa

def splitAllInDir(dirName):
    for csvFileName in os.listdir(dirName):
        filePath = os.path.join(dirName, csvFileName)
        split(filePath)

def split(csvFilePath):
    print('Splitting ' + csvFilePath)
    callId, _ = os.path.splitext(os.path.basename(csvFilePath))
    audioFilePath = os.path.join('forcedAlignment/mp3', callId + '.mp3')

    with open(csvFilePath) as csvFile:
        csvreader = csv.reader(csvFile)
        for row in csvreader:
            splitId, startTime, endTime = row[0], row[1], row[2]
            saveFilePath = os.path.join('forcedAlignment/mp3_segments', callId + '_' + splitId + '.mp3')
            if os.path.exists(saveFilePath):
                print('Skipping ' + saveFilePath)
                continue

            ffmpegSplitter(audioFilePath, startTime, endTime, saveFilePath)

def getMFCC(audioFilePath, startTime, endTime):
    startTime, endTime = float(startTime), float(endTime)
    duration = endTime - startTime

    y, sr = librosa.load(audioFilePath, offset=startTime, duration=duration)
    mfcc = list(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=1)[0])

    return mfcc

def ffmpegSplitter(inFile, start, end, outFile):

    # start_sec, start_milli = [int(i) for i in start.split('.')]
    # end_sec, end_milli = [int(i) for i in end.split('.')]
    #
    # start = time.strftime("%H:%M:%S", time.gmtime(start_sec)) + '.' + str(start_milli)
    # end = time.strftime("%H:%M:%S", time.gmtime(end_sec)) + '.' + str(end_milli)

    cmdString = 'ffmpeg -i {inFile} -acodec copy -ss {start} -to {end} {outFile}'
    command = cmdString.format(inFile=inFile, start=start, end=end, outFile=outFile)

    # use subprocess to execute the command in the shell
    subprocess.call(command, shell=True)