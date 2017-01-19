# -*- coding: utf-8 -*-
# @File    : panda.py
# @Author  : zhengdongjian
# @Time    : 2017/1/19 下午10:30
# @Desp    :
import json
import requests


class Panda(object):
    """
    检查熊猫TV全平台观众人数
    """
    @staticmethod
    def fetch(url):
        """
        =.=
        """
        html_data = requests.get(url)
        html_data = html_data.content
        html_data = json.loads(html_data)
        return html_data['data']

    @staticmethod
    def count():
        """
        o.o
        """
        url = 'http://www.panda.tv/ajax_sort?token=6f53df41fbc278569c8dfe4e7f5b2b09&pageno={pageno}&pagenum=120&classification={cla}&_=1484831614936'
        classifications = ['lol', 'yzdr', 'overwatch', 'hwzb', 'hearthstone', 'zhuji', 'deadbydaylight', 'starve', 'dota2', 'war3', 'dnf', 'cf', 'wow', 'csgo', 'diablo3', 'heroes', 'spg', 'mc', 'ftg', 'kof97', 'jxol3', 'tymyd', 'liufang', 'hjjd', 'pokemon', 'popkart', 'foreigngames', 'starcraft', 'wy', 'music', 'shoot', 'pets', 'kingglory', 'ro', 'yys', 'mobilegame', 'fishes', 'clashroyale', 'qipai', 'boardgames', 'cartoon', 'technology', 'finance']
        sum_fans = 0
        for cla in classifications:
            print('check PandaTV.%s' % cla)
            total = int(Panda.fetch(url.format(cla=cla, pageno=1))['total'])
            cur = 0
            pageno = 1
            while cur < total:
                data = Panda.fetch(url.format(cla=cla, pageno=pageno))
                items = data['items']
                # print(json.dumps(items, ensure_ascii=False, indent=2))
                for room in items:
                    # print(room['id'], room['person_num'])
                    sum_fans += int(room['person_num'])
                pageno += 1
                cur += 120
        return sum_fans


if __name__ == '__main__':
    Panda.work()
