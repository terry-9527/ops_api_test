# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/26 10:28
@Author  : Terry
@File    : my_assert.py

'''
import ast

import jsonpath

from commom.handle_log import mylogger
from commom.handle_mysql import MysqlDb


class MyAssert:

    def assert_response_value(self, response_dict, check_str):
        check_result_list = []
        # 1.把Excel表中，assert_list列读取到的内容转化成列表进行处理
        check_list = ast.literal_eval(check_str)
        # 2.遍历列表中的检查语句,把jsonpath表达式替换成从响应结果中提取到的值
        if check_list:
            for check in check_list:
                extract_list = jsonpath.jsonpath(response_dict, check['expr'])
                if extract_list:
                    actual = extract_list[0]
                    mylogger.info("通过jsonpath表达式：{}，提取到的实际结果为：{}".format(check['expr'], actual))
                    mylogger.info("预期结果为：{}".format(check['expected']))
                    # 将从响应中用jsonpath提取到的实际结果与预期结果进行比较
                    if check['type'] == "eq":
                        mylogger.info("断言方式：{}，断言的结果为：{}".format(check['type'], actual == check['expected']))
                        check_result_list.append(actual == check['expected'])
                    elif check['type'] == "gt":
                        pass
                    else:
                        mylogger.error("暂不支持{}断言方式".format(check['type']))
                        check_result_list.append(False)
        # 3.检查False是否存在结果列表中，有False存在即说明有断言失败
        if False in check_result_list:
            mylogger.error("部分响应结果断言失败，请检查结果是False的断言")
            return False
        else:
            mylogger.info("全部响应结果断言通过")
            return True

    def assert_db(self, check_db_str):
        check_db_res_list = []
        # 1.把Excel表中，assert_db列读取到的内容转化成列表进行处理
        check_db_list = ast.literal_eval(check_db_str)
        # 2.连接数据库
        db = MysqlDb()
        # 3.遍历列表中的检查语句,如果为空则无需进行数据库断言
        if check_db_list:
            for check_db_dict in check_db_list:
                mylogger.info("要对比的sql语句为：{}".format(check_db_dict['sql']))
                if check_db_dict['db_type'] == "count":
                    # 根据db_type的值来判断，count表示对查询结果的条数进行比对
                    mylogger.info("数据库查询方式：{}，将进行数据库查询结果条数进行比对".format(check_db_dict['db_type']))
                    res = db.get_count(check_db_dict['sql'])
                elif check_db_dict['db_type'] == "check_value":
                    # 根据db_type的值来判断，eq表示对查询出来的字典数据结果进行比对
                    mylogger.info("数据库查询方式{}，将进行数据库查询结果字典内容进行比对".format(check_db_dict['db_type']))
                    res = db.query(check_db_dict['sql'], state="one")
                    mylogger.info("查询的数据结果为：{}".format(res))
                else:
                    mylogger.error(f"数据库断言比对类型{check_db_dict['db_type']}错误！！！")
                    raise Exception
                # sql查出的数据进行对比
                mylogger.info("数据库查询的实际结果actual：{}".format(res))
                mylogger.info("要对比的预期结果expected：{}".format(check_db_dict['expected']))
                check_db_res_list.append(res == check_db_dict['expected'])
                mylogger.info("数据库比对结果为：===========>>>{}".format(res == check_db_dict['expected']))
        # 关闭数据库连接
        db.close_conn()
        mylogger.info("关闭数据库连接")
        # 4.检查False是否存在结果列表中，有False存在即说明有断言失败
        if False in check_db_res_list:
            mylogger.error("部分数据库断言失败，请检查结果是False的断言")
            return False
        else:
            mylogger.info("全部数据库断言通过")
            return True




if __name__ == '__main__':
    # response_dict = {'code': -1, 'msg': '机房已存在', 'data': {}, 'time': '2.482203ms'}
    # check_str = '[{"expr":"$.code","expected":-1,"type":"eq"},{"expr":"$.msg","expected":"机房已存在","type":"eq"}]'
    # myassert = MyAssert()
    # res = myassert.assert_response_value(response_dict, check_str)
    # print(res)  {"sql":"SELECT * FROM t_machine_room WHERE NAME='aaaa'","expected":1,"db_type":"count"}
    myassert = MyAssert()
    assert_db_str = """[{"sql":"SELECT * FROM t_machine_room WHERE NAME='aaaa'","expected":0,"db_type":"count"},{"sql":"SELECT name FROM t_machine_room WHERE NAME='aaaa'","expected":{"name":"aaaa"},"db_type":"check_value"}]"""
    myassert.assert_db(assert_db_str)