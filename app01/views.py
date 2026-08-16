from django.db.models.expressions import result
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import json

from sympy import true

from libs.baidu_fr import BaiDuFace
from django.template.defaulttags import querystring
from .models import Welcome, Banner


def index(request):
    return JsonResponse({'name': 'ff'})


def getfilm(request):
    with open('./film.json', 'r', encoding='utf-8') as f:
        dis = json.load(f)
    return JsonResponse(dis)


def welcome(request):
    res = Welcome.objects.all().order_by('-order').first()
    img = 'http://192.168.0.108:8000/media/' + str(res.img)

    return JsonResponse({'code': 100, 'msg': '成功', 'result': img})


def banner(request):
    # order 从大到小排序，取前 5 条，同时过滤已软删除数据
    banner_list = Banner.objects.filter(is_delete=False).order_by("-order")[:5]
    data = serializers.serialize("json", banner_list)
    result = []
    for item in banner_list:
        result.append({
            "id": item.id,
            "img": 'http://192.168.0.108:8000' + str(item.img.url),
            "link_url": item.link_url,
            "order": item.order,
        })

    return JsonResponse({
        'code': 100,
        'msg': '成功',
        'result': result
    })


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from .models import Banner, Notice, Collection
from .serializer import BannerSerializer, NoticeSerializer, CollectionSerializer, AreaViewSerializer, \
    CollectionSaveSerializer
from datetime import datetime
from django.utils import timezone


class BannerNotice(GenericViewSet, ListModelMixin):
    queryset = Banner.objects.filter(is_delete=False).order_by("-order")[:5]
    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        notice = Notice.objects.filter(is_delete=False).order_by("create_time").first()
        serializer = NoticeSerializer(instance=notice)

        return Response({'code': 100, 'msg': '成功', 'banner': res.data, 'notice': serializer.data})


class CollectionView(GenericViewSet, ListModelMixin, DestroyModelMixin, CreateModelMixin):
    # serializer_class = CollectionSerializer

    def get_queryset(self):
        today = timezone.now().date()
        # print(Collection.objects.filter())
        return Collection.objects.filter()  # create_time__gte=today

    def get_serializer_class(self):
        # print(self.action)
        if self.action == 'create':
            return CollectionSaveSerializer
        else:
            return CollectionSerializer

    def list(self, request, *args, **kwargs):
        # print(request.method)
        res = super().list(request, *args, **kwargs)
        # print(res.data)
        today_count = self.get_queryset().count()

        return Response({'code': 100, 'msg': '成功', 'result': res.data, 'today_count': today_count})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(instance)
        # 百度ai中删除
        baidu = BaiDuFace()
        res = baidu.delete(instance.name_pinyin, instance.face_token)
        # print(res)
        self.perform_destroy(instance)
        return Response()


from .models import Area


class AreaView(GenericViewSet, ListModelMixin):
    queryset = Area.objects.all()
    serializer_class = AreaViewSerializer


from django.db.models.functions import Trunc
from django.db.models import Count
from .models import Collection
from .serializer import StatisticsListSerializer


class StatisticsView(GenericViewSet, ListModelMixin):
    queryset = Collection.objects.annotate(date=Trunc('create_time', 'day')).values('date').annotate(
        count=Count('id')).values('date', 'count')
    serializer_class = StatisticsListSerializer


from libs.baidu_fr import BaiDuFace


class FaceView(GenericViewSet):
    def create(self, request, *args, **kwargs):
        # 1 取出前端传入的人
        # print(request.data)
        avatar_object = request.data.get('avatar')
        print(avatar_object)
        if not avatar_object:
            return Response({'code': 103, 'msg': '请正常拍照'})
        # 2 使用百度人脸库--》搜索
        ai = BaiDuFace()
        res = ai.search(avatar_object)
        print(res)
        if res.get('error_code') == 0:
            # 3查到了，取出userid--》能匹配成功多个，只取第一条
            user_id = res.get('result').get('user_list')[0].get('user_id')
            score = int(res.get('result').get('user_list')[0].get('score'))
            # 4去咱们采集库，查出用户详情
            user = Collection.objects.filter(name_pinyin=user_id).first()
            area_name = user.area.name if user.area else None
            return Response({'code': 100, 'msg': '匹配成功', 'name': user.name, 'score': score, 'area': area_name})
        else:
            return Response({'code': 102, 'msg': '查无此人'})


from .models import Activity
from .serializer import ActivitySerializer


class ActivityView(GenericViewSet, ListModelMixin):
    queryset = Activity.objects.all().order_by('date')
    serializer_class = ActivitySerializer


# 验证码发送
from django.core.cache import cache
from rest_framework.decorators import action
from libs.send_tx_sms import get_code, send_sms_by_phone
from .models import UserInfo
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(GenericViewSet):
    @action(methods=['GET'], detail=False)
    def send_sms(self, request, *args, **kwargs):
        print(request)
        mobile = request.query_params.get('mobile')
        code = get_code()
        # 验证码缓存 临时存取 后期跟根据key取出来
        cache.set(f'sms_{mobile}', code)
        res = true  # send_sms_by_phone(mobile, code)
        print(code)
        if res:
            return Response({'code': 100, 'msg': '短信发送成功'})
        else:
            return Response({'code': 101, 'msg': '短信发送失败，请稍后再试'})

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        code = request.data.get('code')

        old_code = cache.get(f'sms_{mobile}', code)

        if old_code == code:
            user = UserInfo.objects.filter(mobile=mobile).first()
            if not user:
                #fake = Faker('zh_CN')
                username = '新用户'
                user = UserInfo.objects.create(mobile=mobile,name=username)
            refresh = RefreshToken.for_user(user)
            #print(refresh)
            #print(user)
            return Response(
                {'code': 100,'msg':'登录成功','token':str(refresh.access_token),'name':user.name,
                'score':user.score, 'avatar':'http://127.0.0.1:8000/media/' +str(user.avatar)})
        else:
            return Response({'code': 102,'msg':'验证码错误'})

    @action(methods=['post'], detail=False)
    def quick_login(self, request, *args, **kwargs):
        code = request.data.get('code')
        # 2 通过code，调用微信开发平台接口，换取手机号
        # 3 拿到手机号再自己库中查，能查到，签发token
        # 4 查不到注册再签发token
        user = UserInfo.objects.filter(pk=1).first()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'code': 100, 'msg': '登录成功', 'token': str(refresh.access_token), 'name': user.name,
             'score': user.score,'avatar': 'http://127.0.0.1:8000/media/' + str(user.avatar)})