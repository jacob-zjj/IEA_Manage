from __future__ import unicode_literals
from django.db import models

# Create your models here.
"""
具体思路是：有18个设备对应了不同的id  0-17
            这18个设备对应了5个不同的协议类型
"""
# 协议一 ModbusRtu协议设备
class ModbusRtu(models.Model):
    name = models.CharField(max_length=30)
    deviceStatus = models.BooleanField()
    #用来识别设备是 多少编号
    deviceId = models.IntegerField()
    realtimeData = models.DecimalField(decimal_places=2,max_digits=6)
    class Meta:
        verbose_name_plural = u'MoudbusRtu设备(0-9)'
    def __str__(self):
        return u'MoudbusRtu设备: %s' % (self.name)

# 协议二 Can总线
class Can(models.Model):
    name = models.CharField(max_length=30)
    deviceStatus = models.BooleanField()
    # 用来识别设备是 多少编号
    deviceId = models.IntegerField()
    realtimeData = models.DecimalField(decimal_places=2,max_digits=6)
    class Meta:
        verbose_name_plural = u'Can总线设备(10-13)'
    def __str__(self):
        return u'Can总线设备: %s' % (self.name)

# 协议三 ModbusTcp设备
class ModbusTcp(models.Model):
    name = models.CharField(max_length=30)
    deviceStatus = models.BooleanField()
    # 用来识别设备是 多少编号
    deviceId = models.IntegerField()
    realtimeData = models.DecimalField(decimal_places=2,max_digits=6)
    class Meta:
        verbose_name_plural = u'ModbusTcp设备(14-15)'
    def __str__(self):
        return u'ModbusTcp设备: %s' % (self.name)

# 协议四树莓派设备传感器
class RaspberryPi(models.Model):
    name = models.CharField(max_length=30)
    deviceStatus = models.BooleanField()
    # 用来识别设备是 多少编号
    deviceId = models.IntegerField()
    realtimeData = models.DecimalField(decimal_places=2,max_digits=6)
    class Meta:
        verbose_name_plural = u'RaspberryPi设备(16-17)'
    def __str__(self):
        return u'树莓派设备: %s' % (self.name)