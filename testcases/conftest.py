# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/27 11:45
@Author  : Terry
@File    : conftest.py

'''
import pytest

from commom.Data import Data
from commom.handle_extract import extract_data_from_response
from commom.handle_request import HandleRequests
from commom.handle_sms_code import get_sms_code
from commom.read_data import readData
from commom.rsa_encrypt import rsaEncrypt


@pytest.fixture(scope="class")
def class_init():
    class_share_data = Data()
    yield class_share_data
@pytest.fixture(scope="class")
def user_login():
    share_data = Data()
    req = HandleRequests()
    phone = readData().read_config("test_account", "phone1")
    passwd = readData().read_config("test_account", "password1")
    encry_passwd = rsaEncrypt(passwd)
    sms_code = get_sms_code(phone)
    login_url = "/base/login"
    data = {
        "sms_code":sms_code,
        "phone":phone,
        "password":encry_passwd
    }
    res = req.send_requests("post", login_url, data)
    extract_data_from_response('{"token":"$..token"}', res.json(), share_data)
    yield share_data