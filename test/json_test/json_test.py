#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/18/18 4:36 PM
# @Author  : hys
# @Site    : 
# @File    : json_test.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com

import json


class JsonTest:
    """此处用于练习json数据的存储"""
    def __init__(self):
        """初始化本类"""
        print("Json初始化")

    @staticmethod
    def write_date(write_value, file_name="default_file.json"):
        """写数据"""
        with open(file_name, 'w') as f_obj:
            json.dump(write_value, f_obj)

    @staticmethod
    def read_dat(file_name):
        with open(file_name) as f_obj:
            file_value = json.load(f_obj)
        return file_value


if __name__ == "__main__":
    # 声明变量
    json_test = JsonTest()
    # 声明要写入的值
    numbers = [2, 3, 4, 5, 6]
    json_test.write_date(file_name="numbers.json", write_value=numbers)

    rv = json_test.read_dat("numbers.json")
    print(rv)

