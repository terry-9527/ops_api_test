# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/24 10:29
@Author  : Terry
@File    : test_001_sms_code.py

'''
import pytest

from commom.Data import Data
from commom.handle_request import HandleRequests
from commom.read_data import readData
from commom.handle_extract import extract_data_from_response


class TestGetSMSCode:

    cases = readData().read_excel("短信验证码", "demo.xlsx")
    @pytest.mark.parametrize("args", cases)
    def test_login_sms_code(self, args):
        req = HandleRequests()
        res = req.send_requests(args['method'], args['url'], args['req_data'])
        extract_data_from_response(args['extract'], res.json(), Data)
        if hasattr(Data, "sms_code"):
            print(Data.sms_code)