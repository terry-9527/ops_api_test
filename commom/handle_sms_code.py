# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/24 14:22
@Author  : Terry
@File    : handle_sms_code.py

'''
import jsonpath

from commom.handle_log import mylogger
from commom.handle_request import HandleRequests


def get_sms_code(phone, sms_type="login"):
    """
    :param phone: 手机号码
    :param sms_type: login,modify
    :return: 返回短信验证码
    """
    data = {
        "sms_type": sms_type,
        "phone": phone
    }
    req = HandleRequests()
    res = req.send_requests("post", url="/sms/get", data=data)
    sms_code = jsonpath.jsonpath(res.json(), "$..sms_code")
    mylogger.info("生成的验证码为：{}".format(sms_code[0]))
    return sms_code[0]


if __name__ == '__main__':
    code = get_sms_code("18277777777")
    print(code)
