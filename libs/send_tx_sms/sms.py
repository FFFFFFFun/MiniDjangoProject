import random
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models
from .setting import TENCENT_SMS
import os

def get_code() -> str:
    """
    获取4位纯数字验证码
    :return: 4位字符串数字 如 "1234"
    """
    # 生成 0000 ~ 9999 四位数字，补零
    code = random.randint(0, 9999)
    return f"{code:04d}"


def send_sms_by_phone(mobile: str, code: str):
    """
    腾讯云发送短信验证码
    :param mobile: 手机号 11位字符串
    :param code: 4位验证码字符串
    :return: dict 统一返回结果
    """
    # 读取配置
    secret_id = os.getenv("TENCENT_SECRET_ID")
    secret_key = os.getenv("TENCENT_SECRET_KEY")
    sdk_app_id = "1465378339"
    template_id = TENCENT_SMS["template_id"]
    sign_name = TENCENT_SMS["sign_name"]
    region = TENCENT_SMS["region"]


    # 校验配置
    if not all([secret_id, secret_key, sdk_app_id, template_id, sign_name]):
        return {
            "success": False,
            "msg": "腾讯云短信配置缺失，请检查settings",
            "data": None
        }

    # 手机号简单校验
    if not mobile or len(mobile) != 11 or not mobile.isdigit():
        return {
            "success": False,
            "msg": "手机号格式错误",
            "data": None
        }

    # 验证码校验
    if len(code) != 4 or not code.isdigit():
        return {
            "success": False,
            "msg": "验证码必须为4位数字",
            "data": None
        }

    try:
        # 实例化认证对象
        cred = credential.Credential(secret_id, secret_key)
        http_profile = HttpProfile()
        http_profile.reqTimeout = 10
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        # 初始化短信客户端
        client = sms_client.SmsClient(cred, region, client_profile)

        # 组装请求参数
        req = models.SendSmsRequest()
        req.SmsSdkAppId = sdk_app_id
        req.SignName = sign_name
        req.TemplateId = template_id
        # 手机号必须带+86
        req.PhoneNumberSet = [f"+86{mobile}"]
        # 模板参数，按腾讯云模板顺序，验证码放在第一位
        req.TemplateParamSet = [code]

        # 发送请求
        resp = client.SendSms(req)
        response_data = resp.to_json_string()

        # 解析返回结果
        send_status = resp.SendStatusSet[0]
        if send_status.Code == "Ok":
            return {
                "success": True,
                "msg": "短信发送成功",
                "data": {
                    "serial_no": send_status.SerialNo,
                    "phone": mobile
                }
            }
        else:
            return {
                "success": False,
                "msg": f"发送失败：{send_status.Message}",
                "data": response_data
            }

    except Exception as e:
        return {
            "success": False,
            "msg": f"短信服务异常：{str(e)}",
            "data": None
        }