import logging
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils



class approve(unittest.TestCase):
    phone2 = '13033445577'
    pwd = 'test123'
    realname = "张三"
    cardId = "512501197506045175"

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.approve_api = approveAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 认证成功
    def test01_approve_success(self):
        response = self.login_api.login(self.session, '13033445566', 'test123')  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.approve_api.approve(self.session, self.realname, self.cardId)
        logging.info("get approve response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "提交成功!")

    # 姓名为空，认证失败(bug,提示错误)
    def test02_approve_fail_name_is_null(self):
        response = self.login_api.login(self.session, self.phone2, self.pwd)  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.approve_api.approve(self.session, "", self.cardId)
        logging.info("get approve response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "姓名不能为空")

    # 身份证号为空,认证失败(bug,提示错误)
    def test03_approve_fail_cardId_is_null(self):
        response = self.login_api.login(self.session, self.phone2, self.pwd)  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.approve_api.approve(self.session, self.realname, "")
        logging.info("get approve response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "身份证号不能为空")

    # 获取认证信息
    def test04_get_approve(self):
        response = self.login_api.login(self.session, '13033445566', 'test123')  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        response = self.approve_api.get_approve(self.session)
        logging.info("get approve response {}".format(response.json()))
        self.assertEqual(200, response.status_code)
