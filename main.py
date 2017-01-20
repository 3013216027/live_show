# -*- coding: utf-8 -*-
# @File    : main.py
# @Author  : zhengdongjian
# @Time    : 2017/1/19 下午10:29
# @Desp    : 
from panda import Panda
from douyu import Douyu
from zhanqi import Zhanqi
from datetime import datetime

if __name__ == '__main__':
    count_panda = Panda.work()
    count_douyu = Douyu.work()
    count_zhanqi = Zhanqi.work()
    count_all = count_panda + count_douyu + count_zhanqi
    ti = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('Time: %s' % ti)
    print('PandaTV = %s' % count_panda)
    print('DouyuTV = %s' % count_douyu)
    print('ZhanqiTV = %s' % count_zhanqi)
    print('Totally = %s' % count_all)
