# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
# ucc_init.py 是用來將.xlsx檔案中的資料回傳給model使用的
xlsx_path = 'data_file'
# If you want to select multiple columns, use this function.
# read CGDAT.xlsx to pd.dataframe and then select multiple columns
def CGDAT_data(select_col):
    data = pd.read_excel(xlsx_path + '/CGDAT.xlsx')
    data = data[select_col]
    return data
# read GDAT.xlsx to pd.dataframe and then select multiple columns
def GDAT_data(select_col):
    data = pd.read_excel(xlsx_path + '/GDAT.xlsx')
    data = data[select_col]
    return data
def CGDAT_data2(select_col):
    data = pd.read_excel(xlsx_path + '/new cg data.xlsx')
    data = data[select_col]
    return data

# ---------------------------------------------------------
# read T.xlsx
def T_init():
    data = pd.read_excel(xlsx_path + '/T.xlsx')
    data = data['T'].tolist()
    return data[0]

# read GDAT.xlsx and select column 'UNIT_NAME'
def UNIT_NAMES_init():
    data = pd.read_excel(xlsx_path + '/GDAT.xlsx')
    data = data['UNIT_NAME'].tolist()
    return data

# read CG_NAME.xlsx
def CG_NAMES_init():
    data = pd.read_excel(xlsx_path + '/CG_NAME.xlsx')
    data = data['CG_NAME'].tolist()
    return data

# UNITxTYPE select columns 'Unit_EName' and 'Operat_con' from CGDAT.xlsx and return list [('Unit_EName', 'Operat_con')]
def UNITxTYPE_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con'])
    data = data.values.tolist()
    data = [tuple([x[0],int(x[1])]) for x in data]
    return data

# 狀態轉換
def trans_init(model):
    new=[]
    new2=[]
    # 所有狀態
    data = model.UNITxTYPE*model.TYPE
    # 挑出正確的j到k的狀態
    for (i,j,k) in data:
        if j == 1:
            if k == 4:
                new.append((i,j,k))
        elif j == 4:
            if k == 1 or k == 5 or k == 6:
                new.append((i,j,k))
        elif j == 5:
            if k == 4 or k == 6:
                new.append((i,j,k))
        elif j == 6:
            if k == 4 or k == 5:
                new.append((i,j,k))
    # 刪掉不合適的狀態 如在只有1 4 5的狀態下 4雖然可以到1 5 6 因為沒有6 所以要把4到6的狀態刪除
    for (i,j,k) in new:
        for (m,n) in model.UNITxTYPE:
            if i == m and k == n:
                new2.append((i,j,k))
    return new2

# read GDAT.xlsx and return dictionary [Key : Value] = ['UNIT_NAME' : 'fuel_a']
def a_init():
    data = GDAT_data(['UNIT_NAME', 'fuel_a'])
    data = data.set_index('UNIT_NAME')['fuel_a'].to_dict()
    return data

# read GDAT.xlsx and return dictionary [Key : Value] = ['UNIT_NAME' : 'fuel_b']
def b_init():
    data = GDAT_data(['UNIT_NAME', 'fuel_b'])
    data = data.set_index('UNIT_NAME')['fuel_b'].to_dict()
    return data

# read GDAT.xlsx and return dictionary [Key : Value] = ['UNIT_NAME' : 'fuel_c']
def c_init():
    data = GDAT_data(['UNIT_NAME', 'fuel_c'])
    data = data.set_index('UNIT_NAME')['fuel_c'].to_dict()
    return data

# read GDAT.xlsx and return dictionary [Key : Value] = ['UNIT_NAME' : 'fuel_d']
def d_init():
    data = GDAT_data(['UNIT_NAME', 'fuel_d'])
    data = data.set_index('UNIT_NAME')['fuel_d'].to_dict()
    return data

# read CF_th.xlsx and return dictionary [Key : Value] = [('cf_time', 'unit') : 'cv']
def CV_th_init():
    data = pd.read_excel(xlsx_path + '/CF_th.xlsx')
    data = data[['cf_time', 'unit','cv']]
    data['cf_time'] += 1
    data = data.set_index(['cf_time', 'unit'])['cv'].to_dict()
    return data

# read CF_th.xlsx and return dictionary [Key : Value] = [('cf_time', 'unit') : 'up']
def UP_th_init():
    data = pd.read_excel(xlsx_path + '/CF_th.xlsx')
    data = data[['cf_time', 'unit','up']]
    data['cf_time'] += 1
    data = data.set_index(['cf_time', 'unit'])['up'].to_dict()
    return data
'''
# read CGDAT.xlsx and return dictionary [Key : Value] = [('Unit_EName', 'Operat_con') : 'Fuel_a']
def ca_init():
    data = CGDAT_data(['Unit_EName', 'Operat_con', 'Fuel_a'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Fuel_a'].to_dict()
    return data

# read CGDAT.xlsx and return dictionary [Key : Value] = [('Unit_EName', 'Operat_con') : 'Fuel_b']
def cb_init():
    data = CGDAT_data(['Unit_EName', 'Operat_con', 'Fuel_b'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Fuel_b'].to_dict()
    return data

# read CGDAT.xlsx and return dictionary [Key : Value] = [('Unit_EName', 'Operat_con') : 'Fuel_c']
def cc_init():
    data = CGDAT_data(['Unit_EName', 'Operat_con', 'Fuel_c'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Fuel_c'].to_dict()
    return data

# read CGDAT.xlsx and return dictionary [Key : Value] = [('Unit_EName', 'Operat_con') : 'Fuel_d']
def cd_init():
    data = CGDAT_data(['Unit_EName', 'Operat_con', 'Fuel_d'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Fuel_d'].to_dict()
    return data

def CV_cg_init():
    data = pd.read_excel(xlsx_path + '/CF_cg.xlsx')
    data = data[['cf_time', 'unit','cv']]
    data['cf_time'] += 1
    data = data.set_index(['cf_time', 'unit'])['cv'].to_dict()
    return data

def UP_cg_init():
    data = pd.read_excel(xlsx_path + '/CF_cg.xlsx')
    data = data[['cf_time', 'unit','up']]
    data['cf_time'] += 1
    data = data.set_index(['cf_time', 'unit'])['up'].to_dict()
    return data
'''
# read CGDAT.xlsx and return dictionary [Key : Value] = [('Unit_EName', 'Operat_con') : 'MAX']

def cRU_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Ramp_Up'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Ramp_Up'].to_dict()
    return data

def cRD_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Ramp_Down'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Ramp_Down'].to_dict()
    return data

def cUT_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Min_utime'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Min_utime'].to_dict()
    return data

def cDT_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Min_dtime'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['Min_dtime'].to_dict()
    return data

# 如果最大值是4.5 回傳5 最大值是4.001 回傳4 分界是0.001
def cmtl_init():
    data = CGDAT_data2('Min_utime')
    data = data.max()
    if data - data//1 > 0.001:
        return data//1 + 1
    else:
        return data//1

# 如果最大值是4.5 回傳5 最大值是4.001 回傳4 分界是0.001
def cmct_init():
    data = CGDAT_data2('Min_dtime')
    data = data.max()
    if data - data//1 > 0.001:
        return data//1 + 1
    else:
        return data//1

def ctoff0_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'toff0'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['toff0'].to_dict()
    return data

def cton0_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'ton0'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['ton0'].to_dict()
    return data

# if cton0[i,j] > 0 then cu0[i,j] = 1 else cu0[i,j] = 0;
def cu0_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'ton0'])
    data['ton0']=[1 if i > 0 else 0 for i in data['ton0']]
    data = data.set_index(['Unit_EName', 'Operat_con'])['ton0'].to_dict()
    return data

def cSc_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cSc'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cSc'].to_dict()
    return data
# 使用者選擇
def cuMrun_init():
    CG_NAME_data = pd.read_excel(xlsx_path + '/CG_NAME.xlsx')
    CG_NAME_data = CG_NAME_data['CG_NAME'].tolist() # name
    t = pd.read_excel(xlsx_path + '/T.xlsx')
    t = t['T'].tolist()
    t = range(1, t[0] + 1)    # t =  1...24
    keys = [(a,b) for a in CG_NAME_data for b in t]
    values = np.zeros(len(keys),dtype=int)
    data = dict(zip(keys,values))
    return data
# 使用者選擇
def cuMoff_init():
    UNITxTYPE = CGDAT_data2(['Unit_EName', 'Operat_con'])
    UNITxTYPE = UNITxTYPE.values.tolist()
    t = pd.read_excel(xlsx_path + '/T.xlsx')
    t = t['T'].tolist()
    t = range(1, t[0] + 1)
    keys = [(a,b,c) for (a,b) in UNITxTYPE for c in t]
    values = np.zeros(len(keys),dtype=int)
    data = dict(zip(keys,values))
    return data

def pMAX_init():
    data = GDAT_data(['UNIT_NAME', 'max_gen'])
    data = data.set_index('UNIT_NAME')['max_gen'].to_dict()
    return data

def pMIN_init():
    data = GDAT_data(['UNIT_NAME', 'min_gen'])
    data = data.set_index('UNIT_NAME')['min_gen'].to_dict()
    return data

def Sc_init():
    data = GDAT_data(['UNIT_NAME', 'start_cost'])
    data = data.set_index('UNIT_NAME')['start_cost'].to_dict()
    return data

def Sdc_init():
    data = GDAT_data(['UNIT_NAME', 'shut_down_cost'])
    data = data.set_index('UNIT_NAME')['shut_down_cost'].to_dict()
    return data

def RU_init():
    data = GDAT_data(['UNIT_NAME', 'ramp_up_limit'])
    data = data.set_index('UNIT_NAME')['ramp_up_limit'].to_dict()
    return data

def RD_init():
    data = GDAT_data(['UNIT_NAME', 'ramp_down_limit'])
    data = data.set_index('UNIT_NAME')['ramp_down_limit'].to_dict()
    return data

def UT_init():
    data = GDAT_data(['UNIT_NAME', 'min_up_time'])
    data = data.set_index('UNIT_NAME')['min_up_time'].to_dict()
    return data

def DT_init():
    data = GDAT_data(['UNIT_NAME', 'min_down_time'])
    data = data.set_index('UNIT_NAME')['min_down_time'].to_dict()
    return data
# 使用者選擇
def uMoff_init():
    UNIT_NAME_data = GDAT_data('UNIT_NAME')
    UNIT_NAME_data = UNIT_NAME_data.tolist() # name
    t = pd.read_excel(xlsx_path + '/T.xlsx')
    t = t['T'].tolist()
    t = range(1, t[0] + 1)
    keys = [(a,b) for a in UNIT_NAME_data for b in t]
    values = np.zeros(len(keys),dtype=int)
    data = dict(zip(keys,values))
    return data
# 使用者選擇
def uMrun_init():
    UNIT_NAME_data = GDAT_data('UNIT_NAME')
    UNIT_NAME_data = UNIT_NAME_data.tolist() # name
    t = pd.read_excel(xlsx_path + '/T.xlsx')
    t = t['T'].tolist()
    t = range(1, t[0] + 1)
    keys = [(a,b) for a in UNIT_NAME_data for b in t]
    values = np.zeros(len(keys),dtype=int)
    data = dict(zip(keys,values))
    return data

# 如果min_up_time最大值是4.5 回傳5 最大值是4.001 回傳4 分界是0.001
def mtl_init():
    data = GDAT_data('min_up_time')
    data = data.max()
    if data - data//1 > 0.001:
        return data//1 + 1
    else:
        return data//1
# 如果min_down_time最大值是4.5 回傳5 最大值是4.001 回傳4 分界是0.001
def mct_init():
    data = GDAT_data('min_down_time')
    data = data.max()
    if data - data//1 > 0.001:
        return data//1 + 1
    else:
        return data//1

def toff0_init():
    data = GDAT_data(['UNIT_NAME', 'toff'])
    data = data.set_index('UNIT_NAME')['toff'].to_dict()
    return data

def ton0_init():
    data = GDAT_data(['UNIT_NAME', 'ton'])
    data = data.set_index('UNIT_NAME')['ton'].to_dict()
    return data

# if ton0[i] > 0 then u0[i] = 1 else u0[i] = 0;
def u0_init():
    data = GDAT_data(['UNIT_NAME', 'ton'])
    data['ton']=[1 if i > 0 else 0 for i in data['ton']]
    data = data.set_index('UNIT_NAME')['ton'].to_dict()
    return data

def demand_init():
    data = pd.read_excel(xlsx_path + '/LF_EXCEL.xlsx')
    data['HOUR'] += 1
    data = data.set_index('HOUR')['POWER'].to_dict()
    return data

def sR_init(UNIT_TYPE):
    UNIT_TYPE.construct()
    UNIT_TYPE_data = list(UNIT_TYPE.value)
    data = pd.read_excel(xlsx_path + '/SR.xlsx')
    data['sr_time'] += 1
    data = data[data['unit_type'].isin(UNIT_TYPE_data)]
    data = data.set_index(['sr_time', 'unit_type'])['sr'].to_dict()
    return data
# 如果 (UT_data[i] - ton0_data[i]) 是4.5 回傳5 最大值是4.01 回傳4 分界是0.01
def state_logic1_time_data(ST):
    UT_data = GDAT_data(['UNIT_NAME','min_up_time'])
    UT_data = UT_data.set_index('UNIT_NAME')['min_up_time'].to_dict()
    ton0_data = GDAT_data(['UNIT_NAME','ton'])
    ton0_data = ton0_data.set_index('UNIT_NAME')['ton'].to_dict()
    ST.construct()
    ST_data = ST.value
    data = {key: (UT_data[key] - ton0_data.get(key, 0)) for key in UT_data.keys()}
    data = {key: int(ST_data -1 + data[key]//1 + 1) if data[key] - data[key]//1 > 0.01 else int(ST_data - 1 + data[key]//1) for key in data.keys()}
    return data
# 如果 (DT_data[i] - toff0_data[i]) 是4.5 回傳5 最大值是4.01 回傳4 分界是0.01
def state_logic2_time_data(ST):
    DT_data = GDAT_data(['UNIT_NAME','min_down_time'])
    DT_data = DT_data.set_index('UNIT_NAME')['min_down_time'].to_dict()
    toff0_data = GDAT_data(['UNIT_NAME','toff'])
    toff0_data = toff0_data.set_index('UNIT_NAME')['toff'].to_dict()
    ST.construct()
    ST_data = ST.value
    data = {key: (DT_data[key] - toff0_data.get(key, 0)) for key in DT_data.keys()}
    data = {key: int(ST_data -1 + data[key]//1 + 1) if data[key] - data[key]//1 > 0.01 else int(ST_data - 1 + data[key]//1) for key in data.keys()}
    return data
# 如果 (cUT[i,j]-cton0[i,j]) 是4.5 回傳5 最大值是4.01 回傳4 分界是0.01
def state_logic_cg1_time_data(ST):
    cUT_data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Min_utime'])
    cUT_data = cUT_data.set_index(['Unit_EName', 'Operat_con'])['Min_utime'].to_dict()
    cton0_data = CGDAT_data2(['Unit_EName', 'Operat_con', 'ton0'])
    cton0_data = cton0_data.set_index(['Unit_EName', 'Operat_con'])['ton0'].to_dict()
    ST.construct()
    ST_data = ST.value
    data = {key: (cUT_data[key] - cton0_data.get(key,0)) for key in cUT_data.keys()}
    data = {key: int(ST_data -1 + data[key]//1 + 1) if data[key] - data[key]//1 > 0.01 else int(ST_data - 1 + data[key]//1) for key in data.keys()}
    return data

def state_logic_cg2_time_data(ST):
    cDT_data = CGDAT_data2(['Unit_EName', 'Operat_con', 'Min_dtime'])
    cDT_data = cDT_data.set_index(['Unit_EName', 'Operat_con'])['Min_dtime'].to_dict()
    ctoff0_data = CGDAT_data2(['Unit_EName', 'Operat_con', 'toff0'])
    ctoff0_data = ctoff0_data.set_index(['Unit_EName', 'Operat_con'])['toff0'].to_dict()
    ST.construct()
    ST_data = ST.value
    data = {key: (cDT_data[key] - ctoff0_data.get(key,0)) for key in cDT_data.keys()}
    data = {key: int(ST_data -1 + data[key]//1 + 1) if data[key] - data[key]//1 > 0.01 else int(ST_data - 1 + data[key]//1) for key in data.keys()}
    return data

#----------新增加的參數
#CG CG MILP 分段點
def cpMIN_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'MIN'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['MIN'].to_dict()
    return data

def cpSTEP2_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP2'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP2'].to_dict()
    return data

def cpSTEP3_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP3'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP3'].to_dict()
    return data

def cpSTEP4_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP4'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP4'].to_dict()
    return data

def cpSTEP5_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP5'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP5'].to_dict()
    return data

def cpSTEP6_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP6'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP6'].to_dict()
    return data

def cpSTEP7_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cpSTEP7'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cpSTEP7'].to_dict()
    return data

def cpMAX_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'MAX'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['MAX'].to_dict()
    return data


# CG MILP 熱號率
def fcpMIN_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpMIN'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpMIN'].to_dict()
    return data

def fcpSTEP2_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP2'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP2'].to_dict()
    return data

def fcpSTEP3_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP3'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP3'].to_dict()
    return data

def fcpSTEP4_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP4'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP4'].to_dict()
    return data

def fcpSTEP5_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP5'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP5'].to_dict()
    return data

def fcpSTEP6_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP6'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP6'].to_dict()
    return data

def fcpSTEP7_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSTEP7'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSTEP7'].to_dict()
    return data
#CG MILP 斜率
def fcpSeg1_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg1'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg1'].to_dict()
    return data

def fcpSeg2_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg2'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg2'].to_dict()
    return data

def fcpSeg3_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg3'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg3'].to_dict()
    return data

def fcpSeg4_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg4'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg4'].to_dict()
    return data

def fcpSeg5_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg5'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg5'].to_dict()
    return data

def fcpSeg6_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'fcpSeg6'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['fcpSeg6'].to_dict()
    return data

def cE_init():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'cE'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['cE'].to_dict()
    return data

def availabledailyEOH():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'availabledailyEOH'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['availabledailyEOH'].to_dict()
    return data

def thismondayEOH():
    data = CGDAT_data2(['Unit_EName', 'Operat_con', 'thismondayEOH'])
    data = data.set_index(['Unit_EName', 'Operat_con'])['thismondayEOH'].to_dict()
    return data    

'''
def CG_NAMES_init2():
    data = pd.read_excel(xlsx_path + '/CG_NAME.xlsx')
    data = data['CG_NAME'].tolist()
    return data
def UNITxTYPE_init2():
    data = CGDAT_data(['Unit_EName', 'Operat_con'])
    data = data.values.tolist()
    data = [tuple([x[0],int(x[1])]) for x in data]
    return data
'''