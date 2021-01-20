#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
# 导入数据库模型 也就是导入数据类
from IOTEWMPApp.models import *
# from IOTEWMPApp.原来的数据库models1 import *
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from . import ClientToServer
ClientToServer = ClientToServer.ClientToServer()
# 先对其进行注释在 连接底层的情况下再进行连接
ClientToServer.connect()
import logging

# Create your views here.
@login_required()
def managePage(request):
    # username = getpass.getuser()
    # 请求这个网页时 直接转发为登录界面不管有没有进行登录
    # return HttpResponseRedirect("/login/")
    # return render(request, 'ManagementPlatform.html', {'username':username})
    if request.user.is_authenticated:
        username = request.user.get_username()
        return render(request, 'ManagementPlatform.html', {'username':username})
    else:
        return render(request, 'login.html')

def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                #重定向到成功页面
            else:
                #提示错误信息
                warning1 = "登陆失败！"
                return render(request, 'login.html', {'warning': warning1})
        else:
            #提示错误信息
            warning2 = "用户不存在或密码错误！"
            return render(request, 'login.html', {'warning': warning2})
        # 与底层服务器之间建立好连接
        return render(request, 'ManagementPlatform.html', {'username': username})

@login_required()
def my_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

######################################亮度处理#####################################################
#共用的亮度sensor数据处理函数
@login_required()
def floodlightMonitor(request):
    result = {}
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = ModbusRtu.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus":item.deviceStatus, "realtimeData":item.realtimeData}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = ModbusRtu.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus": item.deviceStatus,"realtimeData": item.realtimeData}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = ModbusRtu.objects.get(deviceId=id)
        if "sensorWrite" == request.POST['writeType']:
            # 根据id从边缘网关服务器中获取数据
            oldSensor.realtimeData = ClientToServer.sendDeviceId(id)
            # oldSensor.realtimeData = request.POST['realtimeData']
            oldSensor.save(update_fields=['realtimeData'])
        #web端写
        else:
            sensorName = request.POST['sensorName']
            # 如果找到该名称
            if len(ModbusRtu.objects.filter(name=sensorName)):
                # 且该名称与其他名称重合，不能修改
                if oldSensor.name != sensorName:
                    result["editStatus"] = "该名称已存在！"
                # 是原来的名称，可以修改
                else:
                    result["editStatus"] = "修改成功！"
                    oldSensor.deviceStatus = request.POST['deviceStatus']
                    oldSensor.save(update_fields=['deviceStatus'])
            # 新的唯一的名称，直接修改
            else:
                result["editStatus"]="修改成功！"
                oldSensor.name = sensorName
                oldSensor.save(update_fields=['name'])
                oldSensor.deviceStatus = request.POST['deviceStatus']
                oldSensor.save(update_fields=['deviceStatus'])
    return JsonResponse(result)

#增加，删除亮度传感器
@login_required()
def floodlightSensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorName = request.POST['sensorName']
        sensorID = request.POST['sensorID']
        if len(ModbusRtu.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = ModbusRtu(name=sensorName, deviceStatus=True, deviceId = sensorID, realtimeData=0.0)
            aSensor.save()
    #删除传感器
    else:
        # 在表单上传过程中会伴随着值 这个值是在生成表单时所隐藏的设备id 传递
        sensorId = request.GET['sensorId']
        ModbusRtu.objects.get(deviceId=sensorId).delete()
    return JsonResponse(result)

######################################温度处理#####################################################
#共用的sensor数据处理函数
@login_required()
def temperatureMonitor(request):
    result = {}
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = Can.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus":item.deviceStatus, "realtimeData": item.realtimeData}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = Can.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus": item.deviceStatus,"realtimeData": item.realtimeData}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = Can.objects.get(deviceId=id)
        if "sensorWrite" == request.POST['writeType']:
            # 直接使用服务器获取数据
            # oldSensor.realtimeData = request.POST['realtimeData']
            oldSensor.realtimeData = ClientToServer.sendDeviceId(id)
            oldSensor.save(update_fields=['realtimeData'])
        #web端写
        else:
            sensorName = request.POST['sensorName']
            # 如果找到该名称
            if len(Can.objects.filter(name=sensorName)):
                # 且该名称与其他名称重合，不能修改
                if oldSensor.name != sensorName:
                    result["editStatus"] = "该名称已存在！"
                # 是原来的名称，可以修改
                else:
                    result["editStatus"] = "修改成功！"
                    oldSensor.deviceStatus = request.POST['deviceStatus']
                    oldSensor.save(update_fields=['deviceStatus'])
            # 新的唯一的名称，直接修改
            else:
                result["editStatus"]="修改成功！"
                oldSensor.name = sensorName
                oldSensor.save(update_fields=['name'])
                oldSensor.deviceStatus = request.POST['deviceStatus']
                oldSensor.save(update_fields=['deviceStatus'])
    return JsonResponse(result)

#增加，删除传感器
@login_required()
def temperatureSensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorName = request.POST['sensorName']
        sensorID = request.POST['sensorID']
        if len(Can.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = Can(name=sensorName, deviceStatus=True, deviceId = sensorID, realtimeData=0.0)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        Can.objects.get(deviceId=sensorId).delete()
    return JsonResponse(result)

######################################湿度处理#####################################################
#共用的湿度sensor数据处理函数
@login_required()
def humidityMonitor(request):
    result = {}
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = ModbusTcp.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus":item.deviceStatus, "realtimeData":item.realtimeData}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = ModbusTcp.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus": item.deviceStatus, "realtimeData": item.realtimeData}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = ModbusTcp.objects.get(deviceId=id)
        if "sensorWrite" == request.POST['writeType']:
            oldSensor.realtimeData = ClientToServer.sendDeviceId(id)
            # oldSensor.realtimeData = request.POST['realtimeData']
            oldSensor.save(update_fields=['realtimeData'])
        #web端写
        else:
            sensorName = request.POST['sensorName']
            # 如果找到该名称
            if len(ModbusTcp.objects.filter(name=sensorName)):
                # 且该名称与其他名称重合，不能修改
                if oldSensor.name != sensorName:
                    result["editStatus"] = "该名称已存在！"
                # 是原来的名称，可以修改
                else:
                    result["editStatus"] = "修改成功！"
                    oldSensor.deviceStatus = request.POST['deviceStatus']
                    oldSensor.save(update_fields=['deviceStatus'])
            # 新的唯一的名称，直接修改
            else:
                result["editStatus"]="修改成功！"
                oldSensor.name = sensorName
                oldSensor.save(update_fields=['name'])
                oldSensor.deviceStatus = request.POST['deviceStatus']
                oldSensor.save(update_fields=['deviceStatus'])
    return JsonResponse(result)

#增加，删除湿度传感器
@login_required()
def humiditySensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorName = request.POST['sensorName']
        sensorID = request.POST['sensorID']
        if len(ModbusTcp.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = ModbusTcp(name=sensorName, deviceStatus=True, deviceId = sensorID, realtimeData=0.0)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        ModbusTcp.objects.get(deviceId=sensorId).delete()
    return JsonResponse(result)

######################################大气压强传感器#####################################################
#共用的大气压强sensor数据处理函数
@login_required()
def atomPressMonitor(request):
    result = {}
    #读取传感器数据
    if request.method == "GET":
        #来自传感器模拟的读请求,返回工作中的传感器
        if "sensorRead" == request.GET['read']:
            #filter方法：匹配到数据时返回一个列表，不可以对查询到的数据进行修改(没有.save()方法)。没有匹配到数据时会返回一个空列表[].
            workingSensors = RaspberryPi.objects.filter(deviceStatus = True)
            workingSensorsJSONArray = []
            for item in workingSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus": item.deviceStatus, "realtimeData": item.realtimeData}
                workingSensorsJSONArray.append(temp)
            result={"workingSensorsJSON":workingSensorsJSONArray}
        # 来自监视器网页的读请求
        else:
            allSensors = RaspberryPi.objects.all()
            allSensorsJSONArray = []
            for item in allSensors:
                temp = {"id": item.deviceId, "name": item.name, "deviceStatus": item.deviceStatus,"realtimeData": item.realtimeData}
                allSensorsJSONArray.append(temp)
            result = {"allSensorsJSON": allSensorsJSONArray}
    #传感器和web端更新传感器数据的操作
    else:
        id = request.POST['id']
        oldSensor = RaspberryPi.objects.get(deviceId=id)
        if "sensorWrite" == request.POST['writeType']:
            oldSensor.realtimeData = ClientToServer.sendDeviceId(id)
            # oldSensor.realtimeData = request.POST['realtimeData']
            oldSensor.save(update_fields=['realtimeData'])
        #web端写
        else:
            sensorName = request.POST['sensorName']
            # 如果找到该名称
            if len(RaspberryPi.objects.filter(name=sensorName)):
                # 且该名称与其他名称重合，不能修改
                if oldSensor.name != sensorName:
                    result["editStatus"] = "该名称已存在！"
                # 是原来的名称，可以修改
                else:
                    result["editStatus"] = "修改成功！"
                    oldSensor.deviceStatus = request.POST['deviceStatus']
                    oldSensor.save(update_fields=['deviceStatus'])
            # 新的唯一的名称，直接修改
            else:
                result["editStatus"]="修改成功！"
                oldSensor.name = sensorName
                oldSensor.save(update_fields=['name'])
                oldSensor.deviceStatus = request.POST['deviceStatus']
                oldSensor.save(update_fields=['deviceStatus'])
    return JsonResponse(result)

#增加，删除大气压强传感器
@login_required()
def atomPressSensor(request):
    result = {}
    #新增传感器
    if request.method == "POST":
        sensorName = request.POST['sensorName']
        sensorID = request.POST['sensorID']
        if len(RaspberryPi.objects.filter(name=sensorName)):
            result["addStatus"]="名称已存在！"
        else:
            result["addStatus"] = "添加成功！"
            aSensor = RaspberryPi(name=sensorName, deviceStatus=True, deviceId = sensorID, realtimeData=0.0)
            aSensor.save()
    #删除传感器
    else:
        sensorId = request.GET['sensorId']
        RaspberryPi.objects.get(deviceId=sensorId).delete()
    return JsonResponse(result)


######################################图表显示#####################################################
@login_required()
def SystemView(request):
    username = request.user.get_username()
    return render(request,'SystemView.html', {'username': username})

@login_required()
def DeviceDis(request):
    username = request.user.get_username()
    return render(request, 'SystemDevice.html', {'username': username})

@login_required()
def DeviceUrl(request):
    username = request.user.get_username()
    return render(request, 'SystemUrl.html', {'username': username})


def LogPlat(request):
    username = request.user.get_username()
    return render(request, 'SystemLog.html', {'username': username})