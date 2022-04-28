# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/27 15:00
@Author  : Terry
@File    : test_role.py

'''
import json
import pytest

from commom.handle_extract import extract_data_from_response
from commom.handle_log import mylogger
from commom.handle_request import HandleRequests
from commom.read_data import readData
from commom.handle_replace import replace_case_from_re
from commom.my_assert import MyAssert

# 读取测试用例数据
cases = readData().read_excel("新建角色", "demo.xlsx")
req = HandleRequests()
myassert = MyAssert()

@pytest.mark.usefixtures("user_login")
class TestRole:

    @pytest.mark.parametrize("case", cases)
    def test_new_role(self, case, user_login):
        mylogger.info("===========  新建角色接口测试  ===============")
        share_data = user_login
        # 1.用例数据处理，用上一接口的提取到的数据，替换下一接口的请求数据
        case = replace_case_from_re(case, share_data)
        # 2.替换之后的请求数据，用json.loads()方法把json格式的字符串转换成python的dict字典
        if case['req_data']:
            req_dict = json.loads(case['req_data'])
            mylogger.info("处理之后的请求数据为：{}".format(req_dict))
        else:
            req_dict = None
        # 3.用处理后的数据发起请求
        # if hasattr(share_data, "token"):
        res = req.send_requests(case['method'], case['url'], req_dict, token=getattr(share_data, "token"), sql=case['pre_sql'])
        # else:
        #     res = req.send_requests(case['method'], case['url'], req_dict)
        if case['extract']:
            extract_data_from_response(case['extract'], res.json(), share_data)

        assert_res = []

        # 4.对响应结果进行断言
        if case['assert_response']:
            check_res = myassert.assert_response_value(res.json(), case['assert_response'])
            assert_res.append(check_res)

        # 5.对数据库进行断言
        if case['assert_db']:
            check_db_res = myassert.assert_db(case['assert_db'])
            assert_res.append(check_db_res)

        # 6.对上述结果总的结果进行判断
        if False in assert_res:
            mylogger.error("用例执行失败")
            raise AssertionError
if __name__ == '__main__':
    pytest.main(["-v", "-s"], "test_role.py")