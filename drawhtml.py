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
    # print "dates_count:"
    # dates_count1 = sorted(dates_count)
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
        {name: '1星',value : %(n1)s,color:'#a5c2d5'},
        {name : '2星',value : %(n2)s,color:'#cbab4f'},
        {name : '3星',value : %(n3)s,color:'#76a871'},
        {name : '4星',value : %(n4)s,color:'#9f7961'},
        {name : '5星',value : %(n5)s,color:'#a56f8f'}
    ]''' % {
        'n1': rates[1],
        'n2': rates[2],
        'n3': rates[3],
        'n4': rates[4],
        'n5': rates[5]
    }
    rate_s_data = '''[%(n1)s, %(n2)s, %(n3)s, %(n4)s, %(n5)s ]''' % {
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
    tag_data = '['
    tag_data += ','.join("{name:'" + tag[0] + "',value:"+str(tag[1][0])+",color:'#006666'}" for tag in tags)
    tag_data += ']'
    # print tag_data
    ############################### TODO
    table = ''
    for tag in tags:
        table += '<tr>\n'
        table += '<td>'+tag[0]+'</td>\n'
        table += '<td>'+str(tag[1][0])[:5]+'</td>\n'
        for i in xrange(5):
            table += '<td>'+str(tag[1][2+i])+'</td>\n'
        table += '</tr>\n'
    # print table
    content = '''
    <!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>%(user)s Douban</title>
        <script src="http://echarts.baidu.com/build/dist/echarts.js"></script>
        <script type="text/javascript">
        require.config({
            paths: {
                echarts: 'http://echarts.baidu.com/build/dist'
            }
        });

        // 使用
        require(
            [
                'echarts',
                'echarts/chart/bar' // 使用柱状图就加载bar模块，按需加载
            ],
            function (ec) {
                    // 基于准备好的dom，初始化echarts图表
                    var myChart = ec.init(document.getElementById('canvasRatingBar'));

                    var option = {
                        tooltip: {
                            show: true
                        },
                        legend: {
                            data:['52269090的豆瓣评分']
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
                                data : ['一星', '二星', '三星', '四星', '五星']
                            }
                        ],
                        yAxis : [
                            {
                                type : 'value'
                            }
                        ],
                        series : [
                            {
                                "name":"销量",
                                "type":"bar",
                                "data":%(rate_s_data)s
                            }
                        ]
                    };

                    // 为echarts对象加载数据
                    myChart.setOption(option);
                }
            );
            </script>
    </head>
    <body>
        <div id='canvasRatingBar' style="height:400px; width:800px" ></div>
        <div id='canvasRatingPie'></div>
        <div id='canvasRatingMonth'></div>
        <h4>%(user)s喜欢的标签</h4>
        <table border="1">
        <tr>
          <td>标签</td>
          <td>4，5星占比</td>
          <td>5星</td>
          <td>4星</td>
          <td>3星</td>
          <td>2星</td>
          <td>1星</td>
        </tr>
        %(table)s
        </table>
    </body>
</html>
    ''' % {
        'user': user,
        'rate_s_data': str(rate_s_data),
        'table': table
    }
    with open(os.path.join(filepath, user+'.html'), 'w') as output:
        output.write(content)