import random
import unittest, logging, requests

from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from utils import assert_utils, request_third_api


class Trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户
    def test01_trust_request(self):
        # 认证通过的账号登录
        response = self.login_api.login(self.session, '13033445566', 'test123')  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("trust register response {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))
        # 调用第三方请求方法
        response = request_third_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    # 充值成功
    def test02_recharge(self):
        # 认证通过的账号登录
        response = self.login_api.login(self.session, '13033445566', 'test123')  # 登录成功
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 获取充值验证码
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        logging.info("get recharge verify code response ={}".format(response.text))
        self.assertEqual(200, response.status_code)
        # 发送充值请求
        response = self.trust_api.recharge(self.session, '10000')
        logging.info(" recharge  response ={}".format(response.json()))
        self.assertEqual(200, response.json().get("status"))
        #发送第三方请求
        form_data = response.json().get("description").get("form")
        logging.info('form response={}'.format(form_data))
        # 调用第三方请求方法
        response = request_third_api(form_data)
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)
