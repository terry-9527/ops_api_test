# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/27 14:33
@Author  : Terry
@File    : demo.py

'''
import json
import re
from faker import Faker

import jsonpath



# req_data ={"name":"#random_name#","owned_customer":"#cliet_id#","note":"西游记、水浒装、三国演义、红楼梦"}
# for key,value in req_data.items():
# 	# print(key, value)
# 	# if value.startswith("#") and value.endswith("#"):
# 	if value.__contains__("random_name"):
# 		print(key)
# data = '{"name":"fdfdsf","owned_customer":null,"note":"西游记、水浒装、三国演义、红楼梦"}'
#
# data = json.loads(data)
# print(type(data))
# print(data)
faker = Faker(locale="zh_CN")

# print(faker.pystr()[:5])
# role_name = "role-" + faker.pystr()[:5] + "-" + faker.numerify()
# print(role_name)

from faker import Faker
from faker.providers import BaseProvider

# 创建自定义Provider
class CustomProvider(BaseProvider):
    def customize_type(self):
        return 'test_Faker_customize_type'

    def machineroom_name(self):
        name = "先河系统-" + faker.province() + "-" + faker.numerify() + "机房"
        return name

# 添加Provider
fake = Faker()
fake.add_provider(CustomProvider)
print(fake.customize_type())
print(fake.machineroom_name())