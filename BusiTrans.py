#!/usr/bin/env python
#-*-coding:utf8-*-


import pandas as pd
from datetime import datetime
import math


#时间差
def TimeGap(startdate, enddate):
    d1 = datetime.strptime(startdate, "%Y-%m-%d")
    d2 = datetime.strptime(enddate, "%Y-%m-%d")
    return (d2-d1).days

def ScanFile(file, index_col=None):
    # file_data = pd.read_table('D:\\tmp\\'+file, sep = '|',index_col = 'com_buss_no')
    file_data = pd.read_table('D:\\tmp\\'+file, sep = '|',index_col = index_col )
    return file_data


def FilePro(file_data):
    com_acc_list = []
    com_acc_sorted =[]
    for com_acc in set(file_data.index):
        #print type(file_data.ix[com_acc]['tran_date'])
        index = 0
        com_contribute = 0.0
        tmp_com_contribute = 0.0
        for x in zip(file_data.ix[com_acc]['tran_date'],file_data.ix[com_acc]['bal_amt']):
             if index == 0:
                 com_contribute = x[1]*0.00012
                 tmp_com_contribute = x[1]
                 tmp_date = x[0]
             else:
                daygap = TimeGap(tmp_date, x[0])
                if daygap == 0:
                    pass
                else:
                    com_contribute += tmp_com_contribute * math.pow(1+ 0.00012, daygap) - tmp_com_contribute
                tmp_date =x[0]
                tmp_com_contribute = x[1]
                #print x[0],x[1], daygap ,com_contribute
             index += 1
        print com_acc, com_contribute
        #com_acc_list.append([com_acc,com_contribute])
        #break
    com_acc_sorted = sorted(com_acc_list, key=lambda x: x[1])
    #print com_acc_sorted
    return com_acc_sorted

def main():
    file_data = ScanFile('tmp2.txt','com_acc')
    data_list = FilePro(file_data)

    return

if __name__ == '__main__':
    main()

