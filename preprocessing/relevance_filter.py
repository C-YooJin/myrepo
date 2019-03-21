import pandas as pd
import glob
import csv
from io import StringIO

def csvfilelist(path):
    files = glob.glob(path + '/**/*.csv', recursive=True)
    return files

def filter_relevance(file):
   ''' couldn't parse with pandas. issue from using excel
       instead getting all the '1's by going through each line and getting the last element except for \n'''
    starter = set()
    RELEVANT = 1
    with open(file, 'r', encoding='ISO-8859-1') as f:
        text = f.readlines()
    for line in text:
        if line[-2]=='1':
            reader = csv.reader(StringIO(line))
            item = list(reader)[0][2]
            starter.add(item)
    return list(starter)

def get_originals(files, outfile):
    with open(outfile, 'a') as w:
        for file in files:
            with open(file, 'r', ) as f:
                w.write(f.read())

def find_original(starter, originalsfile, finalfile):
    RELEVANTID = []
    df = pd.read_csv(originalsfile)
    for item in starter:
        row = df.loc[(df['conversationA'] == item)].values
        try:
            originid = str(row[0][0])
            replyid = str(row[0][1])
            conversationA = '"'+str(row[0][2])+'"'
            conversationB = '"'+str(row[0][3])+'"'
        except:
            pass

        writenewfile(originid, replyid, conversationA, conversationB, finalfile)

def writenewfile(originid, replyid, conversationA, conversationB, finalfile):
    with open(finalfile, 'a', encoding='utf-8') as w:
        w.write(','.join([originid, replyid, conversationA, conversationB, '']) + '\n')


if __name__ == '__main__':
    #path = sys.argv[1]
    path = 'results'
    outfile = 'concat.csv'
    finalfile = '0227_labelcheck_fixed.csv'
    files = csvfilelist(path)
    ALL = []
    for file in files:
        starter = filter_relevance(file)
        ALL += starter
    with open(finalfile, 'w', encoding='utf-8') as w:
        w.write(','.join(['originid', 'replyid', 'conversationA', 'conversationB', 'relevance']) + '\n')
    find_original(ALL, outfile, finalfile)

