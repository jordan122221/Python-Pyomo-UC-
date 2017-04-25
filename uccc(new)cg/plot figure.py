# -*- coding: utf-8 -*-
from ucc_init import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Ellipse, Polygon
xlsx_path = 'output'

def get_data(files):
    data = pd.read_excel(xlsx_path +'/'+files)
    return data
'''
#負載
fig = plt.figure()
ax1 = fig.add_subplot(111)
for i in demand_init().keys():
   ax1.bar(i,demand_init()[i], color='red', edgecolor='black', hatch="/")
#plt.show()
plt.title('LOAD Demend')
plt.xlabel("Time (hours)")
plt.ylabel("MW")
plt.savefig("LOAD Demend.png",dpi=600,format="png")
'''
#機組類型(th ,cg)淨出力
#p_data(select_col)
data1 = get_data('cp_type_4.xlsx')
data2 = get_data('cp_type_5.xlsx')
data3 = get_data('cp_type_6.xlsx')
data = get_data('p.xlsx')
def p_cp_draw():
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    pOUTPUT =[]
    cpOUTPUT =[]
    for i in range(len(data.values[0][:])):
        a = sum(data[i+1].tolist())
        b = sum(data1[i+1].tolist())+sum(data2[i+1].tolist())+sum(data3[i+1].tolist())
        pOUTPUT.append(a)
        cpOUTPUT.append(b)
        ax1.bar(i,pOUTPUT[i], color='red', edgecolor='black', hatch="/")
        ax1.bar(i,cpOUTPUT[i], color='blue', edgecolor='black', hatch="//")
    ax1.legend(['p generation','cp generation']) 
    plt.title('Output Power Rate')
    plt.xlabel("Time (hours)")
    plt.ylabel("MW")
    plt.savefig("Output Power Rate.png",dpi=600,format="png")
    return 0





