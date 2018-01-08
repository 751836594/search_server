#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: run.py
@time: 2018/1/3 下午2:46
"""
import json
import traceback

from help.search import Search

if __name__ == '__main__':
    tree = Search()
    tree.add('你好吗')
    print(tree.search('nih'))
