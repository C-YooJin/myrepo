# pip install icrawler
from icrawler.builtin import GoogleImageCrawler
from datetime import date
import os
import argparse


def main(config):

    if not os.path.exists(config.save_dir):
        os.makedirs(config.save_dir)

    google_crawler = GoogleImageCrawler(
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=4,
        storage={'root_dir': config.save_dir})
    
    for year in range(2018, 2018+1):
        for month in [1, 4, 7, 10]:
            filters = dict(
                size='large',
                type='photo',
                date=((year, month, 1), (year, month+2, 30)))

            google_crawler.crawl(keyword=config.target_class,
                                filters=filters,
                                max_num=config.max_num,
                                file_idx_offset='auto',
                                min_size=(512, 512))
        
        print('year: {}, month: {}~{} finished..!'.format(year, month, month+2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_class', type=str, default='dog', help='keyword to crawl images from google')
    parser.add_argument('--save_dir', type=str, default='/Users/user/Documents/document/test', help='directory where images are downloaded')
    parser.add_argument('--max_num', type=int, default=10, help='maximum number of images to download')
    
    config = parser.parse_args()
    print(config)
    main(config)