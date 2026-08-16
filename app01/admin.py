from django.contrib import admin

# Register your models here.

from .models import Welcome,Banner,Notice,UserInfo,Area,Collection,Activity

admin.site.register(Welcome)
admin.site.register(Banner)
admin.site.register(Notice)
admin.site.register(UserInfo)
admin.site.register(Area)
admin.site.register(Collection)
admin.site.register(Activity)

