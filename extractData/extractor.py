import csv
import os
from bs4 import BeautifulSoup
import enum
from urllib import request
from urllib import parse

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
        base = base.split('-')[0]

        savePath = os.path.join(outPutDir, base + '.csv')
        with open(savePath, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, ['speaker', 'words'])

            writer.writeheader()
            writer.writerows(data)

        savePathTextAlone = os.path.join(outPutDir, base + '.txt')
        with open(savePathTextAlone, 'w') as file:

            data = [line['words'] for line in data]
            for line in data:
                file.write("%s\n" % line)



def getECUrls(symbol='ms'):
    url = 'http://www.nasdaq.com/symbol/' + symbol + '/call-transcripts'
    print("Retreiving urls for " + url)

    page_whole = request.urlopen(url).read().decode('utf-8')

    page_content = BeautifulSoup(page_whole, features="html.parser")

    page_articles = page_content.find("table", {"id": "quotes_content_left_CalltranscriptsId_CallTranscripts"})

    if page_articles is None:
        print("Unable to retrive urls for " + url)
        return []

    rows = page_articles.findAll("tr")

    urls = []

    for row in rows:
        url = row.find('a')['href']

        if url.startswith('javascript') or 'earnings-call' not in url:
            continue

        url_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        story_id = url_params['StoryId']
        title = url_params['Title']

        url = 'https://seekingalpha.com/article/' + story_id + '-' + title + '?part=single'
        urls.append(url)

    return urls

def saveECUrls(fileName, urls):
    with open(fileName, 'w') as f:
        for item in urls:
            f.write("%s\n" % item)

def loadCompanies(fileName):
    with open(fileName) as f:
        content = f.readlines()

    content = [x.split('\t')[1].strip() for x in content]

    return content