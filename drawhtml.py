# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    drawhtml.py
# Description :    输出目标网页
# Author      :    Frank
# Date        :    2014.03.08
# ######################################################


import datetime
import os
from dateutil.relativedelta import relativedelta


def drawHTML(dates, rates, tag_count, user, filepath='htmlfile/'):
    """
    输出带图表的html文件
    :param dates:  观看时间的列表， 例如：[('2015-02-22', '5'), ('2013-07-12', '3')]
    :param rates:  评价列表， 例如：[0, 4, 2, 1, 5, 44]
    :param tag_count: 字典，例如：{'': [0, 1, 0, 0, 0, 7],}
    :param user: 用户Id
    :return:
    """
    dates = sorted(dates)
    # print dates
    start_month = datetime.datetime.strptime(dates[0][0][:-3], '%Y-%m')  # 开始记录观影的时间
    end_month = datetime.datetime.strptime(dates[-1][0][:-3], '%Y-%m')   # 结束记录观影的时间
    # print start_month, end_month
    dates_count = {}
    for date in dates:
        if date[0][:-3] not in dates_count:
            dates_count[date[0][:-3]] = 0
        dates_count[date[0][:-3]] += 1
    month = start_month
    month_count = []
    month_name = []
    # print dates_count1
    while month <= end_month:
        m = month.strftime('%Y-%m')
        if m in dates_count:
            month_count.append(dates_count[m])
        else:
            month_count.append(0)
        if int(month.strftime('%m')) % 3 == 0:
            month_name.append(month.strftime('%y-%m'))
        else:
            month_name.append('')
        month = month + relativedelta(months=1)
    # print month_count
    # print month_name
    rates_s = '''[
        {value : %(n1)s, name: '1星'},
        {value : %(n2)s, name : '2星'},
        {value : %(n3)s, name : '3星'},
        {value : %(n4)s, name : '4星'},
        {value : %(n5)s, name : '5星'}
    ]''' % {
        'n1': rates[1],
        'n2': rates[2],
        'n3': rates[3],
        'n4': rates[4],
        'n5': rates[5]
    }
    rate_s_data_num = '''[%(n1)s, %(n2)s, %(n3)s, %(n4)s, %(n5)s ]''' % {
        'n1': rates[1],
        'n2': rates[2],
        'n3': rates[3],
        'n4': rates[4],
        'n5': rates[5]
    }
    tags = [(tag, [float(sum(count[4:]))/sum(count), float(count[5])/sum(count),  # 4 5星加起来占比，5星占比
            count[5], count[4], count[3], count[2], count[1]])
            for tag, count in tag_count.iteritems() if sum(count) > 3 and len(tag.strip()) > 0]
    tags = sorted(tags, key=lambda x: x[1], reverse=True)
    # print tags

    item_nodes = '['
    item_nodes += ','.join("{name:'" + tag[0] + "',value:"+str(100*float(tag[1][0]))[:5]+"}" for tag in tags)
    item_nodes += ']'
    print item_nodes
    content = '''
    <!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>%(user)s Douban</title>
        <script src="./echarts220/build/dist/echarts.js"></script>
        <script type="text/javascript">
        require.config({
            paths: {
                echarts: './echarts220/build/dist'
            }
        });

        // 使用
        require(
            [
                'echarts',
                'echarts/chart/bar',  // 使用柱状图就加载bar模块，按需加载
                'echarts/chart/pie',
                'echarts/chart/line',
                'echarts/chart/force'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var barChart = ec.init(document.getElementById('canvasRatingBar'));
                var barOption = {
                    title:{
                        text:'%(user)s的豆瓣评分',
                        x:'center'
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%%)"
                    },
                    legend: {
                        x:'left',
                        data:['%(user)s的豆瓣评分']
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data : ['1星', '2星', '3星', '4星', '5星']
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    series : [
                        {
                            "name":"%(user)s的豆瓣评分",
                            "type":"bar",
                            "data":%(rate_s_data_num)s,
                            itemStyle:{
                                normal:{
                                    color: function (value){
                                        return "#"+("00000"+((Math.random()*16777215
                                        +0.5)>>0).toString(16)).slice(-6) ;
                                    }
                                }
                            },
                            markPoint : {
                                data : [
                                    {type : 'max', name: '最大值'},
                                    {type : 'min', name: '最小值'}
                                ]
                            }
                        }
                    ]
                };
                // 为echarts对象加载数据
                barChart.setOption(barOption);

                var pieChart = ec.init(document.getElementById('canvasRatingPie'));
                var pieOption = {
                    title : {
                        text:'%(user)s的豆瓣评分分布图',
                        x:'center'
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%%)"
                    },
                    legend: {
                        orient : 'vertical',
                        x : 'left',
                        data:['1星','2星','3星','4星','5星']
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {
                                show: true,
                                type: ['pie', 'funnel'],
                                option: {
                                    funnel: {
                                        x: '25%%',
                                        width: '50%%',
                                        funnelAlign: 'left',
                                        max: 1548
                                    }
                                }
                            },
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    series : [
                        {
                            name:'%(user)s的豆瓣评分',
                            type:'pie',
                            radius : '55%%',
                            center: ['50%%', '60%%'],
                            data: %(rates_s)s
                        }
                    ]
                };
                pieChart.setOption(pieOption);

                var lineChart = ec.init(document.getElementById('canvasRatingMonth'));
                var lineOption = {
                    title: {
                        text: '%(user)s的观影数量分布',
                        x: 'center'
                    },
                    legend: {
                        data:['观看电影数'],
                        x: 'left',
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : %(month_name)s
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            axisLabel : {
                                formatter: '{value} 部'
                            }
                        }
                    ],
                    series: [
                        {
                            name: '%(user)s的观看电影数量分布',
                            type:'line',
                            symbol:'emptyCircle',
                            symbolSize: 5,
                            itemStyle: {
                                normal: {
                                    lineStyle: {            // 系列级个性化折线样式，横向渐变描边
                                        width: 2,
                                        color: (function (){
                                            var zrColor = require('zrender/tool/color');
                                            return zrColor.getLinearGradient(
                                                0, 0, 1000, 0,
                                                [[0, 'rgba(255,0,0,0.8)'],[0.8, 'rgba(255,255,0,0.8)']]
                                            )
                                        })(),
                                        shadowColor : 'rgba(0,0,0,0.5)',
                                        shadowBlur: 10,
                                        shadowOffsetX: 8,
                                        shadowOffsetY: 8
                                    }
                                },
                                emphasis : {
                                    label : {show: true}
                                }
                            },
                            markLine : {
                                data : [
                                    {type : 'average', name: '平均值'}
                                ]
                            },
                            data: %(month_count)s
                        }
                    ]
                };
                lineChart.setOption(lineOption);

                var forceChart = ec.init(document.getElementById('canvasFavItem'));
                var forceOption = {
                    title : {
                        text: '%(user)s的标签',
                        x:'center'
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c}%%"
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            restore : {show: true},
                            magicType: {show: true, type: ['force', 'chord']},
                            saveAsImage : {show: true}
                        }
                    },
                    legend: {
                        x: 'left',
                        data:['标签']
                    },
                    series : [
                        {
                            type:'force',
                            name : "标签4，5星占比",
                            ribbonType: false,
                            itemStyle: {
                                normal: {
                                    label: {
                                        show: true,
                                        textStyle: {
                                            color: '#333'
                                        }
                                    },
                                    nodeStyle : {
                                        brushType : 'both',
                                        borderColor : 'rgba(255,215,0,0.4)',
                                        borderWidth : 1
                                    }
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                                    },
                                    nodeStyle : {
                                        //r: 30
                                    }
                                }
                            },
                            draggable: 'true',
                            useWorker: false,
                            minRadius : 15,
                            maxRadius : 30,
                            gravity: 2.2,
                            scaling: 1.1,
                            roam: 'move',
                            links:[],
                            nodes: %(item_nodes)s
                        }
                    ]
                };
                forceChart.setOption(forceOption);
            }
        );
            </script>
    </head>
    <body>
        <div id='canvasRatingBar' style="height:500px; width:1000px;" ></div>
        <br><br><br><br><br>
        <div id='canvasRatingPie' style="height:500px; width:1000px;"></div>
        <br><br><br><br><br>
        <div id='canvasRatingMonth' style="height:500px; width:1000px;"></div>
        <br><br><br><br><br>
        <div id='canvasFavItem' style="height:800px; width:1000px;"></div>
    </body>
</html>
    ''' % {
        'user': user,
        'rate_s_data_num': str(rate_s_data_num),
        'rates_s': str(rates_s),
        'month_count': str(month_count),
        'month_name': str(month_name),
        'item_nodes': str(item_nodes)
    }
    # print "rates_s:", rates_s
    # print "month_count:", str(month_count)    # 用来画折线图
    # print "month_name:", str(month_name)      # 用来画折线图
    # print "monthwidth:", str(len(month_name) * 20)

    with open(os.path.join(filepath, user+'.html'), 'w') as output:
        output.write(content)