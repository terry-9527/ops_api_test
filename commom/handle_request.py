# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/22 11:33
@Author  : Terry
@File    : handle_request.py

'''
import json
import requests

from commom.handle_log import mylogger
from commom.handle_mysql import MysqlDb
from commom.read_data import readData


class HandleRequests:

    def send_requests(self, method, url, data=None, token=None, sql=None):
        self.__handle_pre_sql(sql)
        mylogger.info("=======================  发起一次HTTP请求  =======================")
        mylogger.info(f"请求方法为:{method}")
        # 处理请求头
        self.headers = self.__deal_headers(token)
        mylogger.info(f"请求头headers为：{self.headers}")
        # 处理URL请求地址
        self.url = self.__deal_url(url)
        mylogger.info(f"请求的URL为：{self.url}")
        # 处理请求的数据
        self.data = self.__deal_data(data)
        mylogger.info(f"请求数据为：{self.data}")
        if method.upper() == "GET":
            self.response = requests.get(self.url, params=self.data, headers=self.headers)
        elif method.upper() == "POST":
            self.response = requests.post(self.url, json=self.data, headers=self.headers)
        mylogger.info("响应状态码：{}".format(self.response.status_code))
        mylogger.info("响应数据为：{}".format(self.response.json()))
        return self.response

    def __deal_headers(self, token=None):
        self.headers = {"Content-Type": "application/json"}
        if token is not None:
            self.headers['Authorization'] = "Bearer {}".format(token)
        return self.headers


    def __deal_url(self, url):
        """
        读取Excel表格中的URL，拼接上配置文件中的base_url,组合成完成的URL
        :param url: 表格中读取到的URL
        :return: 返回拼接后完整的的URL
        """
        base_url = readData().read_config("api", "base_url")
        url = base_url + url
        return url

    def __deal_data(self, data):
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data
        return self.data

    def __handle_pre_sql(self, sql):
        if sql:
            mylogger.info("执行测试用例pre_sql列的前置条件，执行数据库语句：{}".format(sql))
            db = MysqlDb()
            db.execute(sql)
            db.close_conn()