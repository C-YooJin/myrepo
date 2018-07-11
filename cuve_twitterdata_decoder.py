'''
Cuve Document (twitter) Data Decoder
 - when dumped in json format, 'data' part in unreadable
 - cuve document's 'data' part is encded in base64
 - have to decode 'data' part to make it readable within json format
'''

import json
import base64

def getJsonList(file):
    json_list = []
    for line in open(f, 'r'):
        json_list.append(json.loads(line))
    return json_list

def decodeText(json_list):
    decoded = []
    for jsdoc in json_list:
        # filter only the documents in Korean
        if jsdoc['contentMap']['syndiMeta']['metaMap']['userLang'] == 'ko':
            base64_string = base64.b64decode(jsdoc['contentMap']['syndiContentInfo']['data']).decode('utf-8')
            jsdoc['contentMap']['syndiContentInfo']['data'] = base64_string
            decoded.append(jsdoc)
    return decoded


f =  '/Users/user/Documents/DATA_preprocessed/syndiinfo/twitter.web_doc.20180430000000-20180430000100.00000'

json_list = getJsonList(f)
decoded = decodeText(json_list)

