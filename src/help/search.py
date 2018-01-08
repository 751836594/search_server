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
import json
import re
import traceback

from pypinyin import FINALS
from pypinyin import INITIALS
from pypinyin import lazy_pinyin


class Search:
    """
    全局节点id
    """
    node_id = 0

    def __init__(self):
        self.tree = {0: {'id': 0, 'map': {}}}

    def add(self, word):
        """
        增加搜索关键字
        :param word:
        :return:
        """
        # 搜索关键字转换
        word_info = self._han2pinyin(word)

        self._add_child(word_info, 0)

    @staticmethod
    def _han2pinyin(word):
        """
        例1:你好吗 => (('你', 'n', 'i'), ('好', 'h', 'ao'), ('吗', 'm', 'a'))
        例2:你hao吗 => (('你', 'n', 'i'), ('hao', '', ''), ('吗', 'm', 'a'))

        中文转英文,这里用的是python-pinyin

        github地址:https://github.com/mozillazg/python-pinyin

        :param word:
        :return:
        """
        arr2 = re.findall('([\u4e00-\u9fa5]+|[a-zA-Z0-9]+)', word)
        all_result = []
        for item in arr2:
            if re.match('[\u4e00-\u9fa5]+', item):
                quan = lazy_pinyin(item)
                sheng = lazy_pinyin(item, style=INITIALS)
                yun = lazy_pinyin(item, style=FINALS)
                full_pinyin = lazy_pinyin(item)
                for k, s in enumerate(sheng):
                    # 判断是否声母为空
                    if s == '':
                        sheng[k] = full_pinyin[k][0]
                        yun[k] = full_pinyin[k][1:]
                        # 判断拼接后的声韵母 是否等于 全拼的声韵母
                        if sheng[k] + yun[k] != quan[k]:
                            l = len(sheng[k])
                            yun[k] = quan[k][l:]
                    else:
                        # 判断拼接后的声韵母 是否等于 全拼的声韵母
                        if s + yun[k] != quan[k]:
                            l = len(sheng[k])
                            yun[k] = quan[k][l:]

                all_result.extend(zip(item, sheng, yun))
            else:
                all_result.extend([(item, '', '')])

        return tuple(all_result)

    def _add_child(self, word_info, prev_id):
        """
        递归新增节点
        :param word_info:
        :param prev_id:
        :return:
        """
        if len(word_info) == 0:
            return

        single = word_info[0]  # 单个字的中文,声母,韵母的元祖 例:('你','n','i')
        han = single[0]
        sheng = single[1]
        yun = single[2]

        self._add_tree(han, word_info[1:], prev_id)
        self._add_tree(sheng, word_info[1:], prev_id)
        self._add_tree(sheng + yun, word_info[1:], prev_id)

    def _add_tree(self, word, word_info, prev_id):
        """
        新增节点逻辑
        :param word: 例如:'你'或'n'或'ni'
        :param word_info: 剩余元祖
        :param prev_id: 上一个关联节点id
        :return:
        """
        cur_tree = self.tree[prev_id]
        for kw in word:
            if kw not in cur_tree['map']:
                self.node_id += 1
                cur_id = self._push(cur_tree['id'], kw)
            else:
                cur_id = cur_tree['map'][kw]
            cur_tree = self.tree[cur_id]
        self._add_child(word_info, cur_tree['id'])

    def _push(self, prev_id, kw):
        """
        新增节点
        :param prev_id: 上一个关联节点id
        :param kw: 例如:'你'或'n'或'ni'
        :return: 返回新建节点id
        """
        cur_id = self.node_id
        self.tree[prev_id]['map'][kw] = cur_id
        self.tree[cur_id] = {'id': cur_id, 'map': {}}
        return cur_id

    def search(self, kw):
        """
        递归查询结果
        :param kw:
        :return:
        """
        if not kw:
            return {}
        kw = self._filter(kw)
        cur_tree = self.tree[0]
        for key in kw:
            if key not in cur_tree['map']:
                return {}

            cur_id = cur_tree['map'][key]
            cur_tree = self.tree[cur_id]
        return cur_tree

    @staticmethod
    def _filter(kw):
        """
        过滤
        :param kw:
        :return:
        """
        res = re.findall('([\u4e00-\u9fa5]+|[a-zA-Z0-9]+)', kw)
        return ''.join(res)
