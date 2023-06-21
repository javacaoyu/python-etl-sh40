# coding:utf8
"""
字符串相关工具方法
"""

def check_null(data) -> bool:
    """
    检查传入的变量是否是无意义的内容。
    无意义的定义是：
    - 空字符串
    - NULL
    - None
    - undefined
    :param data: 被判断的变量
    :return: True就是无意义，False就是有意义
    """
    if not data:
        # 如果data是None，直接返回无意义，也就是True
        return True

    # 为了避免大小写的问题，统一转小写（大写也行随意）
    data = str(data).lower()

    if data == "" or data == "null" or data == 'none' or data == 'undefined':
        return True

    return False


def check_null_and_transform_to_sql_null(data) -> str:
    """
    检查字符串内容是否是无意义，如果是返回NULL字符串，如果不是返回本身，同时外面包上''
    :param data: 被判断的字符串
    :return: 字符串，NULL或data本身（包上'')
    """
    if check_null(data):
        # 如果进来表示无意义
        return "NULL"

    return "'" + str(data) + "'"


def check_number_null_and_transform_to_sql_null(data):
    """
    检查数字内容是否是无意义，如果是返回NULL字符串，如果不是返回本身
    :param data: 被判断的字符串
    :return: NULL或data本身
    """
    if check_null(data):
        # 如果进来表示无意义
        return "NULL"

    return data


def clean_str(data):
    """
    清理字符串中一些自带的' " $ # \ /等等
    -- 娃哈哈水（黑马专供）
    -- 娃哈哈水黑马专供
    -- 娃哈哈水'黑马专供'
    :param data:
    :return: str
    """
    return str(data).replace("\'", "").\
        replace("\"", "").\
        replace("$", "").\
        replace("#", "").\
        replace("\\", "").\
        replace("/", "").\
        replace("&", "").\
        replace("^", "").\
        replace(",", "")



def unite_path_slash(path: str) -> str:
    """
    统一将路径的斜杠，规划为单左斜杠
    :param path: 被处理的路径字符串
    :return: 处理好的路径字符串
    """
    return path \
        .replace("\\\\", "/") \
        .replace("\\", "/") \
        .replace("//", "/")
