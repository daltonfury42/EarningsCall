import csv
import os
import subprocess
import time

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
        for splitId, startTime, endTime, _ in csvreader:
            saveFilePath = os.path.join('forcedAlignment/mp3_segments', callId + '_' + splitId + '.mp3')
            if os.path.exists(saveFilePath):
                print('Skipping ' + saveFilePath)
                continue

            ffmpegSplitter(audioFilePath, startTime, endTime, saveFilePath)


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