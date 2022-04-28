# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/21 15:29
@Author  : Terry
@File    : test_002_login.py

'''
import json
import re
import pytest

from commom.Data import set_dataclass_arrt_from_resp, Data
from commom.handle_log import mylogger
from commom.handle_request import HandleRequests
from commom.read_data import readData
from commom.handle_sms_code import get_sms_code
from commom.handle_extract import extract_data_from_response


class TestLoginCase:
    cases = readData().read_excel("登陆", "demo.xlsx")
    @pytest.mark.parametrize("args", cases)
    def test_login(self, args):
        mylogger.info("=========== 登陆接口测试  ===============")
        mark_list = re.findall("#sms_code#", args['req_data'])
        if mark_list:
            sms_code = get_sms_code(eval(args['req_data'])['phone'])
            mylogger.info(sms_code)
            args['req_data'] = args['req_data'].replace("#sms_code#", sms_code)
        req = HandleRequests()
        res = req.send_requests(args['method'], args['url'], args['req_data'])
        extract_data_from_response(args['extract'],res.json(),Data())

if __name__ == '__main__':
    pytest.main(["-v", "-s"], "test_002_login.py")