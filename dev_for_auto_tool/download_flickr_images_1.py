# First, you should install flickrapi
# pip install flickrapi
import flickrapi
import urllib.request
import os
import argparse
import time
import datetime


def download(photos, url_type, start_idx, save_dir):
    # Get urls
    start_time = time.time()
    urls = []
    for i, photo in enumerate(photos):
        try:
            url = photo.get(url_type)
            urls.append(url)

            if (i+1) % 1000 == 0:
                et = time.time() - start_time
                et = str(datetime.timedelta(seconds=et))[:-7]
                print('[GET {}] Elapsed [{}] Progress [{}]..!'.format(url_type, et, i+1))

            if (i+1) > 10000:
                break
        except:
            print('error occured..')

    # Download images
    urls = [url for url in urls if url is not None]
    urls = list(set(urls))    
    for i, url in enumerate(urls):
        try:
            filename = '{:06d}.jpg'.format(start_idx+i+1)
            save_path = os.path.join(save_dir, filename, urls) # 수정포인트(1) filename과 urls 저장하도록 수정
            urllib.request.urlretrieve(url, save_path)

            if (i+1) % 100 == 0:
                et = time.time() - start_time
                et = str(datetime.timedelta(seconds=et))[:-7]
                print('[DOWNLOAD {}] Elapsed [{}] Progress [{}/{}]..!'.format(url_type, et, i+1, len(urls)))
        except:
            print('error occured..')

    return len(urls)


def main(config):
    if not os.path.exists(config.save_dir):
        os.makedirs(config.save_dir)

    # Flickr api access key
    flickr=flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)
    
    keyword = config.target_class
    
    num_images = 0  #  이미지 개수
    for url_type in ['url_k', 'url_h', 'url_o']:  # https://www.flickr.com/services/api/misc.urls.html
        photos = flickr.walk(text=keyword,
                             tag_mode='all',
                             tags=keyword,
                             extras=url_type,
                             per_page=config.per_page,
                             sort='relevance')
        
        num_images = download(photos, url_type, start_idx=num_images, save_dir=config.save_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='/Users/user/Documents/document/flickr_test') # 수정포인트(2) dir 수정
    parser.add_argument('--target_class', type=str, default='white tiger')
    parser.add_argument('--per_page', type=int, default=500)
    
    
    config = parser.parse_args()
    print(config)
    main(config)
    
# python download_flickr_images.py --save_dir images_flickr/siberian_husky --target_class 'siberian husky'