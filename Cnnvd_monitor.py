# -*- coding:utf-8 -*-
import dominate
import requests
from bs4 import BeautifulSoup
import os
import re
import xlwt
import time
import datetime
from io import BytesIO
import sqlite3
import json
from xlrd import open_workbook
from dominate.tags import *

access_token = ''
#该函数用于获取单独的一条漏洞详细信息
def getURLDATA(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        'Connection': 'keep-alive', }
    r = requests.get(url, headers=header, timeout=30)
    html = BeautifulSoup(r.text, 'html.parser')
    link = html.find(class_='detail_xq w770')  # 漏洞信息详情
    vuln_name = link.find('h2').text.lstrip().rstrip() #漏洞名称
    vuln_num = re.findall(r'CNNVD-+\d+-+\d+',str(url))[0] #漏洞编号
    link_introduce = html.find(class_='d_ldjj')  # 漏洞简介
    link_others = html.find_all(class_='d_ldjj m_t_20')  # 其他
    one_cve_info = []
    #漏洞名称
    try:
        one_cve_info.append(str(vuln_name))
    except:
        one_cve_info.append("")
    #漏洞在CNNVD上的链接
    try:
        one_cve_info.append(str(url))
    except:
        one_cve_info.append("")
    #漏洞在CNNVD上的编号
    try:
        one_cve_info.append(vuln_num)
    except:
        one_cve_info.append("")
    # 危害等级
    try:

        one_cve_info.append(str(link.contents[3].contents[5].find('a').text.lstrip().rstrip()))
    except:
        #print("危害等级:is empty")
        one_cve_info.append("")
    #CVE编号
    try:
        one_cve_info.append(str(link.contents[3].contents[7].find('a').text.lstrip().rstrip()))
    except:
        #print("CVE编号:is empty")
        one_cve_info.append("")
    #漏洞类型
    try:
        one_cve_info.append(str(link.contents[3].contents[9].find('a').text.lstrip().rstrip()))

    except:
        #print("漏洞类型:is empty")
        one_cve_info.append("")

    #发布时间
    try:
        one_cve_info.append(str(link.contents[3].contents[11].find('a').text.lstrip().rstrip()))
    except:
       # print("发布时间:is empty")
        one_cve_info.append("")
    #威胁类型
    try:
        one_cve_info.append(str(link.contents[3].contents[13].find('a').text.lstrip().rstrip()))
    except:
        #print("威胁类型:is empty")
        one_cve_info.append("")

    #更新时间
    try:
        one_cve_info.append(str(link.contents[3].contents[15].find('a').text.lstrip().rstrip()))
    except:
        #print("更新时间:is empty")
        one_cve_info.append("")
    #厂商
    try:
        one_cve_info.append(str(link.contents[3].contents[17].find('a').text.lstrip().rstrip()))
    except:
        #print("厂商:is empty")
        one_cve_info.append("")

    #漏洞简介
    try:
        link_introduce_data = BeautifulSoup(link_introduce.decode(), 'html.parser').find_all(name='p')
        s = ""
        for i in range(0, len(link_introduce_data)):
            s = s + str(link_introduce_data[i].text.lstrip().rstrip())
        one_cve_info.append(s)
    except:
        one_cve_info.append("")

    if (len(link_others) != 0):
        try:
            # 漏洞公告
            link_others_data1 = BeautifulSoup(link_others[0].decode(), 'html.parser').find_all(name='p')
            s = ""
            for i in range(0, len(link_others_data1)):
                s = s + str(link_others_data1[i].text.lstrip().rstrip())
            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 参考网址
            link_others_data2 = BeautifulSoup(link_others[1].decode(), 'html.parser').find_all(name='p')
            s = ""
            for i in range(0, len(link_others_data2)):
                s = s + str(link_others_data2[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 受影响实体
            link_others_data3 = BeautifulSoup(link_others[2].decode(), 'html.parser').find_all('a', attrs={
                'class': 'a_title2'})
            s = ""
            for i in range(0, len(link_others_data3)):
                s = s + str(link_others_data3[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 补丁
            link_others_data3 = BeautifulSoup(link_others[3].decode(), 'html.parser').find_all('a', attrs={
                'class': 'a_title2'})
            s = ""
            for i in range(0, len(link_others_data3)):
                s = s + str(link_others_data3[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")
    else:
        one_cve_info.append("")
        one_cve_info.append("")
        one_cve_info.append("")
        one_cve_info.append("")
    return one_cve_info


#企业微信消息推送
def wechat_qiye(lever_test):
    #文件下载服务器url
    #url = "http://www.xf*****b.cn/" + filename
    global access_token
    # 自定义应用的 Secret
    Secret = "pyUtd3RYDs**************BY5YYHjAWKjUEpNiQ"
    # 注册的企业 corpid
    corpid = 'wwbfd**********1708'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'

    '''
        先提供Secret以及corpid获取access_token。
    '''
    if access_token == '':

        getr = requests.get(url=url.format(corpid, Secret))
        access_token = getr.json().get('access_token')


    print(access_token)
    data = {
        # "chatid" : "xxx",
        # "touser" : "Test",   # 向这些用户账户发送
        "toparty": "1",  # 向群聊部门发送
        # "msgtype" : "text",
        "agentid": 1000001,  # 应用的 id 号
        # "text" : {
        #     "content" : "一看到你，我就泛起微笑^_^。"
        # },
        "msgtype": "textcard",
        "textcard": {
            "title": "今天的CVE到啦",
            "description": "<div class=\"gray\">"+str(datetime.datetime.now().year)+"年"+str(datetime.datetime.now().month)+"月"+str(datetime.datetime.now().day)+"日</div> <div class=\"normal\">最新CNNVD漏洞情报</div><div class=\"highlight\">"+lever_test+"</div><div class=\"highlight\">请注意查收，嘿嘿嘿</div>",
            "url": "http://www.x*******b.cn/"+str(datetime.datetime.now().date())+".html",
            "btntxt": "获取最新CNNVD的文件"
        },
        "safe": 0
    }

    r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                          data=json.dumps(data))
    print(r.text)
    if str(json.loads(r.text)['errcode']) == '42001':
        #获取新的access_token
        getr = requests.get(url=url.format(corpid, Secret))
        access_token = getr.json().get('access_token')
        #恢复之前因token过期异常失去的请求
        r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                          data=json.dumps(data))
        print(r.text)


def slack_messge():
    pass


#最新漏洞消息、程序报错消息写到日志中，便于后期审查
def write_log(log_time,msg):
    log_file_name ='./log/' + str(datetime.datetime.now().date()) + '.log'
    with open(log_file_name,'a') as f:
        f.write(log_time + " " + msg + "\n")
    f.close()

#创建数据库连接池
def conn_db():
    con = sqlite3.connect("cve_db.db")
    cursor = con.cursor()
    return cursor,con


#数据库插入操作
def insertTo(values):
    sql = 'insert into cve_info values('+values+ ')'
    cursor,con = conn_db()
    try:
        cursor.execute(sql)
        cursor.close()
        con.commit()
        con.close()
    except Exception as e:
        print(e)

#判断某条漏洞信息是否在数据库中存在
def is_not_exist(one_info):
    log_update_time = str(datetime.datetime.now().ctime())
    cursor,con = conn_db()
    sql = "select * from cve_info where cnnvd_num=?"
    try:
        cursor.execute(sql,(str(one_info[2]),))
        info = cursor.fetchone()
        #print(info)
        if info == None:
            insert_msg = "[*]有最新CNNVD编号漏洞:" + one_info[2]
            print(insert_msg)
            write_log(log_update_time,insert_msg)
            return True
        print("[!]无最新CNNVD编号")
        return False
    except Exception as e:
        error_msg = "[x]ERROR: " + str(e)
        print(error_msg)
        write_log(log_update_time,error_msg)
        return False
    finally:
        cursor.close()
        con.close()

#判断数据库是否为空
def is_database_empty():
    cursor,con = conn_db()
    sql = "select count(*) from cve_info"
    try:
        cursor.execute(sql)
        info = cursor.fetchone()
        if info[0] == 0:
            print("[*]当前数据库为空，数据库马上初始化.....")
            return True

        else:
            return False
    except Exception as e:
        print(e)

#查询漏洞信息危害级别
def danger_level_nums():
    cursor,con = conn_db()
    #sql = "select danger_level, count(*) from cve_info  where  danger_level='中危'"
    if datetime.datetime.now().weekday() + 1 == 5:

        sql = "SELECT  danger_level,count(*)  from cve_info where updated_time > datetime('now','-7 days') group by danger_level having count(*)>1"
        #sql1 = "select * from cve_info where [updated_time]>= updated_time('now', 'localtime',  'start of day')"
        try:
            cursor.execute(sql)
            info1 = cursor.fetchall()
            today = datetime.datetime.now().weekday() + 1
            print(today)
            return str(info1)

        except Exception as e:
            print(e)
    else:

        return  "今天记得查看哦"

#excel文件的初始化创建
def sheet_init(f):
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    sheet1.write(0, 0, "漏洞名称")
    sheet1.write(0, 1, "网址")
    sheet1.write(0, 2, "CNNVD编号")
    sheet1.write(0, 3, "危害等级")
    sheet1.write(0, 4, "CVE编号")
    sheet1.write(0, 5, "漏洞类型")
    sheet1.write(0, 6, "发布时间")
    sheet1.write(0, 7, "威胁类型")
    sheet1.write(0, 8, "更新时间")
    sheet1.write(0, 9, "厂商")
    sheet1.write(0, 10, "漏洞简介")
    sheet1.write(0, 11, "漏洞公告")
    sheet1.write(0, 12, "参考网址")
    sheet1.write(0, 13, "受影响实体")
    sheet1.write(0, 14, "补丁")
    return sheet1

# 创建获取excel数据的函数
def excel_sheet_processor(filepath):
    # 通过open_workbook函数 获取Book对象
    wb = open_workbook(filepath, formatting_info=True)
    # 创建一个新的sheet 对象
    ws = wb.sheet_by_index(0)
    # 创建2个空列表用于储存数据
    workbook_list = []
    my_keys = []
    # 通过遍历ncols 获取excel表中第一行（python中0是第一行的意思）和所有列的数据
    for col in range(ws.ncols):
        my_keys.append(ws.cell_value(rowx=0, colx=col))

    # 通过遍历nrows和 获取excel表中所有行里面的和对应列的数据
    for r in range(1,ws.nrows):
        dict = {}
        for pos in range(0, len(my_keys)):
            dict[my_keys[pos]] = ws.cell_value(rowx=r, colx=pos)
        # 将获取的字典数据  添加进一开始写好的空列表中
        workbook_list.append(dict)
    return workbook_list

# 创建excel生成静态html页面的函数
def list_diction_to_html(list_work):
    # 用dominate函数生成静态html页面
    doc = dominate.document(title='最新CVE列表')
    # 写在头部的 css 可以自定义自己的想要用的css文件， （重要： meta一定要加 要不会在打开html时乱码，因为html默认不是utf-8编码）
    with doc.head:
        #stylesheet
        #Perconnel / static / css / style.css
        link(href='style.css', rel='stylesheet', type='text/css')
        meta(charset='utf-8')
    # 创建一个table，将获取到的数据通过遍历添加进去对应的位置
    with doc:
        with div(id='excel_table').add(table(id="qgg-table",border="1px solid #ccc" ,cellspacing="0", cellpadding="0")):
            with thead():
                dict = list_work[0]
                for key in dict.keys():
                    table_header = td()
                    table_header.add(p(key))
            for dict2 in list_work:
                table_row = tr(cls='excel_table_row')
                for key in dict2:
                    with table_row.add(td()):
                        p(dict2[key])
    return str(doc)

#保存HTML文件
def save_dom_to_html(dom):
    today_time = datetime.datetime.now().date()
    filepath = os.path.abspath('/usr/share/nginx/html/download/'+str(today_time)+".html")
    print(filepath)
    htmfile = open(filepath, "w",encoding='utf-8')
    htmfile.write(str(dom))
    htmfile.close()


#主函数
def main():
    excel_row = 1
    try:
        while True:
            file_path = "/usr/share/nginx/html/download/"
            today_time = str(datetime.datetime.now().date())
            fileName = file_path + today_time + '.xls'
            if os.path.isfile(fileName):
                excel_row = excel_row
            else:
                excel_row = 1
            file = open(fileName, mode='ab')#在硬盘上创建EXCEL文件
            stream = BytesIO() # 打开数据流
            f = xlwt.Workbook()  # 创建EXCEL工作簿
            sheet1 = sheet_init(f) # 初始化工作
            pageNo = 1
            flag = False #该标志用于控制是否继续请求CNNVD下一页的数据
            send_msg_flag = False #该标志用于控制是否需要向微信推送消息
            if is_database_empty():
                flag = True
            #print(danger_level_nums()[0])
            #print(danger_level_nums()[1])
            #quit(0)
            #该while循环是
            while True:
                url = 'http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno=' + str(pageNo) + '&repairLd='
                header = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
                    'Connection': 'keep-alive',
                }
                r = requests.get(url, headers=header, timeout=30)
                html = BeautifulSoup(r.text, 'html.parser')
                links = html.find_all(class_='a_title2')
                for link in links:
                    try:
                        k = str(link.attrs['href'])
                        one = getURLDATA("http://www.cnnvd.org.cn" + k)  # 获取每一个单独漏洞的详细信息页面
                        values = "'" + one[0] + "'"
                        if is_not_exist(one):
                            for i in range(1, len(one)):
                                values = values + "," + "'" + one[i] + "'"
                                sheet1.write(excel_row, i - 1 , one[i - 1])
                            excel_row = excel_row + 1
                            insertTo(values)
                           # print(values)
                           # pageNo = pageNo + 1
                            send_msg_flag = True
                        else:
                            pageNo = 1
                            flag = True
                            break
                    except Exception as e:
                        print("http://www.cnnvd.org.cn" + k)
                        break
                if flag:
                    f.save(stream)  # 保存数据到内存中
                    value = stream.getvalue() #从内存中取出数据
                    file.write(value) #将数据写入硬盘中的文件
                    file.close() #关闭文件流
                    #打开生成的xls文件
                    print('/usr/share/nginx/html/download/' + str(today_time) + '.xls')
                    filepath = os.path.abspath('/usr/share/nginx/html/download/' + str(today_time) + '.xls')
                    #解析生成的xls
                    list_work = excel_sheet_processor(filepath)
                    if list_work:
                        #生成HTML格式
                        dom = list_diction_to_html(list_work)
                        #保存到文件
                        save_dom_to_html(dom)

                    if send_msg_flag:
                        # server(str(datetime.datetime.now().date())+"的最新CNNVD信息推送：","EXCEL文件下载位置")
			            #推送微信
                        lever_test = str(danger_level_nums())
                        print(lever_test)
                        wechat_qiye(lever_test)
                        send_msg_flag = False
                    time.sleep(60 * 60 * 8) #设置定时,每八小时查看查看一次
                    pageNo = 1 #重置页数
                    flag = False
                    break #跳出内层While
                else:
                    pageNo = pageNo + 1

    except KeyboardInterrupt:
        log_update_time = str(datetime.datetime.now().ctime())
        shutdown_msg = "[x] 程序人为停止!!"
        write_log(log_update_time,msg = shutdown_msg)
        print('程序已停止')

if __name__ == "__main__":
    main()#程序入口


