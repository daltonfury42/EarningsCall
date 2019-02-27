import csv
import os
from bs4 import BeautifulSoup
import enum

class Section(enum.Enum):
    COMPANY_PARTICIPANTS = 0
    CONF_CALL_PARTICIPANTS = 1
    COMPANY_SPEAKS  = 3
    Q_N_A = 4

def readDataFromDir(inDir):
    dataWithFileName = []

    for fileName in os.listdir(inDir):
        fullPath = os.path.join(inDir, fileName)
        processedData = readData(fullPath)
        dataWithFileName.append((fileName, processedData))

    return dataWithFileName

def readData(fileName):
    print("Processing " + fileName)
    with open(fileName, 'r') as f:
        webpage = f.read()

    page_content = BeautifulSoup(webpage, features="html.parser")
    page_articles = page_content.find("div", {"id": "a-body"})

    paragraphs = page_articles.findAll("p")

    speaker = None
    processedData = []

    for para in paragraphs[1:]:
        if para.find("strong") is not None:
            text = para.find("strong").text
            if text not in ['Company Participants', 'Conference Call Participants', 'Question-and-Answer Session']:
                speaker = text
        else:
            if speaker is not None:
                dataPoint = {'speaker': speaker, 'words': para.text}
                processedData.append(dataPoint)

    return processedData

def writeToCSV(outPutDir, dataWithFileName):
    for fileName, data in dataWithFileName:
        base, ext = os.path.splitext(fileName)
        savePath = os.path.join(outPutDir, base + '.csv')
        with open(savePath, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, ['speaker', 'words'])

            writer.writeheader()
            writer.writerows(data)
