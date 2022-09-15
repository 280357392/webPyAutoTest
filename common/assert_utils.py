"""
common.assert_utils
~~~~~~~~~~~~~~~~~~~

编写断言的地方
"""
import re


def find_text(pattern_text, pattern, string):
    """
    精确匹配，在原始文本中匹配指定文本。\n
    例如：\n
    匹配<html><h1>和</h1></html>之间的内容。\n
    '<html><h1>登录成功</h1></html>'\n
    '<html><h1>(.*)</h1></html>'\n
    :param pattern_text: 指定文本。
    :param pattern: 正则表达式。
    :param string: 原始文本。
    :return: 匹配成功时返回True，匹配失败时返回False。
    """
    result = re.findall(pattern, string, re.M)
    return pattern_text in result


def search_text(pattern_text, string):
    """
    模糊匹配，在原始文本中匹配指定文本。 \n
    :param pattern_text: 指定文本。
    :param string: 原始文本。
    :return: 匹配成功时返回True，匹配失败时返回False。
    """
    result = re.search(pattern_text, string, re.M)
    return bool(result)
