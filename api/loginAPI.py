import app
import requests


class loginAPI():
    def __init__(self):
        self.imgCode_url = app.BASE_URL + '/common/public/verifycode1/'
        self.message_url = app.BASE_URL + '/member/public/sendSms'
        self.register_url = app.BASE_URL + '/member/public/reg'
        self.login_url = app.BASE_URL + '/member/public/login'

    # 获取图片验证码
    def get_imgCode(self, session, r):
        url = self.imgCode_url + r
        response = session.get(url)
        return response

    # 获取短信验证码
    def get_messageCode(self, session, phone, imgVerifyCode):
        data = {'phone': phone, 'imgVerifyCode': imgVerifyCode, 'type': 'reg'}
        response = session.post(self.message_url, data=data)
        return response

    # 注册
    def register(self, session, phone, pwd, imgVerifyCode='8888', phoneCode='666666', dyServer='on', invite_phone=""):
        data = {"phone": phone,
                "password": pwd,
                "verifycode": imgVerifyCode,
                "phone_code": phoneCode,
                "dy_server": dyServer,
                "invite_phone": invite_phone}
        response = session.post(self.register_url, data=data)
        return response

    # 登录
    def login(self, session, phone, pwd):
        data = {"keywords": phone, "password": pwd}
        response = session.post(self.login_url, data=data)
        return response
