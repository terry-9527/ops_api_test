# -*- coding: utf-8 -*-
'''
@Time    : 2022/4/28 15:50
@Author  : Terry
@File    : my_faker.py

'''
from faker import Faker
from faker.providers import BaseProvider


class MyProvider(BaseProvider):

    def domain(self):
        name = "https://f0{}.arsyun.com:32100".format(faker.numerify())
        return name
    def role_name(self):
        role_name = "role-" + faker.pystr()[:5] + "-" + faker.numerify()
        return role_name
    def comment(self):
        comment = faker.paragraph()
        return comment


faker = Faker(locale="zh_CN")
faker.add_provider(MyProvider)
print(faker.domain())