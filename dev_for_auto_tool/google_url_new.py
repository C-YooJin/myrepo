from collections import OrderedDict
from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
from six.moves.urllib.parse import urlparse
import base64
import os
import json


class MyImageDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_real = OrderedDict()
        url_idx = 0


        for i in range(10):
            url_real[i] = OrderedDict()

            # 여기부터는 파일명.jpg를 만들기 위한 코드
            url_path = urlparse(task['file_url'])[2]
            if '.' in url_path:
                extension = url_path.split('.')[-1]
                if extension.lower() not in [
                        'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
                ]:
                    extension = default_ext
            else:
                extension = default_ext
            filename = base64.b64encode(url_path.encode()).decode()

            # add to dict
            url_real[i]['url'] = task['file_url']
            url_real[i]['file_name'] = '{}.{}'.format(filename, extension)
        # print(url_real)

        with open('/Users/user/Downloads/url_test' + '/url_result.json', 'w', encoding="utf-8") as make_file:
            json.dump(url_real, make_file, ensure_ascii=False, indent="\t")

        # print(url_real)
        return '{}.{}'.format(filename, extension)

def get_json(keyword, save, num):

    if not os.path.exists(save):
        os.makedirs(save)

    google_crawler = GoogleImageCrawler(
        downloader_cls=MyImageDownloader,
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=4,
        storage={'root_dir': save})

    google_crawler.crawl(keyword=keyword,
                         max_num=num)         # num값 받아와야됨

get_json('sugar glider', '/Users/user/Downloads/url_test', 500)