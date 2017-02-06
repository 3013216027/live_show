# -*- coding: utf-8 -*-
# @File    : douyu.py
# @Author  : zhengdongjian
# @Time    : 2017/1/19 下午10:32
# @Desp    :
import json
import requests
from pyquery import PyQuery as Q
from settings import DEBUG


class Douyu(object):
    """
    斗鱼TV采用的是后端模板渲染的形式，所以需要自己解析页面结构
    """
    base_url = 'https://www.douyu.com/directory/'
    url = base_url + 'game/{cla}?page={page}'

    @staticmethod
    def fetch(url):
        """
        fetch html data with url
        :param url: the page url
        :return: a jQuery-like document
        """
        return Q(url=url)

    @staticmethod
    def work():
        """
        handle
        :return: number of watchers
        """
        # Step 1. get all classifications
        home = Douyu.fetch(Douyu.base_url)
        clas = home('.unit a')
        sum_fans = 0
        for item in clas:
            cla = item.get('href').split('/')[-1]
            sub_url = Douyu.url.format(cla=cla, page=1)
            game_home = Douyu.fetch(sub_url)  # 游戏子页面
            page_count_tag = game_home('.tag_list a')
            if not page_count_tag:
                continue
            page_count = int(page_count_tag[0].get('data-pagecount'))
            if DEBUG:
                print('check Douyu.%s, page_count = %s' % (cla, page_count))
            fans = 0
            for page in range(1, page_count + 1):
                game_page = Douyu.fetch(Douyu.url.format(cla=cla, page=page))
                nums = game_page('.dy-num.fr')
                for num_text in nums:
                    num = num_text.text
                    if num.find(u'万') != -1:
                        fans += int(float(num.rstrip(u'万')) * 10000)
                    else:
                        fans += int(num)
            sum_fans += fans
            if DEBUG:
                print('Douyu.%s = %s' % (cla, fans))
        return sum_fans


if __name__ == '__main__':
    print('DouyuTV = %s' % Douyu.work())
