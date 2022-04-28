# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/22 17:21
@Author  : Terry
@File    : handle_replace.py

'''
import json
import re

from commom.Data import Data
from commom.handle_log import mylogger
from commom.handle_sms_code import get_sms_code
from commom.read_data import readData
from commom.my_faker import faker

def replace_case_from_re(case_dict, share_data_obj: Data):
    """
    对用例数据进行处理，根据标记的#xxx#标记符，替换成对应的值
    :param case_dict: 一条测试用例数据，字典类型
    :param common_obj: 用于动态存储数据的公共类Data
    :return: 返回替换之后的用例数据，类型dict
    """
    key_list = []
    # 把字典类型的测试数据，转换成str类型，方便通过re正则进行查找标记符#XXXX#
    case_str = str(case_dict)
    mylogger.info("测试用例数据为：{}".format(case_str))
    # 查看到已#开头#结尾的所有标识符，正则#(\w+)#，表示查找到##中间的标识符，（）正则中的分组，只返回匹配括号里面的内容
    marks_list = re.findall("#(\w+)#", case_str)
    mylogger.info("查找到需要替换的标记符为：{}".format(marks_list))
    # 判断不为空则找到需要替换的标记符，否则表明没有需要替换的标记符
    if marks_list:
        # 如果存在sms_code和phone标识符，表示要生成短信验证码进行替换,获取配置的phone进行替换
        if "phone" and "sms_code" in marks_list:
            phone = readData().read_config("test_account", "phone3")
            mylogger.info("把需要替换的#phone#替换成：{}".format(phone))
            sms_code = get_sms_code(phone)
            mylogger.info("把需要替换的#sms_code#替换成：{}".format(sms_code))
            case_str = case_str.replace("#phone#", phone)
            case_str = case_str.replace("#sms_code#", sms_code)

        if "address" in marks_list:
            address = faker.address()
            case_str = case_str.replace("#address#", address)

        if "email" in marks_list:
            email = faker.free_email()
            case_str = case_str.replace("#email#", email)

        if "domain" in marks_list:
            domain = faker.domain()
            case_str = case_str.replace("#domain#", domain)

        if "comment" in marks_list:
            comment = faker.comment()
            case_str = case_str.replace("#comment#", comment)

        for mark in marks_list:
            # 判断Data类中如果存在mark属性，则用对应的mark属性值替换用例数据中的标识符
            if hasattr(share_data_obj, mark):
                mylogger.info("将标识符为：#{}#，替换为：{}".format(mark, getattr(share_data_obj, mark)))
                case_str = case_str.replace(f"#{mark}#", str(getattr(share_data_obj, mark)))
        new_case_dict = eval(case_str)
        mylogger.info("替换之后的测试用例数据为：{}".format(new_case_dict))
        return new_case_dict
    else:
        mylogger.info("用例中没有需要替换的标识符,无需进行处理。")
        return case_dict



if __name__ == '__main__':
    case = {'case_id': 1, 'title': '新建机房', 'method': 'post', 'url': '/machine/create/one', 'req_data': '{"machine_name":"aaaa","machine_site":"aaaaa","domain":"aaaa","note":"aaaa","scheduling":true}', 'assert_list': '[{"expr":"$.code","expected":0,"type":"eq"},\n{"expr":"$.msg","expected":"操作成功","type":"eq"}]', 'assert_db': None, 'extract': None, 'execute': 'True'}
    # req_data ={'case_dict': '{"machine_name":"aaaa","machine_site":"aaaaa","domain":"aaaa","note":"aaaa","scheduling":true}'}
    req_data = case['req_data']
    print(type(req_data))
    print(req_data)
    new_req_data = json.loads(req_data)
    print(type(new_req_data))
    print(new_req_data)
    # new_case_dict = replace_case_from_re(case_dict, Data())
