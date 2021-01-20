# < div
# id = "container_"
# style = "min-width:400px;height:400px; opacity: 0.85" > < / div >
# < script >
# Highcharts.setOptions({
# global: {
#     useUTC: false
# }
# });
# function
# activeLastPointToolip(chart)
# {
#     var
# points = chart.series[0].points;
# chart.tooltip.refresh(points[points.length - 1]);
# }
# var
# chart = Highcharts.chart('container_', {
#     chart: {
#         type: 'spline',
#         marginRight: 10,
#         events: {
#             load: function() {
#                 var series = this.series[0],
#                              chart = this;
# activeLastPointToolip(chart);
# setInterval(function()
# {
# $.ajax({
#     url: "/floodlightMonitor/",
#     data: {read: "webRead"},
#     type: "GET",
#     dataType: "JSON",
#     success: function(data) {
#         var x = (new Date()).getTime(); // 当前时间
#                                            // 找到第一个工作的节点数据
# var
# y;
# for (var i = 0; i < data.allSensorsJSON.length; i++)
# {
# if (true == data.allSensorsJSON[i].deviceStatus)
# {
# // 找到第一个为true的设备
# 也就是正在运行的设备
# y = data.allSensorsJSON[i].luminance;
# break;
# }
# }
# y = parseFloat(y);
# // 随机值
# series.addPoint([x, y], true, true);
# activeLastPointToolip(chart);
# },
# error: function(jqXHR, textStatus, errorThrown)
# {
#     alert('获取数据错误, 请先开启服务器');
# }
# })
# }, 2500);
# }
# }
# },
# title: {
#     text: '<b>动态模拟实时数据</b>'
# },
# xAxis: {
#     type: 'datetime',
#     tickPixelInterval: 150
# },
# yAxis: {
#     title: {
#         text: null
#     }
# },
# tooltip: {
#     formatter: function() {
# return '<b>' + this.series.name + '</b><br/>' +
# Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
# Highcharts.numberFormat(this.y, 2);
# }
# },
# legend: {
#     enabled: false
# },
# series: [{
# name: '实时数据',
# data: (function() {
# // 生成随机值
# var data =[],
# time = (new Date()).getTime(), \
#                     i;
# for (i = -19; i <= 0; i += 1)
# {
#     data.push({
#               // 2.5
# s显示一次
# x: time + i * 2500,
# // 这里是从开始位置之前使用的是随机值来进行模拟
# y: 350 + Math.round(50 * Math.random() * 100) / 100
# });
# }
# return data;
# }())
# }]
# });
# < / script >