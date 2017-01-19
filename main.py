# -*- coding: utf-8 -*-
# @File    : main.py
# @Author  : zhengdongjian
# @Time    : 2017/1/19 下午10:29
# @Desp    : 
from panda import Panda
from douyu import Douyu


if __name__ == '__main__':
    print('PandaTV = %s' % Panda.work())
    print('DouyuTV = %s' % Douyu.work())
