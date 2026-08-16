
from django.contrib import admin
from django.urls import path,include
from app01.views import index,getfilm
from django.views.static import serve
from django.conf import settings
from .views import welcome,banner,BannerNotice,CollectionView,AreaView,StatisticsView,FaceView,ActivityView,LoginView
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('BannerNotice', BannerNotice, 'BannerNotice')
router.register('Collection', CollectionView, 'Collection')
router.register('AreaView', AreaView, 'AreaView')
router.register('StatisticsView', StatisticsView, 'StatisticsView')
router.register('FaceView', FaceView, 'FaceView')
router.register('ActivityView', ActivityView, 'ActivityView')
router.register('user', LoginView, 'user')


urlpatterns = [
    path('welcome/', welcome),
    path('banner/', banner),

]
urlpatterns+=router.urls