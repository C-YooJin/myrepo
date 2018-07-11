import pandas as pd
import os



def filechecker(f, sep, encoding):
    try:
        df = pd.read_csv(f, sep=sep, encoding=encoding)
        print(df.shape)
    except:
        print('format / sep / encoding problem')

def split(f, sep, chunksize):
    '''
    for csv files that are too large
    '''
    filename = os.path.splitext(f)[0]
    for i,chunk in enumerate(pd.read_csv(f, sep=sep, chunksize=chunksize)):
        chunk.to_csv(filename+'_chunk({0:03d}).csv'.format(i+1), encoding='utf-8')

f = '/Users/user/Downloads/partner_list_message_output.csv'
# filechecker('/Users/user/Downloads/partner_list_message_output.csv', '\t', 'utf-8')
# split(f, '\t', 500000)