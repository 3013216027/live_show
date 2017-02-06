# -*- coding: utf-8 -*-
# @File    : zhanqi.py
# @Author  : zhengdongjian
# @Time    : 2017/1/20 下午4:43
# @Desp    :
import json
import requests
# from pyquery import PyQuery as Q
from settings import DEBUG


class Zhanqi(object):
    """
    战旗的API算是比较特殊的。。。稍微看一下不同频道的包，基本会有两种格式，
    其一为https://www.zhanqi.tv/api/static/channel.lives/xxx/yy-z.json，x频道号，y（版本号?)固定30，z页码
    其二为https://www.zhanqi.tv/api/static/v2.1/game/live/xxx/yy/z.json，和上面差不多，而且事实上线上使用这套API的都可以通过上面
    类似的API拿到数据，所以可以统一考虑用第一套API，样例接口如下：
    暴雪全部游戏https://www.zhanqi.tv/api/static/channel.lives/103/30-1.json
    炉石传说    https://www.zhanqi.tv/api/static/game.lives/9/30-1.json
    魔兽世界    https://www.zhanqi.tv/api/static/game.lives/8/30-1.json
    风暴英雄    https://www.zhanqi.tv/api/static/game.lives/21/30-1.json
    暗黑破坏神  https://www.zhanqi.tv/api/static/game.lives/68/30-1.json
    星际争霸    https://www.zhanqi.tv/api/static/game.lives/5/30-1.json
    魔兽争霸3   https://www.zhanqi.tv/api/static/game.lives/18/30-1.json

    手机游戏全部https://www.zhanqi.tv/api/static/v2.1/game/live/28/30/1.json
    三国杀移动版https://www.zhanqi.tv/api/static/v2.1/game/live/105/30/1.json
    阴阳师     https://www.zhanqi.tv/api/static/v2.1/game/live/135/30/1.json
    三国杀第二页https://www.zhanqi.tv/api/static/v2.1/game/live/13/30/2.json

    总体上，后端用的PHP，感觉接口有个地方不尽合理，举个栗子：
    请求：https://www.zhanqi.tv/api/static/game.lives/135/30-1.json，得到：
    {"code":0,"message":"","data":{"cnt":2,"rooms":[{"id":"139386","uid":"23909681","nickname":"森林呆呆","gender":"2","avatar":"https:\/\/img2.zhanqi.tv\/avatar\/d6\/009\/23909681_1465920589.jpg","code":"152553545","url":"\/sen666666","title":"新版本？？？兔子大法！.舞法天团！.","gameId":"135","spic":"https:\/\/img2.zhanqi.tv\/live\/20170120\/139386_TFwJ8_2017-01-20-17-00-55.jpg","bpic":"https:\/\/img1.zhanqi.tv\/live\/20170120\/139386_TFwJ8_2017-01-20-17-00-55_big.jpg","online":"601","status":"4","hotsLevel":"14","videoId":"139386_TFwJ8","verscr":"0","positionType":0,"gameName":"阴阳师","gameUrl":"\/games\/yinyangshi","highlight":0,"fireworks":"","fireworksHtml":""},{"id":"194325","uid":"22978672","nickname":"阳光还耀眼爱宣告","gender":"1","avatar":"https:\/\/img2.zhanqi.tv\/avatar\/f7\/d4c\/22978672_1483526398.jpg","code":"152606727","url":"\/152606727","title":"网易平台遥远之忆大区，小白一名","gameId":"135","spic":"https:\/\/img1.zhanqi.tv\/live\/20170120\/194325_si94g_2017-01-20-17-01-23.jpg","bpic":"https:\/\/img1.zhanqi.tv\/live\/20170120\/194325_si94g_2017-01-20-17-01-23_big.jpg","online":"2","status":"4","hotsLevel":"4","videoId":"194325_si94g","verscr":"0","positionType":0,"gameName":"阴阳师","gameUrl":"\/games\/yinyangshi","highlight":0,"fireworks":"","fireworksHtml":""}]}}
    增加页码，尝试请求：https://www.zhanqi.tv/api/static/game.lives/135/30-2.json，得到：
    {"code":0,"message":"","data":{"cnt":2,"rooms":[]}}
    房间总数放在了cnt上，没有看到(或者是我疏漏了)总页数，所以需要自己稍微枚举一下。
    另外，频道号采用阿拉伯数字而不是英文名，没有发现和频道名称的对应关系，所以也只好枚举频道号了，尝试枚举1-512号= =
    不过这样依然会有一个问题，频道号中有一部分是无效的，比如103号，对应的是"暴雪的所有游戏"，所以我们应该先整理出所有房间号及其观众人数，
    去重后再累加= =
    """
    url = 'https://www.zhanqi.tv/api/static/game.lives/{cla}/30-{page}.json'

    @staticmethod
    def fetch(url):
        """
        fetch html data with url
        :param url: the page url
        :return: a array with room data
        """
        html_data = requests.get(url)
        html_data = html_data.content
        html_data = json.loads(html_data)
        return html_data['data']['rooms']

    @staticmethod
    def work():
        """
        handle
        :return: number of watchers
        """
        data = {}
        for cla in range(1, 513):  # [1, 512]
            if DEBUG:
                print('[Zhanqi.work]check channel %s' % cla)
            page = 1
            while True:
                rooms = Zhanqi.fetch(Zhanqi.url.format(cla=cla, page=page))
                if not rooms:
                    break
                for room in rooms:
                    data[room['id']] = room['online']
                page += 1
        return sum(map(int, data.values()))


if __name__ == '__main__':
    print('ZhanqiTV = %s' % Zhanqi.work())
