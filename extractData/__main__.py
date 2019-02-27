import argparse

from extractData import extractor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program to extract data from html files')
    parser.add_argument('--indir', help='Directory to read files from', required=True)
    parser.add_argument('--outdir', help='Directory to read files from', required=True)
    args = parser.parse_args()

    companies = extractor.loadCompanies('companies.txt')

    urls = []
    for company in companies:
        urls += extractor.getECUrls(company.lower())
    saveUrls = extractor.saveECUrls('urls.txt', urls)
    exit(-1)
    dataWithFileName = extractor.readDataFromDir(args.indir)
    extractor.writeToCSV(args.outdir, dataWithFileName)