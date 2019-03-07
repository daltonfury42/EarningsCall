import argparse

from extractData import extractor
from extractData.urls import fetcher

def extractDataAlone(args):
    dataWithFileName = extractor.readDataFromDir(args.indir)
    extractor.writeToCSV(args.outdir, dataWithFileName)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program to extract data from html files')
    parser.add_argument('--indir', help='Directory to read files from', required=True)
    parser.add_argument('--outdir', help='Directory to read files from', required=True)
    args = parser.parse_args()

    #fetcher.fetchFromCompanies()

    extractDataAlone(args)


