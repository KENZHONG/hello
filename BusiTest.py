#!/usr/bin/env python
#-*-coding:utf8-*-
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']



def get_label( labels ):
    list_libels = list(labels)
    for i in range(len(list_libels)):
        list_libels[i]= list_libels[i].decode('utf8')
    return list_libels

def BussDataAnalysisFS():
    #FSComPlot()
    #FSComCatPlot()
    #FSBossPlot()
    #FSComCat5100()


    ComBirthAll_data = pd.read_table('D:\\tmp\\haha_ComBirth.txt', sep = '|')
    ComBirth5100_data = pd.read_table('D:\\tmp\\haha_ComBirth5100.txt', sep = '|')
    ComBirth5200_data = pd.read_table('D:\\tmp\\haha_ComBirth5200.txt', sep = '|')
    ComBirth7200_data = pd.read_table('D:\\tmp\\haha_ComBirth7200.txt', sep = '|')
    ComBirth3300_data = pd.read_table('D:\\tmp\\haha_ComBirth3300.txt', sep = '|')
    ComBirth7300_data = pd.read_table('D:\\tmp\\haha_ComBirth7300.txt', sep = '|')
    ComBirth7000_data = pd.read_table('D:\\tmp\\haha_ComBirth7000.txt', sep = '|')
    ComBirth2100_data = pd.read_table('D:\\tmp\\haha_ComBirth2100.txt', sep = '|')
    ComBirth_data = [ComBirthAll_data, ComBirth5100_data,ComBirth5200_data,ComBirth7200_data,ComBirth3300_data,ComBirth7300_data,ComBirth7000_data,ComBirth2100_data]
    FSComBirth(*ComBirth_data)
    return

def main():
    ###工商数据基本分析
    # BossSex_data = pd.read_table('D:\\tmp\\haha_BossSex.txt', sep = '|')
    #BossSexPlot(BossSex_data)
    # BossAge_data = pd.read_table('D:\\tmp\\haha_BossAge2.txt', sep = '|')
    # BossAgePlot(BossAge_data)
    # ComCat1_data = pd.read_table('D:\\tmp\\haha_ComCat4.txt', sep = '|')
    # BossCatPlot(ComCat1_data)
    # ComCat2_data = pd.read_table('D:\\tmp\\haha_ComCat5.txt', sep = '|')
    # BossCatPlot(ComCat2_data)
    # BossSexComCat_data = pd.read_table('D:\\tmp\\haha_BossSex2ComCat2.txt', sep = '|')
    # BossSexComCatPlot(BossSexComCat_data)

    #####佛山工商数据分析
    BussDataAnalysisFS()


def FSComBirth(*ComBirth_data):
    plt.title(u'佛山企业工商注册趋势')
    plt.xlabel(u'年份')
    plt.ylabel(u'企业注册数量')
    # for i in range(len(ComBirth_data)):
    #     plt.plot(ComBirth_data[i-1]['date'].values, ComBirth_data[i-1]['num'].values)
    #     #plt.plot(ComBirth_data[1]['date'].values, ComBirth_data[1]['num'].values)
    plt.plot(ComBirth_data[0]['date'].values, ComBirth_data[0]['num'].values,label = u'总企业数')
    plt.plot(ComBirth_data[1]['date'].values, ComBirth_data[1]['num'].values, label = u'批发业')
    plt.plot(ComBirth_data[2]['date'].values, ComBirth_data[2]['num'].values, label = u'零售业')
    plt.plot(ComBirth_data[3]['date'].values, ComBirth_data[3]['num'].values, label = u'商务服务业')
    plt.plot(ComBirth_data[4]['date'].values, ComBirth_data[4]['num'].values, label = u'金属制品业')
    plt.plot(ComBirth_data[5]['date'].values, ComBirth_data[5]['num'].values, label = u'研究和试验发展')
    plt.plot(ComBirth_data[6]['date'].values, ComBirth_data[6]['num'].values, label = u'房地产业')
    plt.plot(ComBirth_data[7]['date'].values, ComBirth_data[7]['num'].values, label = u'家具制造业')
    plt.legend()
    plt.show()

def FSComCat5100():
    plt.title(u'佛山批发行业分析')
    plt.xlabel(u'行业种类')
    plt.ylabel(u'企业数量')
    cat_labels = ['贸易经纪与代理','矿产品、建材及化工产品批发','机械设备、五金及电子产品批发','纺织、服装及家庭用品批发']
    cat_num = [21628,19938,12779,8278]
    plt.bar(cat_labels, cat_num)
    plt.show()

def FSBossPlot():
    Com_labels = get_label(['不属于建行客户企业主','属于建行客户企业主'])
    ###pie
    plt.figure(figsize=(6,6))
    plt.title(u'佛山企业主属于建行客户比例')
    explode=[0.1,0]
    #total 1738625
    plt.pie(['495896','1242729'],explode = explode ,labels = Com_labels, autopct = '%1.1f%%')
    plt.show()

def FSComCatPlot():
    plt.title(u'佛山企业行业排名（按企业数量）')
    plt.xlabel(u'行业种类')
    plt.ylabel(u'企业数量')
    com_ccb_num = [30332,8768,8912,7226,3700,5051,2343]
    com_num = [75941,35312,29612,19081,10729,10379,9091]
    com_not_ccb_num = [com_num[0] - com_ccb_num[0],com_num[1] - com_ccb_num[1],com_num[2] - com_ccb_num[2],com_num[3] - com_ccb_num[3],com_num[4] - com_ccb_num[4],com_num[5] - com_ccb_num[5],com_num[6] - com_ccb_num[6],]
    com_cat = ['批发业','零售业','商务服务业','金属制品业','研究和试验发展','房地产业','家具制造业']

    p2 = plt.bar(com_cat,com_not_ccb_num, bottom = com_ccb_num, color = 'r')
    p1 = plt.bar(com_cat,com_ccb_num)
    plt.legend((p1[0], p2[0]),(u'在建行开户企业',u'没在建行开户企业'))
    plt.show()
    return

def FSComPlot():
    Com_labels = get_label(['没在建行开户企业','在建行开户企业'])
    ###pie
    plt.figure(figsize=(6,6))
    plt.title(u'佛山企业属于建行客户比例')
    explode=[0.1,0]
    plt.pie(['202688','112909'],explode = explode ,labels = Com_labels, autopct = '%1.1f%%')
    plt.show()


def BossSexComCatPlot(BossSexComCat_data):
    plt.title(u'女性企业主所属行业种类排行')
    plt.xlabel(u'行业种类')
    plt.ylabel(u'企业数量')
    plt.bar(BossSexComCat_data['cat'].values,BossSexComCat_data['num'].values)
    plt.show()


def BossCatPlot(ComCatt_data):
     plt.title(u'企业所属行业种类排名（按企业数量）')
     # plt.title(u'企业所属行业种类排名（按企业注册资金额）')
     plt.tick_params(axis = 'x', labelsize = '7')
     plt.xlabel(u'行业种类')
     # plt.ylabel(u'平均注册资金（单位：万元）')
     plt.ylabel(u'企业数量')
     plt.bar(ComCatt_data['cat'].values,ComCatt_data['num'].values)
     #plt.bar(ComCatt_data['cat'].values,ComCatt_data['mon'].values)
     plt.show()

def BossAgePlot(BossAge_data):
    plt.title(u'企业主年龄分布')
    plt.xlabel(u'企业主年龄层')
    plt.ylabel(u'企业主数量')
    plt.bar(BossAge_data['age'].values,BossAge_data['num'].values)
    plt.show()

def BossSexPlot(BossSex_data):
    #
    print  list(BossSex_data['sex'].values)
    print BossSex_data['num'].values
    BossSex_labels = get_label(BossSex_data['sex'].values)
    ###pie


    plt.figure(figsize=(6,6))
    plt.title(u'企业主性别分布')
    explode=[0.1,0]
    plt.pie(BossSex_data['num'].values,explode = explode ,labels = BossSex_labels, autopct = '%1.1f%%')
    #plt.bar(BossSex_data['sex'].values,BossSex_data['num'].values)
    plt.show()



if __name__ == '__main__':
    main()

