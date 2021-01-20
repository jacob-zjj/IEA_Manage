# from __future__ import unicode_literals
# from django.db import models
#
# # Create your models here.
#
# class TemperatureSensor(models.Model):
#     name = models.CharField(max_length=30)
#     deviceStatus = models.BooleanField()
#     #用来识别设备是 多少编号
#     deviceId = models.IntegerField()
#     temperature = models.DecimalField(decimal_places=2,max_digits=6)
#     class Meta:
#         verbose_name_plural = u'温度传感器(TemperatureSensor)'
#     def __str__(self):
#         return u'温度传感器: %s' % (self.name)
#
#
# class FloodlightSensor(models.Model):
#     name = models.CharField(max_length=30)
#     deviceStatus = models.BooleanField()
#     # 用来识别设备是 多少编号
#     deviceId = models.IntegerField()
#     luminance = models.DecimalField(decimal_places=2,max_digits=6)
#     class Meta:
#         verbose_name_plural = u'光照传感器(FloodlightSensor)'
#     def __str__(self):
#         return u'光照传感器: %s' % (self.name)
#
# class HumiditySensor(models.Model):
#     name = models.CharField(max_length=30)
#     deviceStatus = models.BooleanField()
#     # 用来识别设备是 多少编号
#     deviceId = models.IntegerField()
#     humidity = models.DecimalField(decimal_places=2,max_digits=6)
#     class Meta:
#         verbose_name_plural = u'湿度传感器(HumiditySensor)'
#     def __str__(self):
#         return u'湿度传感器: %s' % (self.name)
#
# class AtomPressSensor(models.Model):
#     name = models.CharField(max_length=30)
#     deviceStatus = models.BooleanField()
#     # 用来识别设备是 多少编号
#     deviceId = models.IntegerField()
#     atomPress = models.DecimalField(decimal_places=2,max_digits=6)
#     class Meta:
#         verbose_name_plural = u'大气压力传感器(HumiditySensor)'
#     def __str__(self):
#         return u'大气压力传感器: %s' % (self.name)