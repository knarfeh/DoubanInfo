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
        <script type="text/javascript" src="../ichart.1.2.min.js"></script>
        <script type="text/javascript">
        $(function(){
            var rates1 = %(rates_s)s;
            var month_data = [
                {
                    name : '次数',
                    value:%(month_count)s,
                    color:'#1f7e92',
                    line_width:2
                }
            ];
            new iChart.Column2D({
                render : 'canvasRatingBar',
                data: rates1,
                title : '%(user)s的豆瓣评分',
                width : 800,
                height : 400,
                animation : true,
                animation_duration:800,
                shadow : true,
                shadow_blur : 2,
                shadow_color : '#aaaaaa',
                shadow_offsetx : 1,
                shadow_offsety : 0,
                coordinate:{
                    background_color:'#fefefe',
                    scale:[{
                        position:'left'
                    }]
                }
            }).draw();
            new iChart.Pie2D({
                render : 'canvasRatingPie',
                data: rates1,
                title : '%(user)s的豆瓣评分',
                legend : {
                    enable : true
                },
                sub_option : {
                    label : {
                        background_color:null,
                        sign:false,
                        padding:'0 4',
                        border:{
                            enable:false,
                            color:'#666666'
                        },
                        fontsize:11,
                        fontweight:600,
                        color : '#4572a7'
                    },
                    border : {
                        width : 2,
                        color : '#ffffff'
                    }
                },
                animation:true,
                showpercent:true,
                decimalsnum:2,
                width : 800,
                height : 400,
                radius:140
            }).draw();

            new iChart.Area2D({
                render : 'canvasRatingMonth',
                data: month_data,
                title : '每月看片数',
                width : %(month_width)s,
                height : 400,
                coordinate:{background_color:'#edf8fa'},
                sub_option:{
                        smooth : true,
                        hollow_inside:false,
                        point_size:10
                },
                tip:{
                    enable:true,
                    shadow:true
                },
                labels:%(month_name)s
            }).draw();
        });

        </script>
    </head>
    <body>
        <div id='canvasRatingBar'></div>
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
        'rates_s': rates_s,
        'month_count': str(month_count),
        'month_name': str(month_name),
        'month_width': str(len(month_name)*20),
        'table': table
    }
    with open(os.path.join(filepath, user+'.html'), 'w') as output:
        output.write(content)