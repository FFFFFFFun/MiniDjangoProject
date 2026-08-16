import os
from django.conf import settings

# 腾讯云短信基础配置
TENCENT_SMS = {
    # 腾讯云SecretId
    "secret_id": getattr(settings, "TX_SMS_SECRET_ID", os.getenv("TX_SMS_SECRET_ID", "")),
    # 腾讯云SecretKey
    "secret_key": getattr(settings, "TX_SMS_SECRET_KEY", os.getenv("TX_SMS_SECRET_KEY", "")),
    # 短信SdkAppId 腾讯云短信应用ID
    "sdk_app_id": getattr(settings, "TX_SMS_SDK_APP_ID", os.getenv("TX_SMS_SDK_APP_ID", "")),
    # 短信模板ID
    "template_id": getattr(settings, "TX_SMS_TEMPLATE_ID", os.getenv("TX_SMS_TEMPLATE_ID", "")),
    # 短信签名名称
    "sign_name": getattr(settings, "TX_SMS_SIGN_NAME", os.getenv("TX_SMS_SIGN_NAME", "")),
    # 地域
    "region": getattr(settings, "TX_SMS_REGION", "ap-beijing")
}