import csv
from tqdm import tqdm
import requests
import sys
import json
import urllib.request
import os

"""
from command line : python main.py {csv file with video id}
gets vod ID list from csv file and gets urls from video infra API
then downloads videos from urls
"""

# video infra api
API = 'http://play.rmcnmv.naver.com/vod/downloadUrl/v2.0/videos/'


def get_list(filename):
    """
    :param filename: csv file name
    :return: None. saves url list as a result
    """
    with open(filename, 'r') as f:
        with open(filename+'.vids', 'a') as w:
            reader = csv.reader(f)
            for row in reader:
                vodid = row[5]
                w.write(vodid+'\n')


def get_url(vodid):
    """
    :param vodid: master video id from csv file(given)
    :return: video download url
    """
    headers = {'VOD-SERVICE-KEY': '95c3433c-2b75-11e8-bc84-1272ebab0b70'}
    response = requests.get(API+vodid, headers=headers)
    destUrl = json.loads(response.text)['destUrl']
    return destUrl


def download(vodid, url, path):
    """
    :param vodid: original video id
    :param url: video url from video infra API
    :param path: download path
    :return: None. downloads and logs
    """
    errorlog = os.path.splitext(path)[0]+'.errorlog'
    downloadlog = os.path.splitext(path)[0] + '.log'
    path = path+'/%s'%(url.split('/')[-1])
    try:
        print("downloading %s from %s"%(vodid, url))
        print(path)
        urllib.request.urlretrieve(url, path)
        with open(downloadlog, 'a') as w:
            w.write('\t'.join([vodid, url])+'\n')
    except:
        with open(errorlog, 'a') as w:
            w.write('\t'.join([vodid, url])+'\n')


def get_vid(urlfile, path):
    """
    :param urlfile: url file generated from get_url()
    :param path: download directory
    :return: None.
    """
    with open(urlfile, 'r') as f:
        vodids = f.readlines()[1:]
        for vodid in tqdm(vodids):
            destUrl = get_url(vodid)
            download(vodid, destUrl, path)


if __name__ == '__main__':
    filename = sys.argv[1]
    #filename = 'bts_alone.csv'
    path = os.getcwd() + '/' + os.path.splitext(filename)[0]
    if not os.path.exists(path):
        os.mkdir(path)

    get_list(filename)
    get_vid(filename+'.vids', path)
