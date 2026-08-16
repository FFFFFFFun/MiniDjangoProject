from aip import AipFace
import base64


class BaiDuFace:
    def __init__(self, APP_ID='123986722', API_KEY='PbryIE5r9zlSkJ50r22TKi7t',
                 SECRET_KEY='HdgsYg8tjfUb1WL7yMdIpkKa1kXNRQnu'):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    def add_user(self):
        image = base64.b64encode(open('./1.png', 'rb').read()).decode('utf-8')
        imageType = "BASE64"
        groupId = "100"
        userId = "user1"
        """ 调用人脸注册 """
        #client.addUser(image, imageType, groupId, userId);
        """ 如果有可选参数 """
        options = {}
        options["user_info"] = "user's info"
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"

        """ 带参数调用人脸注册 """
        res = self.client.addUser(image, imageType, groupId, userId, options)

        return res

    def delete(self):
        userId = "user1"
        groupId = "group1"
        faceToken = "face_token_23123"
        #调用人脸删除
        res = self.client.faceDelete(userId, groupId, faceToken)
        return res

    def search(self):
        data = base64.b64encode(open('./2.png', 'rb').read()).decode('utf-8')
        image = data
        imageType = "BASE64"
        groupIdList = "100"

        self.client.search(image, imageType, groupIdList)
        options = {}
        options["match_threshold"] = 70
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["user_id"] = "233451"
        options["max_user_num"] = 3

        """ 带参数调用人脸搜索 """
        res = client.search(image, imageType, groupIdList, options)
        return res

if __name__ == '__main__':
    ai = BaiDuFace()
    #res =  ai.add_user()
    #print(res)
    #{'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 1840941990, 'timestamp': 1784281281, 'cached': 0, 'result': {'face_token': 'e07d7bc60b4dc126af01f04bdbacea83', 'location': {'left': 108, 'top': 137.56, 'width': 143, 'height': 137, 'rotation': -5}}}
