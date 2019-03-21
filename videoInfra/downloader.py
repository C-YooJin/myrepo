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
    :return: vodid, video download url
    """
    headers = {'VOD-SERVICE-KEY': '95c3433c-2b75-11e8-bc84-1272ebab0b70'}
    response = requests.get(API+vodid, headers=headers)
    destUrl = json.loads(response.text)['destUrl']
    return vodid.strip(), destUrl.strip()


def download(vodid, url, path, i):
    """
    :param vodid: original video id
    :param url: video url from video infra API
    :param path: download path
    :param i: increment with duplicates
    :return: None. downaloads and logs
    """
    errorlog = os.path.splitext(path)[0]+'.errorlog'
    downloadlog = os.path.splitext(path)[0] + '.log'
    suffix = '_dup_'
    
    if os.path.exists(path+'/%s'%(url.split('/')[-1])):
        with open(errorlog, 'a') as w:
            w.write('duplicate: %s,%s'%(vodid, url)+'\n')
        path = path + '/%s'%(url.split('/')[-1].split('.')[0])+suffix+'(%d)'%i+'.mp4'
        i += 1
    else:
        path = path + '/%s' % (url.split('/')[-1])

    try:
        print("downloading %s from %s"%(vodid, url))
        print(path)
        urllib.request.urlretrieve(url, path)
        with open(downloadlog, 'a') as w:
            w.write(vodid +',' + url+'\n')
    except:
        with open(errorlog, 'a') as w:
            w.write(vodid + ',' + url + '\n')
    return i


def get_vid(urlfile, path):
    with open(urlfile, 'r') as f:
        vodids = f.readlines()[1:]
        i = 0
        for vodid in tqdm(vodids):
            vodid, destUrl = get_url(vodid)
            i = download(vodid, destUrl, path, i)
    print('done')
    print('duplicates : %d'%i)


if __name__ == '__main__':
    filename = sys.argv[1]
    #filename = 'bts_alone.csv'
    path = os.getcwd() + '/' + os.path.splitext(filename)[0]
    if not os.path.exists(path):
        os.mkdir(path)

    get_list(filename)
    get_vid(filename+'.vids', path)
