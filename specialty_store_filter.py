import json
import base64
import xml.etree.ElementTree as ET
import os
import urllib.request
from pprint import pprint


def getJsonList(file):
    json_list = []
    for line in open(file, 'r'):
        json_list.append(json.loads(line))
    return json_list


def filteroutlet(json_list):
    refined_list = []
    for jsdoc in json_list:
        base64_string = base64.b64decode(jsdoc['contentMap']['internalContentInfo']['data']).decode('utf-8')
        root = ET.fromstring(base64_string)
        if root.find('vertical').text == 'OUTLET':
        #jsdoc['contentMap']['syndiContentInfo']['data'] = base64_string
            refined_list.append(jsdoc)
        return refined_list


def findimageurls(jsdoc):
    one = base64.b64decode(jsdoc['contentMap']['internalImageInfo']['data']).decode('utf-8')
    root = ET.fromstring(one)
    s = root.iter()
    for i in s:
        new = i.findall('org-img-url')
        if new:
            aurl = new[0].text
    return aurl


def savelink2text(urlfilename):
    with open(urlfilename, 'w') as w:
        for item in refined_list:
            aurl = findimageurls(item)
            w.write(aurl+'\n')


def downloadimage(url, download_path):
    try:
        urllib.request.urlretrieve(line, download_path)
    except:
        print('error' + url)



if __name__ == '__main__':

    localpath = '/Users/user/Downloads/commerce_image2/'
    prefix = 'outlet_image'
    if not os.path.isdir(localpath):
        os.mkdir(localpath)

    f =  '/Users/user/cuve-reader-3.6.10/download/commerce2/'


    for name in os.listdir(f):
        file = f+name
        json_list = getJsonList(file)
    refined_list = filteroutlet(json_list)
    savelink2text('alllinks.txt')


    with open('alllinks.txt', 'r') as f:
        i = 0
        for line in f:
            all = f.read().splitlines()
        for line in all:
            img_download_path = localpath + '{0}({1}).jpg'.format(prefix, i)
            downloadimage(line, img_download_path)
            i += 1
