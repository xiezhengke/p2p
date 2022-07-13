import app


class approveAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.get_approve_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self, session, realname, cardID):
        data = {"realname": realname, "card_id": cardID}
        response = session.post(self.approve_url, data=data, files={'x': 'y'})  # 构造多消息体
        return response

    def get_approve(self, session):
        response = session.post(self.get_approve_url)
        return response
