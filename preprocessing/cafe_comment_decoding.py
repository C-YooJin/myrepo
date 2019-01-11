# naver cafe comments data
# it will convert json file to xml file
# decoding with 'utf-8'
# we use 'comment' tag

import json
import base64
import re
import sys

def decoding(filepath):
    with open(filepath) as f:
        with open('%s_output'%filepath, 'a') as w:
            for line in f:
                data = json.loads(line)
                base64_str = base64.b64decode(data['contentMap']['internalContentInfo']['data']).decode('utf-8')
                p = re.compile('<comment>([.\s\S]*?)</comment>')
                result = p.findall(base64_str)
                if result:
                    w.write(result[0]+'\n')

    #print(comment_lst, '\n')
    #return comment_lst

#f = 'naver_cafe.article_comment.20181001000000-20181101000000.00000'
if __name__ == '__main__':
    f = sys.argv[1]
    decoding(f)


