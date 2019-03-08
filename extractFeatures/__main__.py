from extractFeatures import aligner, splitter, mfcc


if __name__ == '__main__':

    # aligner.getAlignmentBatch('extractFeatures/mp3', 'extractData/out', 'extractFeatures/out')

    # splitter.splitAllInDir('extractFeatures/out')
    #
    mfcc.extractAllInDir('extractFeatures/out')
