# -*- coding: utf-8 -*-
from ucc_model import  *
from pyomo.opt import SolverFactory
from pyomo.environ import *
import sys, os
SELF_DIR = os.path.dirname(__file__)
OUTPUT_DIR = SELF_DIR + '/output/' # xlsx輸出位置 
if not os.path.exists(OUTPUT_DIR): # 要創資料夾 不然會error
	os.makedirs(OUTPUT_DIR)
import pandas as pd
from pyomo.core import Var, Constraint
# D:\Admin\Desktop\pyomo> python ucc_run.py > uct.txt

#----------------------------#
import time
tStart = time.time()#計時開始
#----------------------------#
print '# ----------------------------------------------------------'
print 'Input parameter to model......'
print '# ----------------------------------------------------------'
data = DataPortal(model=model)
instance = model.create_instance(data)
# instance.dual = Suffix(direction=Suffix.IMPORT)
#instance.pprint('T')
print '# ----------------------------------------------------------'
print 'Connect to GUROBI......'
print '# ----------------------------------------------------------'
# instance..pprint()
opt = SolverFactory("gurobi")
opt.options['nodemethod'] = 1  # (0=primal simplex, 1=dual simplex, 2=barrier)
opt.options['MIPGap'] = 0.005 #maximum MIP solutions to find
# cplex
# opt = SolverFactory("cplex", executable="C:/Program Files/IBM/ILOG/CPLEX_Studio126/cplex/bin/x64_win64/cplex.exe")
'''
#----------------------------#
#gurobi
opt.options['SolutionLimit'] = 2 #maximum MIP solutions to find
opt.options['timelimit'] = 600#限制時間100分鐘
opt.options['nodemethod'] = 2  #  使用內點法解題
opt.options['mipfocus'] = 3  #  優先優化可行解
opt.options['VarBranch'] = 2
opt.options['CutPasses'] = 2  #  #Number of passes permitted when generating MIP cutting plane
#----------------------------#
'''
print '# ----------------------------------------------------------'
print 'Start calculating......'
print '# ----------------------------------------------------------'
'''
#----------------------------#
orig_stdout = sys.stdout # open
sys.stdout=open("ucc_out.txt","w")
#----------------------------#
'''
results = opt.solve(instance, tee=True)
results.write()
'''
#----------------------------#
sys.stdout.close() # close
sys.stdout=orig_stdout
#----------------------------#
'''
print '# ----------------------------------------------------------'
print 'Output data file......'
print '# ----------------------------------------------------------'
# 將所有輸出合成一個dict-----------------------------------#
OBJ_value=instance.OBJ() # 目標函數值
with open(OUTPUT_DIR + "min_cost.csv", "w") as text_file:
	text_file.write("min_cost,{0}".format(OBJ_value))
dic2={}
for v in instance.component_objects(Var, active=True):
	varobject = getattr(instance, str(v))
	dic={}
	for index in varobject:
		dic.update({index:varobject[index].value if varobject[index].value>0.0000001 else 0}) # 把那種太小的值去掉 有時候會有那種2.345E-14這種奇怪的值
	dic2.update({v.name:dic})
# 輸出 xlsx檔案---------------------------------------------------------------------------------------#
for i in dic2.keys():
	type_save=[ {} for loop in range(7)] # 有6個type 將key中間的6個狀態分離整理 用7個list比較直觀
	if len(dic2[i].keys()[0])==2:  # 處理 name + time 的資料
		temp = dic2[i]
		data = map(list, zip(*temp.keys())) + [temp.values()]
		df = pd.DataFrame(zip(*data)).set_index([0, 1])[2].unstack()
		df.fillna(0, inplace=True) # missing data convert to zero
		df.to_excel(OUTPUT_DIR + i + '.xlsx')
	elif len(dic2[i].keys()[0])==3:  # 處理 name + type + time 的資料
		temp = dic2[i]
		for j in temp.keys():
			type_save[j[1]].update({(j[0],j[2]):temp[j]}) # 將6個狀態分成6個部分 從3維變成2維較好處理
		for k in range(7):
			if type_save[k]:  # 將6個狀態的資料輸出 有存東西再輸出
				temp = type_save[k]
				data = map(list, zip(*temp.keys())) + [temp.values()]
				df = pd.DataFrame(zip(*data)).set_index([0, 1])[2].unstack()
				df.fillna(0, inplace=True) # missing data convert to zero
				df.to_excel(OUTPUT_DIR + i + '_type_' + str(k) + '.xlsx') # 輸出 檔名_type_k.xlsx
# 輸出 cp.xlsx檔案-----------------------------------------------------------------------------------#
df1 = pd.DataFrame()
for i in xrange(7):
    if os.path.exists(OUTPUT_DIR + 'cp_type_'+ str(i) +'.xlsx'):
        df = pd.read_excel(OUTPUT_DIR + 'cp_type_'+ str(i) +'.xlsx')
        df1 = df1.add(df, fill_value=0)         # 將每個type的發電量加起來 就是總發電量
df1.to_excel(OUTPUT_DIR + 'cp(123).xlsx')

# 輸出 cu.xlsx檔案-----------------------------------------------------------------------------------#
df_cu =pd.DataFrame()
for i in xrange(7):
    if os.path.exists(OUTPUT_DIR + 'cu_type_'+ str(i) +'.xlsx'):
        df = pd.read_excel(OUTPUT_DIR + 'cu_type_'+ str(i) +'.xlsx')
        for j in df.columns:
            for k in df.index:              # 將啟動狀態1 換成對應的type
                if df[j][k] == 1:
                    df[j][k] = i
        df_cu = df_cu.add(df, fill_value=0)
df_cu.drop(0, axis=1, inplace=True) # 時間軸有0~24 0是初始值cu0 砍掉
df_cu.to_excel(OUTPUT_DIR + 'cu.xlsx')

# 輸出 dEOH.xlsx檔案---------------------------------------------------------------------------------#
df_EOH = pd.DataFrame()
for i in xrange(7):
    if os.path.exists(OUTPUT_DIR + 'dEOH_type_'+ str(i) +'.xlsx'):
        df = pd.read_excel(OUTPUT_DIR + 'dEOH_type_'+ str(i) +'.xlsx')
        df_EOH = df_EOH.add(df, fill_value=0)
df_EOH.to_excel(OUTPUT_DIR + 'EOH.xlsx')

# 輸出 remainEOH.xlsx檔案----------------------------------------------------------------------------#
df_rEOH = pd.DataFrame()
for i in xrange(7):
    if os.path.exists(OUTPUT_DIR + 'remainEOH_type_'+ str(i) +'.xlsx'):
        df = pd.read_excel(OUTPUT_DIR + 'remainEOH_type_'+ str(i) +'.xlsx')
        df_rEOH = df_rEOH.add(df, fill_value=0)
df_rEOH.to_excel(OUTPUT_DIR + 'remainEOH.xlsx')
# ---------------------------------------------------------------------------------------------------#

#----------------------------#
tEnd = time.time()#計時結束
print '# ----------------------------------------------------------'
print 'Total Time cost:',tEnd - tStart,'sec'
print '# ----------------------------------------------------------'
#----------------------------#


'''
# 舊版輸出方法
#----------------------------#
orig_stdout = sys.stdout # open
sys.stdout=open("ucc_out.txt","w")
#----------------------------#
# Accessing Variable Values
#instance.solutions.load_from(results)
for v in instance.component_objects(Var, active=True):
	print "# ----------------------------------------------------------"
	print ("Variable",v.name)
	print "# ----------------------------------------------------------"
	varobject = getattr(instance, str(v))
	for index in varobject:
		print index,varobject[index].value
#----------------------------#
sys.stdout.close() # close
sys.stdout=orig_stdout
#----------------------------#
'''
