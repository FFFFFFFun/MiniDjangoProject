from django.db import models
from sympy import true


# Create your models here.

# 开启APP广告页模型#
class Welcome(models.Model):
    # upload_to 图片上传后放到media文件夹下的welcome文件夹下
    # 必须安装 pillow
    img = models.ImageField(upload_to='welcome', default='/welcome/default.png')
    order = models.IntegerField(default=0, verbose_name="排序权重")
    link_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="跳转链接")

    # 这个字段不用传 会自动把上传的图片的时间存到数据库
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        verbose_name = '欢迎页面'
        verbose_name_plural = "欢迎页面"


class Banner(models.Model):
    img = models.ImageField(upload_to='banner', default='/banner/default.png')
    order = models.IntegerField(default=0, verbose_name="排序权重")
    link_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="跳转链接")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        verbose_name = "横幅轮播"
        verbose_name_plural = "横幅轮播"
        ordering = ["order"]

    def __str__(self):
        return f"横幅-{self.id}"


class Notice(models.Model):
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    img = models.ImageField(upload_to='notice', default='/notice/default.png')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        verbose_name = "公共表"
        verbose_name_plural = "公共表"
        ordering = ["create_time"]

    def __str__(self):
        return self.title


class Collection(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="居民姓名")
    name_pinyin = models.CharField(max_length=32, blank=True, null=True, verbose_name="姓名拼音")
    avatar = models.ImageField(upload_to='collection/%Y/%m/%d/', default='collection/default.png', verbose_name="头像")
    create_time = models.DateTimeField(auto_now=True, verbose_name="采集时间")
    face_token = models.CharField(max_length=64, verbose_name='百度Token', null=True)
    area = models.ForeignKey(to='Area', null=True, verbose_name='网格区域', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "采集表"
        ordering = ["create_time"]

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="网格区域名")
    desc = models.CharField(max_length=32, blank=True, null=True, verbose_name="网格简称")
    user = models.ForeignKey(to='UserInfo', null=True, verbose_name='网格负责人', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "网格表"

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="居民姓名")
    avatar = models.ImageField(upload_to='userinfo/%Y/%m/%d/', default='userinfo/default.png', verbose_name="头像")
    create_time = models.DateTimeField(auto_now=True, verbose_name="采集时间")
    score = models.IntegerField(verbose_name='积分', default=0)
    mobile = models.CharField(verbose_name='手机号', max_length=11, null=True)

    class Meta:
        verbose_name_plural = "网格员表"

    def __str__(self):
        return self.name


class Activity(models.Model):
    title = models.CharField(verbose_name="活动标题", max_length=128)
    text = models.TextField(verbose_name="活动描述", null=True, blank=True)
    date = models.DateField(verbose_name="举办活动日期")
    count = models.IntegerField(verbose_name='报名人数', default=0)
    score = models.IntegerField(verbose_name="积分", default=0)
    total_count = models.IntegerField(verbose_name='总人数', default=0)
    join_record = models.ManyToManyField(verbose_name="参与者",
                                         through="JoinRecord",
                                         through_fields=("activity", "user"),
                                         to="UserInfo")

    class Meta:
        verbose_name_plural = "活动表"

    def __str__(self):
        return self.title


class JoinRecord(models.Model):
    user = models.ForeignKey(verbose_name='用户', to="UserInfo", on_delete=models.CASCADE)
    activity = models.ForeignKey(verbose_name="活动", to="Activity", on_delete=models.CASCADE, related_name='ac')
    exchange = models.BooleanField(verbose_name="是否已兑换", default=False)

    class Meta:
        verbose_name_plural = '活动报名记录'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "activity"],
                name="unique_user_activity",
            )
        ]
