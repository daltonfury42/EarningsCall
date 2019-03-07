from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

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

def fetchFromCompanies():
    companies = loadCompanies('urls/companies.txt')

    urls = []
    for company in companies:
        urls += getECUrls(company.lower())
    saveECUrls('urls.txt', urls)
    exit(-1)
