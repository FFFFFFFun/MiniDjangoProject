
from django.contrib import admin
from django.urls import path,include
from app01.views import index,getfilm,welcome
from django.views.static import serve
from django.conf import settings
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('index/', index),
    path('getfilm/', getfilm),

    path('media/<path:path>', serve,{'document_root':settings.MEDIA_ROOT}),
    #这个作用是吧图片作为url分发出去
    path('app01/', include('app01.urls')),

]
