from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = '基于边缘计算的IPv6工业互联网设备接入后台管理系统'
admin.site.site_title = '数据管理平台'
class PostModeAdmin(admin.ModelAdmin):
    # 修改django admin中的显示格式
    list_display = ('title', 'created')
admin.site.register(TemperatureSensor)
admin.site.register(FloodlightSensor)
admin.site.register(HumiditySensor)
admin.site.register(AtomPressSensor)