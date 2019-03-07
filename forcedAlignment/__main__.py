from forcedAlignment import aligner, splitter, mfcc


if __name__ == '__main__':

    # aligner.getAlignmentBatch('forcedAlignment/mp3', 'extractData/out', 'forcedAlignment/out')

    # splitter.splitAllInDir('forcedAlignment/out')

    mfcc.extractAllInDir('forcedAlignment/out')
