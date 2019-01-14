import pandas as pd
import re


def findorigin(id, origin):
    pattern = r'([^\n]+%s[^\n]+)'%str(id)
    with open(origin, 'r') as f:
        text = f.read()
        matches = re.findall(pattern, text)
        if not matches:
            print("no match id %s"%str(id))
        elif len(matches) > 1:
            print("error with origin id %s"%str(id))
            return matches[0]
        else:
            return matches[0]

def findreply(id, reply):
    pattern = r'([^\n]+%s[^\n]+)'%str(id)
    with open(reply, 'r') as f:
        text = f.read()
        matches = re.findall(pattern, text)
        if not matches:
            print("no match id %s"%str(id))
        elif len(matches) > 1:
            print("error with reply id %s"%str(id))
            return matches[0]
        else:
            return matches[0]

def reformat(file, origin, reply):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        origin_json = findorigin(row[1], origin)
        reply_json = findreply(row[3], reply)
        with open('test_data', 'a') as w:
            w.write(origin_json+'\n')
        with open('test_label', 'a') as m:
            m.write(reply_json+'\n')


if __name__ == '__main__':
    file = 'contextReply_idfixed.xlsx'
    origin = 'original_post'
    reply = 'reply_post'
    reformat(file, origin, reply)
