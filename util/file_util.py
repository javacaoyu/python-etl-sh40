# coding:utf8
"""
文件相关工具方法
"""


def get_new_by_two_list_compare(big_list, small_list):
    """
    获取big_list中有的，small_list中没有的
    :param big_list: 应当是内容多的那一个
    :param small_list: 应当是内容少的那一个
    :return: 新内容的list
    """
    tmp_list = []
    for i in big_list:
        if i not in small_list:
            tmp_list.append(i)

    return tmp_list
