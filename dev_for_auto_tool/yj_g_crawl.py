from icrawler.builtin import GoogleImageCrawler
from datetime import date
import os
import argparse


def main(config):
    if not os.path.exists(config.save_dir):
        os.makedirs(config.save_dir)

    # 현재 크롤링 된 데이터 수
    num_of_data = next(os.walk(config.save_dir))[2]  # dir is your directory path as string

    # 2010년 1월부터 크롤링
    years = 2010
    months = 1

    while len(num_of_data) < config.num:

        google_crawler = GoogleImageCrawler(
            feeder_threads=1,
            parser_threads=2,
            downloader_threads=4,
            storage={'root_dir': config.save_dir})

        for year in range(years, years + 1):
            for month in [months]:
                filters = dict(
                    size='large',
                    type='photo',
                    date=((year, month, 1), (year, month + 2, 30)))

                google_crawler.crawl(keyword=config.target_class,
                                     filters=filters,
                                     max_num=config.num+200,
                                     file_idx_offset='auto',
                                     min_size=(512, 512))

        # directory에 저장된 파일 수
        num_of_data = next(os.walk(config.save_dir))[2]

        # next year
        # repeat 1, 4, 7, 10 month
        if months == 10:
            years += 1
            months = 1
        else:
            months += 3

        print('year: {}, month: {}~{} finished..!'.format(years, months, months + 2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_class', type=str, default='dog', help='keyword to crawl images from google')
    parser.add_argument('--save_dir', type=str, default='/Users/user/Downloads/loop_test',
                        help='directory where images are downloaded')
    parser.add_argument('--max_num', type=int, default=1000, help='maximum number of images to download')
    parser.add_argument('--num', type=int, default=100)

    config = parser.parse_args()
    print(config)
    main(config)