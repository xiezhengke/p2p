import json
import logging

import requests
from bs4 import BeautifulSoup

import app


def assert_utils(self, response, status_code, status, desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))


def request_third_api(form_data):
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info('third request url={}'.format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])  # 在字典中添加key-value
    logging.info('third request data={}'.format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    logging.info("third response {}".format(response.text))
    return response


# 读取图片验证码参数
def read_imgVerify_data(file_name):
    file = app.BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(file, encoding='utf-8') as f:
        verify_data = json.load(f)
        test_data_list = verify_data.get("test_get_img_verify_code")
        for test_data in test_data_list:
            test_case_data.append((test_data.get("type"), test_data.get("status_code")))
    print("json_data={}".format(test_case_data))
    return test_case_data


# 定义统一的读取所有参数数据文件的方法
def read_param_data(filename, method_name, param_names):
    # filename： 参数数据文件的文件名
    # method_name: 参数数据文件中定义的测试数据列表的名称，如：test_get_img_verify_code
    # param_names: 参数数据文件一组测试数据中所有的参数组成的字符串，如："type,status_code"

    # 获取测试数据文件的文件路径
    file = app.BASE_DIR + "/data/" + filename
    test_case_data = []
    with open(file, encoding="utf-8") as f:
        # 将json字符串转换为字典格式
        file_data = json.load(f)
        # 获取所有的测试数据的列表
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            # 先将test_data对应的一组测试数据，全部读取出来，并生成一个列表
            test_params = []
            for param in param_names.split(","):
                # 依次获取同一组测试数中每个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            # 每完成一组测试数据的读取，就添加到test_case_data后，直到所有的测试数据读取完毕
            test_case_data.append(test_params)
    print("test_case_data = {}".format(test_case_data))
    return test_case_data
