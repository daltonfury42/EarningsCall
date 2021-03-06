import csv
import os
from bs4 import BeautifulSoup


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

    section = 'announcement'

    for para in paragraphs[1:]:
        if para.find("strong") is not None:
            text = para.find("strong").text
            if text not in ['Company Participants', 'Conference Call Participants', 'Question-and-Answer Session']:
                speaker = text
            elif text == 'Question-and-Answer Session':
                section = 'qna'
        else:
            if speaker is not None and speaker not in ['Executives', 'Analysts']:
                dataPoint = {'section': section, 'speaker': speaker, 'words': para.text}
                processedData.append(dataPoint)

    return processedData


def writeToCSV(outPutDir, dataWithFileName):
    for fileName, data in dataWithFileName:
        base, ext = os.path.splitext(fileName)
        # base = base.split('-')[0]

        savePath = os.path.join(outPutDir, base + '.csv')
        with open(savePath, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, ['section', 'speaker', 'words'])

            # writer.writeheader()
            writer.writerows(data)

        savePathTextAlone = os.path.join(outPutDir, base + '.txt')
        with open(savePathTextAlone, 'w') as file:

            data = [line['words'] for line in data]
            for line in data:
                file.write("%s\n" % line)



