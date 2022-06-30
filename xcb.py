#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author:qiu_lzsnmb
@file:xcb.py
@time:2022/06/29
"""

import time

import requests
import json
import os
from lxml import etree

headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)",
}


class XCB:
    def __init__(self, hosts, title, courseid, companyid=0):
        """
        :param hosts:  ip+端口
        :param title: 标题
        :param courseid: 课程号
        :param companyid: 公司号
        """
        self.hosts = hosts
        self.title = title
        self.courseid = courseid
        self.companyid = companyid
        self.companyidList = {}

    def buyFactory(self, companyid, cf, _type=1):
        """
        购买厂房
        :param companyid: 公司代码
        :param cf: 厂房类型,1大2中3小
        :param _type: 租用还是购买
        :return:
        """
        pass

    def getCompanyCode(self):
        """
        获取公司代码
        :return:
        """
        url = f"http://{self.hosts}/BSTCS/student/CEO/B/CEO_B_0.jsp?courseid={self.courseid}&companyid={self.companyid}"
        print("排名", url)
        req = requests.get(url)
        req_html = etree.HTML(req.text)
        rText = req_html.xpath("//*[@id='select_company']/option/text()")
        rID = req_html.xpath("//*[@id='select_company']/option/@value")
        p = {}
        for i, j in zip(rText, rID):
            p[j] = i
        return p

    def getHistoricalDecisions(self, t, companyid):
        """
        获取历史决策
        :param 季度:
        :return:
        """
        url = f"http://{self.hosts}/BSTCS/student/CEO/C/CEO_C_5.jsp"
        data = {
            "companyid": companyid,
            "courseid": self.courseid,
            "sectionid": -1,
            "studentid": "yes",
            "databasename": "null",
            "time": t,
            "section": -1
        }
        req = requests.post(url, data=data, headers=headers)
        return req

    def getProductDesign(self, companyid):
        """
        获取产品设计
        :return:
        """
        deploy = {
            "高亮LED屏幕": 1,
            "TFT全彩触摸屏": 2,
            "OLED显示屏": 3,
            "塑胶": 1,
            "金属": 2,
            "皮革": 3,
            "7天以下": 1,
            "15天": 2,
            "30天": 3,
            "30天以上": 4,
            "有氧锻炼": 1,
            "心率测试": 2,
            "GPS定位": 3,
            "支付功能": 4,
            "公司白领": "白领",
            "青少年群体": "青年",
            "老年群体": "老年",
            "玻璃包装纸": "1",
            "纸质包装盒": "2",
            "金属包装盒": "3",
            "短平绒": "1",
            "松针绒": "2",
            "玫瑰绒": "3",
            "PP棉": "1",
            "珍珠棉": "2",
            "棉花": "3",
            "发声装置": "1",
            "发光装置": "2",
            "品质型客户": "品质",
            "经济型客户": "经济",
            "实惠型客户": "实惠",
            "ABS塑料": "1",
            "合金外壳": "2",
            "主板带2G内存": "1",
            "主板带4G内存": "2",
            "主板带8G内存": "3",
            "4寸": "1",
            "5寸": "2",
            "6寸": "3",
            "蓝牙无线功能": "1",
            "wifi无线上网": "2",
            "3G无线上网": "3",
            "在校学生": "学生",
            "大众人群": "大众",
            "商务人士": "商务",
        }
        url = f"http://{self.hosts}/BSTCS/student/CTO/A/CTO_A_1.jsp?courseid={self.courseid}&companyid={companyid}&title=%E4%BA%A7%E5%93%81%E8%AE%BE%E8%AE%A1"
        req = requests.get(url)
        req_html = etree.HTML(req.text)
        rText = req_html.xpath('//*/tr[@class="tablebodytext"]/td[@width="40%"]/a/text()')
        rID = req_html.xpath('//*/tr[@class="tablebodytext"]/td[@width="40%"]/a/@id')
        p = {}
        for i in rText:
            if i == "\r\n\t\t\t\t\t":
                rText.remove(i)
        for i, j in zip(rText, rID):
            p[j.replace('name_', '')] = i.strip()
        R = {}
        for i in p:
            url2 = f'http://{self.hosts}/BSTCS/show.do?page=7&databasename=null&companyid={companyid}&courseid={self.courseid}&month=1&id={i}'
            req2 = requests.get(url2)
            req2_html = etree.HTML(req2.text)
            rText2 = req2_html.xpath('//*/tr[@class="tablebodytext"]/td/li/text()')
            rZdqt = req2_html.xpath('//*/tr[@class="tablebodytext"]/td[2]/text()')
            s = deploy[rZdqt[3].replace('\xa0\xa0', '')]
            for j in rText2:
                s += str(deploy[j])
            R[p[i]] = s

        return R

    def getCashFlow(self, companyid):
        """
        获取现金流
        :return:
        """
        url = f"http://{self.hosts}/BSTCS/student/CFO/B/CFO_B_1.jsp?courseid={self.courseid}&databasename=bsterbstpcs&companyid={companyid}"
        req = requests.get(url)
        req_html = etree.HTML(req.text)
        rXj = req_html.xpath('//*/span[@class="number_end"]/text()')[0]
        return rXj

    def changeCompanyInformation(self, 公司, name):
        """
        更改公司名
        :param 公司:
        :param name:
        :return:
        """
        pass  # 危险(容易失败，容易编码错误)

    def buyRawMaterials(self, 公司):
        """
        购买原材料
        :param 公司:
        :return:
        """
        pass

    def singlePage(self, companyid):
        单接口 = {
            "报价表": f"http://{self.hosts}/BSTCS/student/CSO/A/CSO_A_2.jsp?courseid={self.courseid}&companyid={companyid}",
            "广告表": f"http://{self.hosts}/BSTCS/student/CMO/A/CMO_A_2.jsp?courseid={self.courseid}&companyid={companyid}",
            "原料表": f"http://{self.hosts}/BSTCS/student/CPO/A/CPO_A_1.jsp?courseid={self.courseid}&companyid={companyid}",
            "成品表": f"http://{self.hosts}/BSTCS/student/CEO/C/CEO_C_8.jsp?courseid={self.courseid}&companyid={companyid}&taskid=0",
            "工人表": f"http://{self.hosts}/BSTCS/student/CPO/A/CPO_A_5.jsp?courseid={self.courseid}&companyid={companyid}&studentid=1384&title="
        }

    def 强加(self, teacherid, classname):
        # url = f"http://{self.hosts}/BSTSTART/student_setLoginInfo.action"
        # data = {
        #     "teacherid": 2,
        #     "courseid": 32
        # }
        # req = requests.post(url,data=data)
        pass


if __name__ == '__main__':
    xcb = XCB(hosts="221.12.107.218:8088", title="6-29晚场手环", courseid=286, companyid=1424)
    h = xcb.getHistoricalDecisions(1, 1424)
    print(h.text)
