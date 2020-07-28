import requests
from bs4 import BeautifulSoup
import datetime
import sys

class news_for_jue(object):

    def __init__(self, with_link=False, with_detail=True):
        self.list = list()
        self.with_link = with_link
        self.with_detail = with_detail
        self.url_lib = [
    'https://new.qq.com/ch/tech/',
    'https://tech.sina.com.cn/',
    'https://tech.163.com/internet',
    'https://money.163.com/'
    ]

    def detail_into_page(self, url_detail):
        tp_r = requests.get(url_detail)
        tp_r.encoding = tp_r.apparent_encoding
        tp_soup = BeautifulSoup(tp_r.text, 'html.parser')
        # get real data.
        self.list.append((tp_soup.select('.post_content_main')[0].select('h1')[0].string,
                          url_detail if self.with_link else 'N/A'))

    def to_TypeofSoup(self, input_list):
        tmp_list = list()
        for i in range(len(input_list)):
            tmp_list.append(input_list[i].select('a')[0])
        return tmp_list

    def analysis(self, TypeofSoup, with_detail=False):
        if not with_detail:
            for soup_idx in TypeofSoup:
                self.list.append((soup_idx.contents[0].string, soup_idx['href'] if self.with_link else "N/A"))
        else:
            for soup_idx in TypeofSoup:
                self.detail_into_page(soup_idx['href'])

    def get_news(self, url):
        self.r = requests.get(url)
        self.r.encoding = self.r.apparent_encoding
        self.soup = BeautifulSoup(self.r.text, 'html.parser')

        if url == self.url_lib[0]:
            pass
        elif url == self.url_lib[1]:
            self.analysis(self.soup.select(".tech-news")[0].select('a'))
            self.analysis(self.soup.select('.tech-left')[0].select('a')[-14:-11])
        elif url == self.url_lib[2]:
            self.analysis(self.soup.select(".mod_cmr_list")[0].select('a'), with_detail=self.with_detail)
            self.analysis(self.soup.select("#right_viewer")[0].select('a'), with_detail=self.with_detail)
            self.analysis(self.to_TypeofSoup(self.soup.select(".bigsize")), with_detail=self.with_detail)
        elif url == self.url_lib[3]:
            self.analysis(self.soup.select(".latest_news")[0].select('a')[2:])
        else:
            raise Exception("Undefined source.----------[*]")


def main():
    with_link = False
    with_detail = True
    print('Running now, please wait. The process takes several minutes.')
    test_instance = news_for_jue(with_link=with_link, with_detail=with_detail)

    for url in test_instance.url_lib:
        test_instance.get_news(url)

    format_tup = '{0}{1:<3}{2:<60}\t{3:<50}' if with_link else '{0}{1:<3}{2:<60}'
    sys.stdout = open('./news_%s.txt' % datetime.date.today(), mode='a', encoding='utf-8')
    for num, tup in enumerate(test_instance.list):
        if with_link:
            print(format_tup.format('内容', num, '：' + tup[0], '网址：'+tup[1]))
        else:
            print(format_tup.format('内容', num, '：' + tup[0]))

if __name__ == '__main__':
    main()

