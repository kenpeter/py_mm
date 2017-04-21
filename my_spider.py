# os
import os
# http request
import requests
#
import pprint

import time

# import html from lxml
from lxml import html

# global
global_page_num = 0
pp = pprint.PrettyPrinter(indent=4)

# write to file
def download_image(img_urls):
    # total img urls
    amount = len(img_urls)

    # loop
    for index, value in enumerate(img_urls, start=0):
        # file name
        filename = 'img/%s.jpg' % (index)
        # dir
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        print('--- start ---')
        print('filename: %s' % filename)
        print('Downloading: %s out of %s' % (index, amount))

        # open file
        with open(filename, 'wb') as f:
            # f write
            # time.sleep(1)
            f.write(requests.get(value).content)


def get_page_number(num):
    url = 'http://digg.com'
    response = requests.get(url).content
    selector = html.fromstring(response)

    img_urls = []
    img_urls = selector.xpath("//div[@class='digg-story__image--thumb']/a/img/@src")

    news_texts = []
    news_texts = selector.xpath("//div[@itemprop='description']/text()")

    # test
    # print('--- something ---')
    # pp.pprint(img_urls)
    # pp.pprint(news_texts)

    download_image(img_urls)

    return img_urls


if __name__ == '__main__':
    # input, page_number, everything into the var
    # page_number = input('Please enter the page number that you want to scrape:')

    # global_page_num
    # global_page_num = page_number;
    # print('hell world!');

    page_number = 4 # hardcode
    get_page_number(page_number)
