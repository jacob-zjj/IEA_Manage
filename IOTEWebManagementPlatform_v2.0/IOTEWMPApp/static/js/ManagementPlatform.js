function pauseTime(millTime) {
    var start=Date.now();
    while(true){
    var nowTime=Date.now();
    var offset=nowTime-start;
    if(offset>=millTime)
        break;
    }
}
simulateFloodlightSensor = function () {
    //先从服务器读取 当前 处于工作中 的注册设备，更新设备的检测数据，关键是根据设备的id进行读写

    $.get("/floodlightMonitor/", {read: "sensorRead"}, function (data) {
        var workingSensors = data.workingSensorsJSON; //返回值是JSON
        //随机改变检测的数据
        for (var i = 0; i < workingSensors.length; i++) {
            newSensor = workingSensors[i];
            // newSensor.realtimeData = 350 + Math.round(50*Math.random()*100)/100; //有效数字精确到小数点后两位
            //上传数据到服务器,不能直接传一个sensor对象，只好拆开,但只需部分数据
            var id = newSensor.id;
            console.log(id);
            // var realtimeData = newSensor.realtimeData;
            // $.post("/floodlightMonitor/", {writeType: "sensorWrite", id:id, realtimeData:realtimeData});//用sensorName是为了与编辑操作的公用服务器端操作的request.POST['sensorName']保持一致
            $.post("/floodlightMonitor/", {writeType: "sensorWrite", id: id});
            pauseTime(300);
        }
    },"JSON")
};

simulateTemperatureSensor = function () {
    //先从服务器读取 当前 处于工作中 的注册设备，更新设备的检测数据，关键是根据设备的id进行读写

    $.get("/temperatureMonitor/", {read: "sensorRead"}, function (data) {
        var workingSensors = data.workingSensorsJSON; //返回值是JSON
        //随机改变检测的数据
        for (var i = 0; i < workingSensors.length; i++) {
            newSensor = workingSensors[i];
            //newSensor.temperature = 50 + Math.round(50*Math.random()*100)/100; //有效数字精确到小数点后两位
            //上传数据到服务器,不能直接传一个sensor对象，只好拆开,但只需部分数据
            var id = newSensor.id;
            //var realtimeData = newSensor.temperature;
            //$.post("/temperatureMonitor/", {writeType: "sensorWrite", id:id, temperature:temperature});//用sensorName是为了与编辑操作的公用服务器端操作的request.POST['sensorName']保持一致
            //$.post("/temperatureMonitor/", {writeType: "sensorWrite", id:id, realtimeData:realtimeData});
            $.post("/temperatureMonitor/", {writeType: "sensorWrite", id:id});
            //这里设置睡眠时间就是因为边缘网关服务器和云端服务器之间的延迟
            pauseTime(300);
        }
    },"JSON")
};

simulateHumiditySensor = function () {
    //先从服务器读取 当前 处于工作中 的注册设备，更新设备的检测数据，关键是根据设备的id进行读写

    $.get("/humidityMonitor/", {read: "sensorRead"}, function (data) {
        var workingSensors = data.workingSensorsJSON; //返回值是JSON
        //随机改变检测的数据
        for (var i = 0; i < workingSensors.length; i++) {
            newSensor = workingSensors[i];
            // newSensor.humidity = 50 + Math.round(50*Math.random()*100)/100; //有效数字精确到小数点后两位

            //上传数据到服务器,不能直接传一个sensor对象，只好拆开,但只需部分数据
            var id = newSensor.id;
            // var realtimeData = newSensor.humidity;
            // $.post("/humidityMonitor/", {writeType: "sensorWrite", id:id, realtimeData:realtimeData});//用sensorName是为了与编辑操作的公用服务器端操作的request.POST['sensorName']保持一致
            $.post("/humidityMonitor/", {writeType: "sensorWrite", id:id });
            pauseTime(300);
        }
    },"JSON")
};

simulateatomPressSensor = function () {
    //先从服务器读取 当前 处于工作中 的注册设备，更新设备的检测数据，关键是根据设备的id进行读写

    $.get("/atomPressMonitor/", {read: "sensorRead"}, function (data) {
        var workingSensors = data.workingSensorsJSON; //返回值是JSON
        //随机改变检测的数据
        for (var i = 0; i < workingSensors.length; i++) {
            newSensor = workingSensors[i];
            // newSensor.atomPress = 50 + Math.round(50*Math.random()*100)/100; //有效数字精确到小数点后两位
            //上传数据到服务器,不能直接传一个sensor对象，只好拆开,但只需部分数据
            var id = newSensor.id;
            // var realtimeData = newSensor.atomPress;
            //用sensorName是为了与编辑操作的公用服务器端操作的request.POST['sensorName']保持一致
            // $.post("/atomPressMonitor/", {writeType: "sensorWrite", id:id, realtimeData:realtimeData});
            $.post("/atomPressMonitor/", {writeType: "sensorWrite", id:id });
            pauseTime(300);
        }
    },"JSON")
};

reloadFloodlightTable = function () {
    $.ajax({
        url: "/floodlightMonitor/",
        data: {read: "webRead"},
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            $("#monitorTable").children("tbody").empty();
            var htmlstr = "";
            for (var i = 0; i < data.allSensorsJSON.length; i++) {
                //将boolean型设备状态数据转换成文字；在model中也可以直接使用CharField表示，但若考虑使用较少的存储空间则使用boolean更好
                var deviceStatusString;
                if (true == data.allSensorsJSON[i].deviceStatus)//在服务器里写入时是True，不知道为什么这里读出来是true
                    deviceStatusString = "工作";
                else
                    deviceStatusString = "暂停";
//                if (data.allSensorsJSON[i].luminance > 399)
//                    alert("设备：【" + data.allSensorsJSON[i].name + "】 监测到的亮度过高！" + "\n为：" + data.allSensorsJSON[i].luminance + " lm" + "\n超过399 lm限制！");
                var unit = "";
                if(data.allSensorsJSON[i].id == "0" || data.allSensorsJSON[i].id == "3" )
                {
                    unit = "RH%";
                }else if(data.allSensorsJSON[i].id == "1" || data.allSensorsJSON[i].id == "4" || data.allSensorsJSON[i].id == "7" || data.allSensorsJSON[i].id == "9")
                {
                    unit = "℃";
                }else if(data.allSensorsJSON[i].id == "2" || data.allSensorsJSON[i].id == "5")
                {
                    unit = "lux";
                }else if(data.allSensorsJSON[i].id == "6" || data.allSensorsJSON[i].id == "8")
                {
                    unit = "kpa";
                }else{
                    unit = "UN"
                }

                htmlstr = htmlstr +
                    "<tr>" +
                    // 这里的hidden是用来后面进行删除时 能够得到对应删除的id
                    "<td class='hidden'>" + data.allSensorsJSON[i].id + "</td>" +
                    "<td style='text-align:left'>" + (i + 1) + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].name + "</td>" +
                    "<td style='text-align:center'>" + deviceStatusString + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].realtimeData + " " + unit + "</td>" +

                    "<td class='text-center'>" +
                    "<a type='button' class='btn btn-xs btn-success btnEdit'>编辑</a>" +
                    "<a type='button' class='btn btn-xs btn-danger btnDel'>删除</a>" +
                    "</td>" +
                    "</tr>";
            }
            $("#monitorTable").children("tbody").html(htmlstr);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('获取数据错误, 请先开启服务器');
        }
    })
};

reloadTemperatureTable = function () {
    $.ajax({
        url: "/temperatureMonitor/",
        data: {read: "webRead"},
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            $("#monitorTable").children("tbody").empty();
            var htmlstr = "";
            for (var i = 0; i < data.allSensorsJSON.length; i++) {
                //将boolean型设备状态数据转换成文字；在model中也可以直接使用CharField表示，但若考虑使用较少的存储空间则使用boolean更好
                var deviceStatusString;
                if (true == data.allSensorsJSON[i].deviceStatus)//在服务器里写入时是True，不知道为什么这里读出来是true
                    deviceStatusString = "工作";
                else
                    deviceStatusString = "暂停";

//                if (99 < data.allSensorsJSON[i].temperature)
//                    alert("设备：【" + data.allSensorsJSON[i].name + "】 监测到的温度过高！" + "\n为：" + data.allSensorsJSON[i].temperature + "°C" + "\n超过99°C限制！");

                htmlstr = htmlstr +
                    "<tr>" +
                    // 这里的hidden是用来后面进行删除时 能够得到对应删除的id
                    "<td class='hidden'>" + data.allSensorsJSON[i].id + "</td>" +
                    "<td style='text-align:left'>" + (i + 1) + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].name + "</td>" +
                    "<td style='text-align:center'>" + deviceStatusString + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].realtimeData + "°C" + "</td>" +

                    "<td class='text-center'>" +
                    "<a type='button' class='btn btn-xs btn-success btnEdit'>编辑</a>" +
                    "<a type='button' class='btn btn-xs btn-danger btnDel'>删除</a>" +
                    "</td>" +
                    "</tr>";
            }
            $("#monitorTable").children("tbody").html(htmlstr);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('获取数据错误, 请先开启服务器');
        }
    })
};

reloadHumidityTable = function () {
    $.ajax({
        url: "/humidityMonitor/",
        data: {read: "webRead"},
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            $("#monitorTable").children("tbody").empty();
            var htmlstr = "";

            for (var i = 0; i < data.allSensorsJSON.length; i++) {

                //将boolean型设备状态数据转换成文字；在model中也可以直接使用CharField表示，但若考虑使用较少的存储空间则使用boolean更好
                var deviceStatusString;
                if (true == data.allSensorsJSON[i].deviceStatus)//在服务器里写入时是True，不知道为什么这里读出来是true
                    deviceStatusString = "工作";
                else
                    deviceStatusString = "暂停";

//                if (99 < data.allSensorsJSON[i].humidity)
//                    alert("设备：【" + data.allSensorsJSON[i].name + "】 监测到的湿度过高！" + "\n为：" + data.allSensorsJSON[i].humidity + "%" + "\n超过99%限制！");

                var unit = "";
                if(data.allSensorsJSON[i].id == "14")
                {
                    unit = "ppm";
                }else if(data.allSensorsJSON[i].id == "15")
                {
                    unit = "lux";
                }else{
                    unit = "UN"
                }

                htmlstr = htmlstr +
                    "<tr>" +
                    // 这里的hidden是用来后面进行删除时 能够得到对应删除的id
                    "<td class='hidden'>" + data.allSensorsJSON[i].id + "</td>" +
                    "<td style='text-align:left'>" + (i + 1) + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].name + "</td>" +
                    "<td style='text-align:center'>" + deviceStatusString + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].realtimeData + " " + unit + "</td>" +

                    "<td class='text-center'>" +
                    "<a type='button' class='btn btn-xs btn-success btnEdit'>编辑</a>" +
                    "<a type='button' class='btn btn-xs btn-danger btnDel'>删除</a>" +
                    "</td>" +
                    "</tr>";
            }
            $("#monitorTable").children("tbody").html(htmlstr);

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('获取数据错误, 请先开启服务器');
        }
    })
};

reloadatomPressTable = function () {
    $.ajax({
        url: "/atomPressMonitor/",
        data: {read: "webRead"},
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            $("#monitorTable").children("tbody").empty();
            var htmlstr = "";

            for (var i = 0; i < data.allSensorsJSON.length; i++) {
                //将boolean型设备状态数据转换成文字；在model中也可以直接使用CharField表示，但若考虑使用较少的存储空间则使用boolean更好
                var deviceStatusString;
                if (true == data.allSensorsJSON[i].deviceStatus)//在服务器里写入时是True，不知道为什么这里读出来是true
                    deviceStatusString = "工作";
                else
                    deviceStatusString = "暂停";

//                if (99 < data.allSensorsJSON[i].humidity)
//                    alert("设备：【" + data.allSensorsJSON[i].name + "】 监测到的湿度过高！" + "\n为：" + data.allSensorsJSON[i].humidity + "%" + "\n超过99%限制！");

                htmlstr = htmlstr +
                    "<tr>" +
                    // 这里的hidden是用来后面进行删除时 能够得到对应删除的id
                    "<td class='hidden'>" + data.allSensorsJSON[i].id + "</td>" +
                    "<td style='text-align:left'>" + (i + 1) + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].name + "</td>" +
                    "<td style='text-align:center'>" + deviceStatusString + "</td>" +
                    "<td style='text-align:center'>" + data.allSensorsJSON[i].realtimeData + " ℃" + "</td>" +

                    "<td class='text-center'>" +
                    "<a type='button' class='btn btn-xs btn-success btnEdit'>编辑</a>" +
                    "<a type='button' class='btn btn-xs btn-danger btnDel'>删除</a>" +
                    "</td>" +
                    "</tr>";
            }
            $("#monitorTable").children("tbody").html(htmlstr);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('获取数据错误, 请先开启服务器');
        }
    })
};

$(document).ready(function () {
    var showType = "null";
    var rtuSim, canSim, tcpSim, raspiSim;
    var rtuRel, canRel, tcpRel, raspiRel;

    $("#MODBUSRTUShowBtn").click(function () {
        $("#realTimeData").text("设备实时数据");
        // $("#floodlightShowBtn").attr("class", "btn btn-primary");
        // $("#temperatureShowBtn").attr("class", "btn btn-danger");
        // $("#humidityShowBtn").attr("class", "btn btn-danger");

        if ("can" == showType){
            window.clearInterval(canSim);
            window.clearInterval(canRel);
        }else if ("tcp" == showType){
            window.clearInterval(tcpSim);
            window.clearInterval(tcpRel);
        }else if("raspi" == showType){
            window.clearInterval(raspiSim);
            window.clearInterval(raspiRel);
        }

        showType = "rtu";
        reloadFloodlightTable();
        //这里表示2.5s进行一次模拟器模拟
        rtuSim = window.setInterval(simulateFloodlightSensor, 3000);
        //表示2s刷新一次对应的数据表
        rtuRel = window.setInterval(reloadFloodlightTable, 3000);
    });

     $("#CANShowBtn").click(function () {
        $("#realTimeData").text("设备实时数据");
        // $("#temperatureShowBtn").attr("class", "btn btn-primary");
        // $("#humidityShowBtn").attr("class", "btn btn-danger");
        // $("#floodlightShowBtn").attr("class", "btn btn-danger");

        if ("rtu" == showType){
            window.clearInterval(rtuSim);
            window.clearInterval(rtuRel);
        }else if ("tcp" == showType){
            window.clearInterval(tcpSim);
            window.clearInterval(tcpRel);
        }else if("raspi" == showType){
            window.clearInterval(raspiSim);
            window.clearInterval(raspiRel);
        }

        showType = "can";
        reloadTemperatureTable();
        canSim = window.setInterval(simulateTemperatureSensor, 2000);
        canRel = window.setInterval(reloadTemperatureTable, 2000);
    });

    $("#MODBUSTCPShowBtn").click(function () {
        $("#realTimeData").text("设备实时数据");
        // $("#humidityShowBtn").attr("class", "btn btn-primary");
        // $("#floodlightShowBtn").attr("class", "btn btn-danger");
        // $("#temperatureShowBtn").attr("class", "btn btn-danger");

       if ("rtu" == showType){
           window.clearInterval(rtuSim);
           window.clearInterval(rtuRel);
       }else if ("can" == showType){
           window.clearInterval(canSim);
           window.clearInterval(canRel);
       }else if("raspi" == showType){
            window.clearInterval(raspiSim);
            window.clearInterval(raspiRel);
        }

        showType = "tcp";
        reloadHumidityTable();
        tcpSim = window.setInterval(simulateHumiditySensor, 2000);
        tcpRel = window.setInterval(reloadHumidityTable, 2000);
    });

    $("#RaspberryPiShowBtn").click(function () {
        $("#realTimeData").text("设备实时数据");
        // $("#humidityShowBtn").attr("class", "btn btn-primary");
        // $("#floodlightShowBtn").attr("class", "btn btn-danger");
        // $("#temperatureShowBtn").attr("class", "btn btn-danger");

        //清空其他类型的数据显示
       if ("rtu" == showType){
           window.clearInterval(rtuSim);
           window.clearInterval(rtuRel);
       }else if ("can" == showType){
           window.clearInterval(canSim);
           window.clearInterval(canRel);
       }else if ("tcp" == showType){
            window.clearInterval(tcpSim);
            window.clearInterval(tcpRel);
        }

       //设置当前的显示类型
        showType = "raspi";
        reloadatomPressTable();
        raspiSim = window.setInterval(simulateatomPressSensor, 2000);
        raspiRel = window.setInterval(reloadatomPressTable, 2000);
    });

    $("#addSensor").click( function () {
        if ("null" == showType){
            alert("请先选择显示的传感器种类！")
        }else{
            save_method = 'add';
            $('#form')[0].reset(); // 重置form
            $('#controlDiv').hide();//隐藏控制选项
            //这里无法向下进行
            $('#modal_form').modal('show'); // 显示modal

            // 设置title
            if ("rtu" == showType)
                $('.modal-title').text('新建modbus-rtu设备');
            else if ("can" == showType)
                $('.modal-title').text('新建can设备');
            else if ("tcp" == showType)
                $('.modal-title').text('新建modbus-tcp设备');
            else if ("raspi" == showType)
                $('.modal-title').text('新建树莓派设备');
        }
    });

    $("#monitorTable").on('click', ".btnEdit", function () {
        save_method = 'update';
        $('#form')[0].reset();
        $("#controlDiv").show();//显示控制选项
        $('[name="id"]').val($(this).parent("td").siblings("td.hidden").text());

        //把deviceStatus的值填入表单，及根据deviceStatus的值显示不同的按钮样式，文字
        var deviceStatus;
        if ("工作" == $(this).parent("td").prev().prev().text()) {
            deviceStatus = "True";//需要加 “”
            $("#btnControl").attr("class", "btn btn-danger");
            $("#btnControl").text("暂停监测");
        }else{
            deviceStatus = "False";
            $("#btnControl").attr("class", "btn btn-primary");
            $("#btnControl").text("启动监测");
        }
        $('[name="deviceStatus"]').val(deviceStatus);
        $('[name="sensorName"]').val($(this).parent("td").prev().prev().prev().text());
        $('#modal_form').modal('show');
        $('.modal-title').text('编辑传感器名称');
    });

    $("#monitorTable").on('click', ".btnDel", function () {
        // 设置url
        var url;
        if ("rtu" == showType)
            url = "/floodlightSensor/";
        else if ("can" == showType)
            url = "/temperatureSensor/";
        else if ("tcp" == showType)
            url = "/humiditySensor/";
        else
            url = "/atomPressSensor/";
        $.ajax({
            url: url,
            type: "GET",
            data: {sensorId: $(this).parent("td").siblings("td.hidden").text()},
            dataType: "JSON",
            success: function () {
                //如果成功，隐藏弹出框并重新加载数据
                $('#modal_form').modal('hide');
                if ("rtu" == showType)
                     reloadFloodlightTable();
                else if ("can" == showType)
                     reloadTemperatureTable();
                else if ("tcp" == showType)
                     reloadHumidityTable();
                else
                     reloadatomPressTable();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('删除错误！');
            }
        })
    });

    $("#btnSave").click(function () {
        var url;

        if (save_method == 'add') {
            // 设置url
            if ("rtu" == showType)
                url = "/floodlightSensor/";
            else if ("can" == showType)
                url = "/temperatureSensor/";
            else if ("tcp" == showType)
                url = "/humiditySensor/";
            else
                url = "/atomPressSensor/";

            $.ajax({
                url: url,
                type: "POST",
                data:$('#form').serialize(),
                dataType: "JSON",
                success: function (data) {
                    if ("名称已存在！" == data.addStatus){
                        alert(data.addStatus);
                    }else{
                        //如果成功，隐藏弹出框并重新加载数据
                        $('#modal_form').modal('hide');
                        if ("rtu" == showType)
                            reloadFloodlightTable();
                        else if ("can" == showType)
                            reloadTemperatureTable();
                        else if ("tcp" == showType)
                            reloadHumidityTable();
                        else
                            reloadatomPressTable();
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert("新建错误！");
                }
             })
        }
        else {//编辑
            // 设置url
            if ("rtu" == showType)
                url = "/floodlightMonitor/";
            else if ("can" == showType)
                url = "/temperatureMonitor/";
            else if ("tcp" == showType)
                url = "/humidityMonitor/";
            else
                url = "/atomPressMonitor/";

            $.ajax({
                url: url,
                type: "POST",
                data:$('#form').serialize(),
                dataType: "JSON",
                success: function (data) {
                    if ("该名称已存在！" == data.editStatus){
                        alert(data.editStatus);
                    }else{
                        //如果成功，隐藏弹出框并重新加载数据
                        $('#modal_form').modal('hide');
                        if ("rtu" == showType)
                            reloadFloodlightTable();
                        else if ("can" == showType)
                            reloadTemperatureTable();
                        else if ("tcp" == showType)
                            reloadHumidityTable();
                        else
                            reloadatomPressTable();
                    }
                },
                 error: function (jqXHR, textStatus, errorThrown) {
                    alert("修改错误！");
                 }
             })
        }
    });

    $("#btnControl").click(function () {
        //改变deviceStatus的值
        if ("True" == $('[name="deviceStatus"]').val()) {//注意，在btnEdit按钮里处理时填入的是True，
            $('[name="deviceStatus"]').val("False");
        }else {
            $('[name="deviceStatus"]').val("True");
        }

        // 设置url
        var url;
        if ("rtu" == showType)
            url = "/floodlightMonitor/";
        else if ("can" == showType)
            url = "/temperatureMonitor/";
        else if ("tcp" == showType)
            url = "/humidityMonitor/";
        else
            url = "/atomPressMonitor/";

        $.ajax({
            url: url,
            type: "POST",
            data:$('#form').serialize(),
            dataType: "JSON",
            success: function (data) {//因为修改状态和名称的界面是同一个界面，提交的时候也应判断名称是否被修改成已存在名称
                if ("该名称已存在！" == data.editStatus){
                    alert(data.editStatus);
                }else{
                    //如果成功，隐藏弹出框并重新加载数据
                    $('#modal_form').modal('hide');
                    if ("rtu" == showType)
                        reloadFloodlightTable();
                    else if ("can" == showType)
                        reloadTemperatureTable();
                    else if ("tcp" == showType)
                        reloadHumidityTable();
                    else
                        reloadatomPressTable();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('修改设备状态错误！');
            }
        })
    });
});




