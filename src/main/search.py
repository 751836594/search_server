#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: search.py
@time: 2018/1/3 下午2:47
"""


class Search:
    def __init__(self):
        self.tree = {}

    def add(self, word):
        """
        增加搜索关键字
        :param word:
        :return:
        """
        word_info = self._han2pinyin(word)

    @staticmethod
    def _han2pinyin(word):
        """
        中文转英文,这里用的是python-pinyin
        github地址:https://github.com/mozillazg/python-pinyin
        :param word:
        :return:
        """