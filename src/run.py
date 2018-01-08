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


def test_demo():
    search = Search()
    search.add('你是谁')

    assert {} != search.search('你')
    assert {} != search.search('你s')
    assert {} != search.search('ni是s')


if __name__ == '__main__':
    pass
