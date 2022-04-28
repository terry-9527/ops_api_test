# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/24 15:42
@Author  : Terry
@File    : handle_extract.py

'''
import jsonpath

from commom.Data import Data
from commom.handle_log import mylogger


def extract_data_from_response(extract_expr, response_dict, share_data_obj: Data):
    """
    :param extract_expr: excel当中extract列中的提取表达式。是一个字典形式的字符串。
                        key为全局变量名。value为jsonpath提取表达式。形如：'{"token":"$..token"}'
    :param response_dict: http请求之后的响应结果，字典类型
    :param data_ojb:
    :return:
    """
    # 1.将从Excel中读取出来的extract的表达式，读取出来的是字符串，转换成字典
    extract_dict = eval(extract_expr)
    # 2.读取表达式的key,value，value即是jsonpath表达式
    for key, value in extract_dict.items():
        mylogger.info("提取的变量名是：{}，提取的jsonpath表达式是：{}".format(key, value))
        result = jsonpath.jsonpath(response_dict, value)
        mylogger.info("jsonpath提取之后的值为：{}".format(result))
        # jsonpath找了就是列表，找不到返回False
        # 如果提取到了真正的值，那么将它设置为Data类的属性。key是全局变量名，result[0]就是提取后的值
        if result:
            setattr(share_data_obj, key, result[0])
            mylogger.info("提取的变量名是：{}，提取到的值是：{},并设置为Data类实例化对象的属性和值。".format(key, result[0]))