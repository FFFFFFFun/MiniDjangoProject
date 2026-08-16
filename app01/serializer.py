from rest_framework import serializers
from .models import Banner, Notice, Collection, Area,Activity
from  libs.baidu_fr import BaiDuFace
from  rest_framework.exceptions import APIException

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'avatar', 'area']
        depth = 1



class CollectionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name', 'avatar', 'area']
    def create(self, validated_data):
        ai = BaiDuFace()
        file_obj = validated_data.get('avatar') #获得图片
        name = validated_data.get('name') #获得人名
        name_pinyin = ai.name_to_pingyin(name)
        res = ai.add_user(file_obj,name_pinyin)
        #print(validated_data)
        #print(res)
        if res.get('error_code') == 0:
            validated_data['face_token']=res.get('result').get('face_token')
            validated_data['name_pinyin'] = name_pinyin
            instance=super().create(validated_data)
            return instance
        else:
            raise APIException('采集信息失败')


class AreaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'desc', 'user']
        depth = 1

class StatisticsListSerializer(serializers.Serializer):
    date = serializers.DateTimeField(format='%Y年%m月%d日')
    count = serializers.IntegerField()

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'text', 'date','count','score','total_count']
        extra_kwargs = {
            'date': {'format': "%Y-%m-%d"}
        }


