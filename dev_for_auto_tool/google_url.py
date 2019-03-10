import base64
from collections import OrderedDict

from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
from six.moves.urllib.parse import urlparse


class MyImageDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_real = OrderedDict()
        url_path = urlparse(task['file_url'])[2]
        #print(task['file_url'])
        url_real['url'] = task['file_url']
        # print(url_real)
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        filename = base64.b64encode(url_path.encode()).decode()
        url_real['file_name'] = '{}.{}'.format(filename, extension)
        print(url_real)
        return '{}.{}'.format(filename, extension)

def get_json(keyword, save, num):
    google_crawler = GoogleImageCrawler(
        downloader_cls=MyImageDownloader,
        downloader_threads=4,
        storage={'root_dir': save})
    google_crawler.crawl(keyword=keyword, max_num=num)         # num값 받아와야됨

get_json('sugar glider', '/Users/user/Downloads/url_test', 1000)