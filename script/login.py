import random
import time
import unittest

import requests
from parameterized import parameterized
from api.loginAPI import loginAPI
from utils import assert_utils, read_imgVerify_data, read_param_data
import logging


class login(unittest.TestCase):
    phone1 = '13033445566'
    phone2 = '13033445577'
    phone3 = '13033445590'
    phone4 = "13033445500"
    imgCode = '8888'
    pwd = 'test123'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()


    # 参数为随机小数时，获取图片验证证码成功
    def test01_get_imgCode_random_float(self):
        r = str(random.random())
        response = self.login_api.get_imgCode(self.session, r)
        logging.info("get imgCode response {}".format(response.text))
        self.assertEqual(200, response.status_code)

    # 参数为随机整数时，获取图片验证码成功
    def test02_get_imgCode_random_int(self):
        r = str(random.randint(0, 9999999))
        response = self.login_api.get_imgCode(self.session, r)
        logging.info("get imgCode response {}".format(response.text))
        self.assertEqual(200, response.status_code)

    # 参数为空时，获取图片验证码失败
    def test03_get_imgCode_null(self):
        response = self.login_api.get_imgCode(self.session, "")
        logging.info("get imgCode response {}".format(response.text))
        self.assertEqual(404, response.status_code)

    # 参数为随机字母时，获取图片验证码失败
    def test04_get_imgCode_random_char(self):
        r = random.sample("abcdefghijklmn", 8)
        rand = ''.join(r)  # 连接字符串，获得随机连到一起的字符串
        response = self.login_api.get_imgCode(self.session, rand)
        logging.info("get imgCode response {}".format(response.text))
        self.assertEqual(400, response.status_code)

    # 参数正确，获取短信验证码成功
    def test05_get_messageCode_success(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        response = self.login_api.get_messageCode(self.session, self.phone1, self.imgCode)
        logging.info("get messageCode response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")

    # 图片验证码错误，获取短信验证码失败
    def test06_get_messageCode_fail_imgCode_error(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        error_code = '1234'
        response = self.login_api.get_messageCode(self.session, self.phone1, error_code)
        logging.info("get messageCode response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 图片验证码为空，获取短信验证码失败
    def test07_get_messageCode_fail_imgCode_isnull(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        response = self.login_api.get_messageCode(self.session, self.phone1, "")
        logging.info("get messageCode response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 手机号为空，获取短信验证码失败
    def test08_get_messageCode_fail_phone_isnull(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        response = self.login_api.get_messageCode(self.session, "", self.imgCode)
        logging.info("get messageCode response {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 不调用获取图片验证码接口，获取短信验证码失败
    def test09_get_messageCode_fail_no_imgCode(self):
        response = self.login_api.get_messageCode(self.session, self.phone1, self.imgCode)
        logging.info("get messageCode response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")


    # 输入必填项，注册成功
    def test10_register_success_param_must(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone1, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 输入所有参数，注册成功
    def test11_register_success_param_all(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone2, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone=self.phone1)
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 图片验证码错误，注册失败
    def test12_register_fail_img_error(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone3, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone3, self.pwd, imgVerifyCode='8889')
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误!")

    # 短信验证码错误，注册失败
    def test13_register_fail_message_error(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone3, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone3, self.pwd, phoneCode='123456')
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误")

    # 手机已存在，注册失败
    def test14_register_fail_phone_is_exist(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone2, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone2, self.pwd, invite_phone=self.phone1)
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 密码为空，注册失败(bug，注册成功)
    def test15_register_fail_pwd_is_null(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone3, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone3, "")
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 未同意条款，注册失败(bug，注册成功)
    def test16_register_fail_no_agree(self):
        self.login_api.get_imgCode(self.session, '5455')  # 获取图片验证码成功
        self.login_api.get_messageCode(self.session, self.phone4, self.imgCode)  # 获取短信验证码成功
        response = self.login_api.register(self.session, self.phone4, self.pwd, dyServer='off')
        logging.info("get register response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "请同意我们的条款")

    # 输入正确手机和密码，登录成功
    def test17_login_success(self):
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")

    # 用户不存在，登录失败
    def test18_login_fail_phone_no(self):
        phone_no = 17378975878
        response = self.login_api.login(self.session, phone_no, self.pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "用户不存在")

    # 密码为空，登录失败
    def test19_login_fail_pwd_is_null(self):
        response = self.login_api.login(self.session, self.phone1, "")
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 登录失败-错误密码
    def test20_login_fail_pwd_error(self):
        # 1.输入错误密码，提示错误一次
        wrong_pwd = 'error'
        response = self.login_api.login(self.session, self.phone1, wrong_pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        # 2.输入错误密码，提示错误两次
        response = self.login_api.login(self.session, self.phone1, wrong_pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        # 3.输入密码密码，提示错误三次锁定
        response = self.login_api.login(self.session, self.phone1, wrong_pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 4.输入正确密码，提示被锁定
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        # 5.等待1分钟，输入正确密码，登录成功
        time.sleep(60)
        response = self.login_api.login(self.session, self.phone1, self.pwd)
        logging.info("get login response {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
