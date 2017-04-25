# -*- coding: utf-8 -*-
from __future__ import division
from pyomo.environ import *
# import XXX_init function to this model
from ucc_init import  *

model = AbstractModel()
# number of time steps for the period stuied
model.T = Param(initialize=T_init(), within=PositiveIntegers) # T_init function
# model.t = RangeSet(1, model.T) # t = 1...T

model.ST = Param(initialize=1, within=PositiveIntegers)
model.ET = Param(initialize=model.T, within=PositiveIntegers)
model.UNIT_NAMES = Set(initialize=UNIT_NAMES_init()) # UNIT_NAMES_init function
model.UNIT_TYPE = Set(initialize=['th','cg'])

model.CG_NAMES = Set(initialize=CG_NAMES_init()) # CG_NAMES_init function
'''
model.CGHr_1GT = Set()
model.CGHr_2GT = Set()
model.CGHr_3GT = Set()
model.CGHr_ST1GT = Set()
model.CGHr_ST2GT = Set()
model.CGHr_ST3GT = Set()
model.CGMs_1GT = Set()
model.CGMs_2GT = Set()
model.CGMs_3GT = Set()
model.CGMs_ST1GT = Set()
model.CGMs_ST2GT = Set()
model.CGMs_ST3GT = Set()
'''
model.TYPE = RangeSet(1, 6)
model.UNITxTYPE = Set(initialize=UNITxTYPE_init(), within=model.CG_NAMES*model.TYPE) # UNITxTYPE_init function
'''
# model.TYPEE = setof {(i,j) in UNITxTYPE} j;
'''
model.trans = Set(initialize=trans_init, within=model.UNITxTYPE*model.TYPE) # trans_init function

# Generator parameter
model.a = Param(model.UNIT_NAMES, initialize=a_init())  # parameter of fuel curve a -> a_init function
model.b = Param(model.UNIT_NAMES, initialize=b_init())  # parameter of fuel curve b -> b_init function
model.c = Param(model.UNIT_NAMES, initialize=c_init())  # parameter of fuel curve c -> c_init function
model.d = Param(model.UNIT_NAMES, initialize=d_init())  # parameter of fuel curve d -> d_init function
model.CV_th = Param(RangeSet(1, model.T), model.UNIT_NAMES, initialize=CV_th_init()) # parameter of calorific value -> CV_th_init function
model.UP_th = Param(RangeSet(1, model.T), model.UNIT_NAMES, initialize=UP_th_init()) # parameter of unit price -> UP_th_init function
# CG Generator parameter
'''
model.ca = Param(model.UNITxTYPE, initialize=ca_init()) # ca_init function
model.cb = Param(model.UNITxTYPE, initialize=cb_init()) # cb_init function
model.cc = Param(model.UNITxTYPE, initialize=cc_init()) # cc_init function
model.cd = Param(model.UNITxTYPE, initialize=cd_init()) # cd_init function
model.CV_cg = Param(RangeSet(1, model.T), model.CG_NAMES, initialize=CV_cg_init())
model.UP_cg = Param(RangeSet(1, model.T), model.CG_NAMES, initialize=UP_cg_init())
'''
model.cRU = Param(model.UNITxTYPE, initialize=cRU_init()) # CGDAT  Ramp_Up
model.cRD = Param(model.UNITxTYPE, initialize=cRD_init()) # CGDAT  Ramp_Down
model.cUT = Param(model.UNITxTYPE, initialize=cUT_init()) # CGDAT  Min_utime
model.cDT = Param(model.UNITxTYPE, initialize=cDT_init()) # CGDAT  Min_dtime
model.cmtl = Param(initialize=cmtl_init())
model.cmct = Param(initialize=cmct_init())
model.ctoff0 = Param(model.UNITxTYPE, initialize=ctoff0_init(), within=NonNegativeReals)
model.cton0 = Param(model.UNITxTYPE, initialize=cton0_init(), within=NonNegativeReals)
model.cu0 = Param(model.UNITxTYPE, initialize=cu0_init())
'''
def cfMAX_init(model, i, j):  # fuel cost at cpMAX
	return model.ca[i,j] + model.cb[i,j]*model.cpMAX[i,j] + model.cc[i,j]*model.cpMAX[i,j]**2 + model.cd[i,j]*model.cpMAX[i,j]**3
model.cfMAX = Param(model.UNITxTYPE, initialize=cfMAX_init)
def cfMIN_init(model, i, j):  # fuel cost at cpMIN
	return model.ca[i,j] + model.cb[i,j]*model.cpMIN[i,j] + model.cc[i,j]*model.cpMIN[i,j]**2 + model.cd[i,j]*model.cpMIN[i,j]**3
model.cfMIN = Param(model.UNITxTYPE, initialize=cfMIN_init)
def cs_init(model, i, j):  # fuel cost at cpMIN
	return (model.cfMAX[i,j]-model.cfMIN[i,j])/(model.cpMAX[i,j]-model.cpMIN[i,j])
model.cs = Param(model.UNITxTYPE, initialize=cs_init)  #MILP分段縣性的第一段
'''
model.cSc = Param(model.UNITxTYPE, initialize=cSc_init()) # cSc_init function
'''
param cuMoff11 {i in CGHr_1GT, t in 1..T};
param cuMoff21 {i in CGHr_2GT, t in 1..T};
param cuMoff31 {i in CGHr_3GT, t in 1..T};
param cuMoff41 {i in CGHr_ST1GT, t in 1..T};
param cuMoff51 {i in CGHr_ST2GT, t in 1..T};
param cuMoff61 {i in CGHr_ST3GT, t in 1..T};
param cuMrun11 {i in CGMs_1GT, t in 1..T};
param cuMrun21 {i in CGMs_2GT, t in 1..T};
param cuMrun31 {i in CGMs_3GT, t in 1..T};
param cuMrun41 {i in CGMs_ST1GT, t in 1..T};
param cuMrun51 {i in CGMs_ST2GT, t in 1..T};
param cuMrun61 {i in CGMs_ST3GT, t in 1..T};
param cuMoff1 {i in CGHr_1GT, t in 1..T};
param cuMoff2 {i in CGHr_2GT, t in 1..T};
param cuMoff3 {i in CGHr_3GT, t in 1..T};
param cuMoff4 {i in CGHr_ST1GT, t in 1..T};
param cuMoff5 {i in CGHr_ST2GT, t in 1..T};
param cuMoff6 {i in CGHr_ST3GT, t in 1..T};
'''
model.cuMrun = Param(model.CG_NAMES, RangeSet(1, model.T), initialize=cuMrun_init())
model.cuMoff = Param(model.UNITxTYPE, RangeSet(1, model.T), initialize=cuMoff_init())
'''
param cuMrun1 {i in CGMs_1GT, t in 1..T};
param cuMrun2 {i in CGMs_2GT, t in 1..T};
param cuMrun3 {i in CGMs_3GT, t in 1..T};
param cuMrun4 {i in CGMs_ST1GT, t in 1..T};
param cuMrun5 {i in CGMs_ST2GT, t in 1..T};
param cuMrun6 {i in CGMs_ST3GT, t in 1..T};
'''
# CG VARIABLES
model.cu = Var(model.UNITxTYPE, RangeSet(0, model.T), within=Binary)
def Tcu_init(model, i, j):
    return 0
model.Tcu = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=Tcu_init)
model.cy = Var(model.UNITxTYPE, RangeSet((-1)*(model.cmct), (model.T+model.cmtl)), within=Binary)
model.cz = Var(model.UNITxTYPE, RangeSet((-1)*(model.cmct), (model.T+model.cmtl)), within=Binary)
'''
model.cy1 = Var(model.UNITxTYPE, within=Binary)
model.cz1 = Var(model.UNITxTYPE, within=Binary)
'''
model.cus = Var(model.CG_NAMES, RangeSet(0, model.T))
#model.cp = Var(model.UNITxTYPE, RangeSet(1, model.T))
#model.cp2 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
def cp_sen_init(model, i, j):
    return 0
model.cp_sen = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=cp_sen_init)
def Tcp_init(model, i, j):
    return 0
model.Tcp = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=Tcp_init)
def CUNIT_COST_init(model, i, j):
    return 0
model.CUNIT_COST = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=CUNIT_COST_init)
def CUNIT_COST_sen_init(model, i, j):
    return 0
model.CUNIT_COST_sen = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=CUNIT_COST_sen_init)
def fuel_cg_init(model, i, j):
    return 0
model.fuel_cg = Var(model.CG_NAMES, RangeSet(1, model.T), initialize=fuel_cg_init)

model.pMAX = Param(model.UNIT_NAMES, initialize=pMAX_init())   # unit i maximum power output [MW]
model.pMIN = Param(model.UNIT_NAMES, initialize=pMIN_init())   # unit i minimum power output [MW]
def pBG1_init(model, i):
    return model.pMIN[i] + (model.pMAX[i] - model.pMIN[i])/3
model.pBG1 = Param(model.UNIT_NAMES, initialize=pBG1_init)   # Best gate generation -9896th[MW]
def pBG2_init(model, i):
    return model.pBG1[i] + (model.pMAX[i] - model.pMIN[i])/3
model.pBG2 = Param(model.UNIT_NAMES, initialize=pBG2_init)   # Best gate generation 2th[MW]

model.Sc = Param(model.UNIT_NAMES, initialize=Sc_init(), within=NonNegativeReals)     # unit i start cost [$] >= 0
model.Sdc = Param(model.UNIT_NAMES, initialize=Sdc_init(), within=NonNegativeReals)    # unit i shutdown cost [$] >= 0
model.RU = Param(model.UNIT_NAMES, initialize=RU_init(), within=NonNegativeReals)     # ramp-up limit of unit i [MW] >= 0
model.RD = Param(model.UNIT_NAMES, initialize=RD_init(), within=NonNegativeReals)     # ramp-down limit of unit i [MW] >= 0
def toffmax_init(model, i):
    return model.T+125
model.toffmax = Param(model.UNIT_NAMES, initialize=toffmax_init) # the MAX number of hours unit i can be off
def tonmax_init(model, i):
    return model.T+125
model.tonmax = Param(model.UNIT_NAMES, initialize=tonmax_init)  # the MAX number of hours unit i can be on
model.UT = Param(model.UNIT_NAMES, initialize=UT_init(), within=NonNegativeReals) # min up time limit [hour] >= 0
model.DT = Param(model.UNIT_NAMES, initialize=DT_init(), within=NonNegativeReals) # min down time limit [hour] >= 0
model.uMoff = Param(model.UNIT_NAMES, RangeSet(1, model.T), initialize=uMoff_init(), within=Binary)     # unit maintain parameter
model.uMrun = Param(model.UNIT_NAMES, RangeSet(1, model.T), initialize=uMrun_init(), within=Binary)     # unit Must-run parameter

model.mtl = Param(initialize=mtl_init())  # the MAX number of UT[i] and DT[i]
model.mct = Param(initialize=mct_init())  # the MAX number of UT[i] and DT[i]

model.toff0 = Param(model.UNIT_NAMES, initialize=toff0_init(), within=NonNegativeReals) #
model.ton0 = Param(model.UNIT_NAMES, initialize=ton0_init(), within=NonNegativeReals)  #
model.u0 = Param(model.UNIT_NAMES, initialize=u0_init(), within=Binary)     # unit state at time 0

# Bus parameter
model.demand = Param(RangeSet(1, model.T), initialize=demand_init())  # demand at time t [MW]
model.sR = Param(RangeSet(1, model.T), model.UNIT_TYPE, initialize=sR_init(UNIT_TYPE=model.UNIT_TYPE))      # spinning reserve at time t [MW]
							# t=No. of time steps
							# i=No. of unit

# VARIABLES
model.u = Var(model.UNIT_NAMES, RangeSet(1, model.T), within=Binary)     # state of thermal unit i at time t
						# u[i,t]=0 unit shut down
						# u[i,t]=1 unit in operation
model.y = Var(model.UNIT_NAMES, RangeSet(((-1)*model.mct), (model.T + model.mtl)), within=Binary) # y[i,t]=1 unit i start-up at time t
model.z = Var(model.UNIT_NAMES, RangeSet(((-1)*model.mct), (model.T + model.mtl)), within=Binary) # z[i,t]=1 unit i shut-down at time t
model.toff = Var(model.UNIT_NAMES, RangeSet(1, model.T))  # off-time counter
model.ton = Var(model.UNIT_NAMES, RangeSet(1, model.T))   # on-time counter
'''
model.y1 = Var(model.UNIT_NAMES, within=Binary)  #
model.z1 = Var(model.UNIT_NAMES, within=Binary) #
'''
# MODEL EQUATIONS
# piecewise-linear fuel curve characteristics(3 segments, 4 breakpoints)
model.p = Var(model.UNIT_NAMES, RangeSet(1, model.T))
model.p1 = Var(model.UNIT_NAMES, RangeSet(1, model.T), within=NonNegativeReals) #[MW]
model.p2 = Var(model.UNIT_NAMES, RangeSet(1, model.T), within=NonNegativeReals) #[MW]
model.p3 = Var(model.UNIT_NAMES, RangeSet(1, model.T), within=NonNegativeReals) #[MW]
model.p4 = Var(model.UNIT_NAMES, RangeSet(1, model.T), within=NonNegativeReals) #[MW]
# save min_cost/max_profit value for parameter analysis.
def UNIT_COST_init(model, i, j):
    return 0
model.UNIT_COST = Var(model.UNIT_NAMES, RangeSet(1, model.T), initialize=UNIT_COST_init)
def UNIT_COST_sen_init(model, i, j):
    return 0
model.UNIT_COST_sens = Var(model.UNIT_NAMES, RangeSet(1, model.T), initialize=UNIT_COST_sen_init)
def fuel_th_init(model, i, j):
    return 0
model.fuel_th = Var(model.UNIT_NAMES, RangeSet(1, model.T), initialize=fuel_th_init)
# f
def fMAX_init(model, i):  # fuel cost at pMAX
	return model.a[i] + model.b[i]*model.pMAX[i] + model.c[i]*model.pMAX[i]**2 + model.d[i]*model.pMAX[i]**3
model.fMAX = Param(model.UNIT_NAMES, initialize=fMAX_init)

def fMIN_init(model, i):  # fuel cost at pMIN
	return model.a[i] + model.b[i]*model.pMIN[i] + model.c[i]*model.pMIN[i]**2 + model.d[i]*model.pMIN[i]**3
model.fMIN = Param(model.UNIT_NAMES, initialize=fMIN_init)

def fBG1_init(model, i):  # fuel cost at pBG1
	return model.a[i] + model.b[i]*model.pBG1[i] + model.c[i]*model.pBG1[i]**2 + model.d[i]*model.pBG1[i]**3
model.fBG1 = Param(model.UNIT_NAMES, initialize=fBG1_init)

def fBG2_init(model, i):  # fuel cost at pBG2
	return model.a[i] + model.b[i]*model.pBG2[i] + model.c[i]*model.pBG2[i]**2 + model.d[i]*model.pBG2[i]**3
model.fBG2 = Param(model.UNIT_NAMES, initialize=fBG2_init)
# Slope
def sBG1_init(model, i):  # BG 0-1 slope
	return (model.fBG1[i] - model.fMIN[i])/(model.pBG1[i] - model.pMIN[i])
model.sBG1 = Param(model.UNIT_NAMES, initialize=sBG1_init)

def sBG2_init(model, i):  # BG 0-1 slope
	return (model.fBG2[i] - model.fBG1[i])/(model.pBG2[i] - model.pBG1[i])
model.sBG2 = Param(model.UNIT_NAMES, initialize=sBG2_init)

def sMAX_init(model, i):  # BG 0-1 slope
	return (model.fMAX[i] - model.fBG2[i])/(model.pMAX[i] - model.pBG2[i])
model.sMAX = Param(model.UNIT_NAMES, initialize=sMAX_init)
##------------------------------------新增參數-------------------------
# piecewise-linear fuel curve characteristics(6 segments, 7 breakpoints) FOR CG
#milp cp 變數
model.cp = Var(model.UNITxTYPE, RangeSet(1, model.T))
model.cp1 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp2 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp3 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp4 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp5 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp6 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
model.cp7 = Var(model.UNITxTYPE, RangeSet(1, model.T), within=NonNegativeReals)
##milp cpSTEP2
model.cpMIN = Param(model.UNITxTYPE, initialize=cpMIN_init())
model.cpSTEP2 = Param(model.UNITxTYPE, initialize=cpSTEP2_init()) # cpSTEP2_init function
model.cpSTEP3 = Param(model.UNITxTYPE, initialize=cpSTEP3_init()) 
model.cpSTEP4 = Param(model.UNITxTYPE, initialize=cpSTEP4_init())
model.cpSTEP5 = Param(model.UNITxTYPE, initialize=cpSTEP5_init())
model.cpSTEP6 = Param(model.UNITxTYPE, initialize=cpSTEP6_init())
model.cpSTEP7 = Param(model.UNITxTYPE, initialize=cpSTEP7_init()) # cpMAX_init function
model.cpMAX = Param(model.UNITxTYPE, initialize=cpMAX_init()) # cpMAX_init function

#CG MILP 熱耗率
model.fcpMIN = Param(model.UNITxTYPE, initialize=fcpMIN_init())
model.fcpSTEP2 = Param(model.UNITxTYPE, initialize=fcpSTEP2_init())
model.fcpSTEP3 = Param(model.UNITxTYPE, initialize=fcpSTEP3_init())
model.fcpSTEP4 = Param(model.UNITxTYPE, initialize=fcpSTEP4_init())
model.fcpSTEP5 = Param(model.UNITxTYPE, initialize=fcpSTEP5_init())
model.fcpSTEP6 = Param(model.UNITxTYPE, initialize=fcpSTEP6_init())
model.fcpSTEP7 = Param(model.UNITxTYPE, initialize=fcpSTEP7_init())
#CG MILP 斜率
model.fcpSeg1 = Param(model.UNITxTYPE, initialize=fcpSeg1_init())
model.fcpSeg2 = Param(model.UNITxTYPE, initialize=fcpSeg2_init())
model.fcpSeg3 = Param(model.UNITxTYPE, initialize=fcpSeg3_init())
model.fcpSeg4 = Param(model.UNITxTYPE, initialize=fcpSeg4_init())
model.fcpSeg5 = Param(model.UNITxTYPE, initialize=fcpSeg5_init())
model.fcpSeg6 = Param(model.UNITxTYPE, initialize=fcpSeg6_init())
#燃料參數
model.cE = Param(model.UNITxTYPE, initialize=cE_init())
#負循環計算時間參數
model.ctoff = Var(model.UNITxTYPE, RangeSet(1, model.T))  # off-time counter 運轉多久時間
model.cton = Var(model.UNITxTYPE, RangeSet(1, model.T))   # on-time counter  停機多久時間
def ctoffmax_init(model, i, j):
    return model.T+125
model.ctoffmax = Param(model.UNITxTYPE, initialize=ctoffmax_init) # the MAX number of hours unit i can be off
def ctonmax_init(model, i, j):
    return model.T+125
model.ctonmax = Param(model.UNITxTYPE, initialize=ctonmax_init)  # the MAX number of hours unit i can be on
#負循環EOH
model.dEOH = Var(model.UNITxTYPE, RangeSet(1, model.T))  #第t小時累計EOH時數
model.availabledailyEOH = Param(model.UNITxTYPE, initialize=availabledailyEOH()) #平均每天可使用eoh
model.cyc = Var(model.UNITxTYPE, RangeSet(1, model.T))    #第t小時累計開機次數
model.thismondayEOH = Param(model.UNITxTYPE, initialize=thismondayEOH()) #平均每天可使用eoh

#------------------------------------------------
# OBJECTIVE
# MINIMUM COST
def obj_expression(model):# 檢查一下 有可能打錯
	time = RangeSet(model.ST,model.ET)
	time.construct()
	return (
		(
			sum(
				(((model.u[i,t]*(1-model.uMoff[i,t]))*model.fMIN[i] + model.p2[i,t]*model.sBG1[i] + model.p3[i,t]*model.sBG2[i] + model.p4[i,t]*model.sMAX[i])*1 +
				(model.y[i,t]*model.Sc[i])+(model.z[i,t]*model.Sdc[i]))*model.UP_th[t,i]/model.CV_th[t,i] for i in model.UNIT_NAMES for t in time
			) +
			sum(
				(
				(model.cu[i,j,t]*(1-model.cuMoff[i,j,t])*model.fcpMIN[i,j])+ 
				(model.cp2[i,j,t]*model.fcpSeg1[i,j])+ 
				(model.cp3[i,j,t]*model.fcpSeg2[i,j])+ 
				(model.cp4[i,j,t]*model.fcpSeg3[i,j])+ 
				(model.cp5[i,j,t]*model.fcpSeg4[i,j])+ 
				(model.cp6[i,j,t]*model.fcpSeg5[i,j])+ 
				(model.cp7[i,j,t]*model.fcpSeg6[i,j]))*model.cE[i,j]+ 
				(model.cy[i,j,t]*model.cSc[i,j]) for (i,j) in model.UNITxTYPE for t in time
			) -
			sum(
				model.cy[i,j,t]*model.cu[i,j,t-1]*model.cSc[i,j] for (i,j) in model.UNITxTYPE for t in time
			)
		)
		)

model.OBJ = Objective(rule=obj_expression)


# thermal CONSTRAINTS
# Piecewise-linear fuel curve
def power_generation_rule(model,i,t):
	return model.p[i,t] == model.p1[i,t] + model.p2[i,t] + model.p3[i,t] + model.p4[i,t]
model.power_generation = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule=power_generation_rule)

def min_generation_rule(model,i,t):
	return model.p1[i,t] == model.pMIN[i]*model.u[i,t]*(1 - model.uMoff[i,t])
model.min_generation = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule=min_generation_rule)

def max2_generation_rule(model,i,t):
	return model.p2[i,t] <= (model.pBG1[i] - model.pMIN[i])*model.u[i,t]*(1 - model.uMoff[i,t])
model.max2_generation = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule=max2_generation_rule)

def max3_generation_rule(model,i,t):
	return model.p3[i,t] <= (model.pBG2[i] - model.pBG1[i])*model.u[i,t]*(1 - model.uMoff[i,t])
model.max3_generation = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule=max3_generation_rule)

def max4_generation_rule(model,i,t):
	return model.p4[i,t] <= (model.pMAX[i] - model.pBG2[i])*model.u[i,t]*(1 - model.uMoff[i,t])
model.max4_generation = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule=max4_generation_rule)

#power_balance Constraint
def power_balance(model,t):
	return sum(model.p[i,t] for i in model.UNIT_NAMES) + sum(model.cp[i,j,t] for (i,j) in model.UNITxTYPE) == model.demand[t]
model.power_balance = Constraint(RangeSet(model.ST,model.ET),rule = power_balance)

#spinning_reserve Constraints
def spinning_reserve1(model,t):#可以這樣寫? (u[i,t]*pMAX[i]-p[i,t])>=sR[t,"th"];
	return sum(model.u[i,t]*model.pMAX[i]-model.p[i,t] for i in model.UNIT_NAMES) >= model.sR[t,"th"]
model.spinning_reserve1 = Constraint(RangeSet(model.ST,model.ET),rule = spinning_reserve1)

def spinning_reserve_CG(model,i,j,t):#可以這樣寫? (cu[i,j,t]*cpMAX[i,j]-cp[i,j,t])>=sR[t,"cg"]
#	if model.cpMAX[i,j] == 0:
#		if 	model.cpSTEP6[i,j] == 0:
#			return sum(model.cu[i,j,t]*model.cpSTEP5[i,j]-model.cp[i,j,t] for (i,j) in model.UNITxTYPE) >= 0.3*model.sR[t,"cg"]
#		else:
#			return sum(model.cu[i,j,t]*model.cpSTEP6[i,j]-model.cp[i,j,t] for (i,j) in model.UNITxTYPE) >= 0.3*model.sR[t,"cg"]					
	return sum(model.cu[i,j,t]*max((model.cpSTEP7[i,j],model.cpSTEP6[i,j],model.cpSTEP5[i,j]))-model.cp[i,j,t] for (i,j) in model.UNITxTYPE) >= model.sR[t,"cg"]
model.spinning_reserve_CG = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = spinning_reserve_CG)

#Unit must_off and must_run Constraints
def unit_must_run(model,i,t):
	return model.u[i,t] >= model.uMrun[i,t]
model.unit_must_run = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = unit_must_run)

def unit_must_off(model,i,t):
	return (model.u[i,t] + model.uMoff[i,t]) <= 1
model.unit_must_off = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = unit_must_off)

def logic_of_must_run_rule(model, i, t):
	if (model.uMoff[i,t] + model.uMrun[i,t]) <= 1:
		return Constraint.Feasible
	else:
		return Constraint.Infeasible
model.logic_of_must_run = Constraint(model.UNIT_NAMES, RangeSet(model.ST,model.ET), rule=logic_of_must_run_rule)

# Unit Maximum/Minimum Generation Constraints
def power_lower_limit_rule(model,i,t):
	return (model.pMIN[i]*model.u[i,t]) <= model.p[i,t]
model.power_lower_limit = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = power_lower_limit_rule)

def power_upper_limit_rule(model,i,t):
	return (model.pMAX[i]*model.u[i,t]) >= model.p[i,t]
model.power_upper_limit=Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = power_upper_limit_rule)

#ramp_up_limit and ramp_down_limit
def ramp_up_limit(model,i,t):
	return (model.p[i,t+1] - model.p[i,t]) <= model.RU[i]*60*1
model.ramp_up_limit = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET-1),rule = ramp_up_limit)

def ramp_down_limit(model,i,t):
	return (model.p[i,t] - model.p[i,t+1]) <= model.RD[i]*60*1
model.ramp_down_limit = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET-1),rule = ramp_down_limit)

# Unit Startup/Shutdown Constraints
def logic_of_startups_and_shutdowns_1_rule(model, i, t):#P.38 (13)
	return model.u[i,t] - model.u[i,t-1] == model.y[i,t] - model.z[i,t]
model.logic_of_startups_and_shutdowns_1 = Constraint(model.UNIT_NAMES,RangeSet(model.ST+1, model.ET),rule = logic_of_startups_and_shutdowns_1_rule)

def logic_of_startups_and_shutdowns_2_rule(model, i, t):#P.38 (14)
	return (model.y[i,t] + model.z[i,t]) <= 1
model.logic_of_startups_and_shutdowns_2 = Constraint(model.UNIT_NAMES,RangeSet(model.ST, model.ET),rule = logic_of_startups_and_shutdowns_2_rule)

def logic_of_startups_and_shutdowns_3_rule(model, i):
	return model.u[i,1] - model.u0[i] == model.y[i,1] - model.z[i,1]
model.logic_of_startups_and_shutdowns_3 = Constraint(model.UNIT_NAMES, rule = logic_of_startups_and_shutdowns_3_rule)

def y_logic_1_rule(model, i, t):
	return model.y[i,t] == 0
model.y_logic_1 = Constraint(model.UNIT_NAMES, RangeSet((model.T+1), (model.T + model.mtl)),rule = y_logic_1_rule)

def y_logic_2_rule(model, i, t):
	return model.y[i,t] == 0
model.y_logic_2 = Constraint(model.UNIT_NAMES, RangeSet((-1)*model.mtl, 0),rule = y_logic_2_rule)

def z_logic_1_rule(model, i, t):
	return model.z[i,t] == 0
model.z_logic_1 = Constraint(model.UNIT_NAMES, RangeSet((model.T+1),(model.T+model.mtl)),rule = z_logic_1_rule)

def z_logic_2_rule(model, i, t):
	return model.z[i,t] == 0
model.z_logic_2 = Constraint(model.UNIT_NAMES, RangeSet((-1)*model.mtl, 0),rule = z_logic_2_rule)

# Unit Down Time Counter Constraints
def toff_constraint_1_rule(model, i, t):
	return model.toff[i,t] <= (model.toff[i,t-1] + 1)
model.toff_constraint_1 = Constraint(model.UNIT_NAMES,RangeSet(model.ST+1, model.ET),rule = toff_constraint_1_rule)

def toff_constraint_2_rule(model, i):
	return model.toff[i,1] <= (model.toff0[i] + 1)
model.toff_constraint_2 = Constraint(model.UNIT_NAMES,rule = toff_constraint_2_rule)

def toff_constraint_3_rule(model, i, t):
	return (model.toff[i,t] + (model.toffmax[i] + 1)*model.u[i,t]) >= (model.toff[i,t-1] + 1)
model.toff_constraint_3 = Constraint(model.UNIT_NAMES,RangeSet(model.ST+1, model.T), rule = toff_constraint_3_rule)

def toff_constraint_4_rule(model, i):
	return (model.toff[i,1] + (model.toffmax[i] + 1)*model.u[i,1]) >= (model.toff0[i] + 1)
model.toff_constraint_4 = Constraint(model.UNIT_NAMES,rule = toff_constraint_4_rule)

def toff_constraint_5_rule(model, i, t):
	return (model.toff[i,t] - model.toffmax[i]*(1 - model.u[i,t])) <= 0
model.toff_constraint_5 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = toff_constraint_5_rule)

def toff_constraint_6_rule(model, i, t):
	return model.toff[i,t] >= 0
model.toff_constraint_6 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = toff_constraint_6_rule)

# Unit Up Time Counter Constraints
def ton_constraint_1_rule(model,i,t):
	return model.ton[i,t] <= (model.ton[i,t-1] + 1)
model.ton_constraint_1 = Constraint(model.UNIT_NAMES,RangeSet(model.ST+1,model.ET),rule = ton_constraint_1_rule)

def ton_constraint_2_rule(model,i):
	return model.ton[i,1] <= (model.ton0[i] + 1)
model.ton_constraint_2 = Constraint(model.UNIT_NAMES, rule = ton_constraint_2_rule)

def ton_constraint_3_rule(model,i,t):
	return (model.ton[i,t] + (model.tonmax[i] + 1)*(1 - model.u[i,t])) >= (model.ton[i,t-1] + 1)
model.ton_constraint_3 = Constraint(model.UNIT_NAMES,RangeSet(model.ST+1,model.T),rule = ton_constraint_3_rule)

def ton_constraint_4_rule(model,i):
	return (model.ton[i,1] + (model.tonmax[i] + 1)*(1 - model.u[i,1])) >= (model.ton0[i] + 1)
model.ton_constraint_4 = Constraint(model.UNIT_NAMES,rule = ton_constraint_4_rule)

def ton_constraint_5_rule(model,i,t):
	return (model.ton[i,t] - model.tonmax[i]*model.u[i,t]) <= 0
model.ton_constraint_5 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = ton_constraint_5_rule)

def ton_constraint_6_rule(model,i,t):
	return model.ton[i,t] >= 0
model.ton_constraint_6 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = ton_constraint_6_rule)

#thermal min_down_time and min_up_time
def min_up_time_1(model,i,t): #sum {k in (t+1)..(t+(UT[i] div 1+min((UT[i]-(UT[i] div 1)*1)*999,1))-1)} z[i,k]) <=1
	if model.UT[i] - (model.UT[i] // 1) > 0.001:
		time = RangeSet(t+1,(model.UT[i] // 1) + 1)
	else:
		time = RangeSet(t+1,model.UT[i] // 1)
	time.construct()
	return (model.y[i,t] + sum(model.z[i,k] for k in time)) <= 1
model.min_up_time_1 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = min_up_time_1)

def min_down_time_1(model,i,t):#(z[i,t]+sum {k in (t+1)..(t+(DT[i] div 1+min((DT[i]-(DT[i] div 1)*1)*999,1))-1)} y[i,k]) <=1
	if model.DT[i] - (model.DT[i] // 1) > 0.001:
		time = RangeSet(t+1,(model.DT[i] // 1) + 1)
	else:
		time = RangeSet(t+1,model.DT[i] // 1)
	time.construct()
	return (model.z[i,t] + sum(model.y[i,k] for k in time)) <= 1
model.min_down_time_1 = Constraint(model.UNIT_NAMES,RangeSet(model.ST,model.ET),rule = min_down_time_1)

#thermal state_logic
state_logic1_time = state_logic1_time_data(ST=model.ST)
def state_logic1_rule(model,i,t):#{i in UNIT_NAMES,t in ST..(ST-1+((UT[i]-ton0[i]) div 1+min(((UT[i]-ton0[i])-((UT[i]-ton0[i]) div 1)*1)*99,1))) : u0[i] > 0}
	if model.u0[i] > 0:
		global state_logic1_time
		if state_logic1_time[i] <= 0:
			return Constraint.Skip
		else:
			if t < state_logic1_time[i]+1:
				return model.u[i,t] >= 1
			else:
				return Constraint.Skip  # 超過時間的位置沒限制
	return Constraint.Skip # 不再範圍內的機組沒限制
model.state_logic1 = Constraint(model.UNIT_NAMES, RangeSet(model.ST,model.ET),rule = state_logic1_rule)

state_logic2_time = state_logic2_time_data(ST=model.ST)
# 如果最大值是4.5 回傳5 最大值是4.001 回傳4 分界是0.01
def state_logic2_rule(model,i,t):#{i in UNIT_NAMES,t in ST..(ST-1+((DT[i]-toff0[i]) div 1+min(((DT[i]-toff0[i])-((DT[i]-toff0[i]) div 1)*1)*99,1))) : u0[i] < 1}
	if model.u0[i] < 1:
		global state_logic2_time
		if state_logic2_time[i] <= 0:
			return Constraint.Skip
		else:
			if t < state_logic2_time[i]+1:
				return model.u[i,t] <= 0
			else:
				return Constraint.Skip
	return Constraint.Skip
model.state_logic2 = Constraint(model.UNIT_NAMES, RangeSet(model.ST,model.ET), rule = state_logic2_rule)


#-----------------------------------------------------------------------------------------------------------------------------
# CG_CONSTRAINTS
#type_limit
def type_limit(model,i,t):
	return sum(model.cu[ii,jj,t] if i ==ii else 0 for (ii,jj) in model.UNITxTYPE) <= 1
model.type_limit = Constraint(model.CG_NAMES,RangeSet(model.ST,model.ET),rule = type_limit)
#----------------新增 cgmilp  Piecewise-linear fuel curve
def CGpower_generation_rule(model,i,j,t):
	return model.cp[i,j,t] == model.cp1[i,j,t] + model.cp2[i,j,t] + model.cp3[i,j,t] + model.cp4[i,j,t] + model.cp5[i,j,t] + model.cp6[i,j,t] + model.cp7[i,j,t]
model.CGpower_generation_rule = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CGpower_generation_rule)

def CG_generation_rule(model,i,j,t):
	return model.cp1[i,j,t] == (model.cpMIN[i,j]*model.cu[i,j,t])*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule)

def CG_generation_rule2(model,i,j,t):
	return model.cp2[i,j,t] <= (model.cpSTEP2[i,j] - model.cpMIN[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule2 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule2)

def CG_generation_rule3(model,i,j,t):
	return model.cp3[i,j,t] <= (model.cpSTEP3[i,j] - model.cpSTEP2[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule3 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule3)

def CG_generation_rule4(model,i,j,t):
	return model.cp4[i,j,t] <= (model.cpSTEP4[i,j] - model.cpSTEP3[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule4 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule4)

def CG_generation_rule5(model,i,j,t):
	if model.cpSTEP5[i,j] == 0:
		return model.cp5[i,j,t] == 0
	else:	
		return model.cp5[i,j,t] <= (model.cpSTEP5[i,j] - model.cpSTEP4[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule5 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule5)

def CG_generation_rule6(model,i,j,t):
	if model.cpSTEP6[i,j] == 0:
		return model.cp6[i,j,t] == 0
	else:
		return model.cp6[i,j,t] <= (model.cpSTEP6[i,j] - model.cpSTEP5[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule6 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule6)

def CG_generation_rule7(model,i,j,t):
	if model.cpSTEP7[i,j] == 0:
		return model.cp7[i,j,t] == 0
	else:
		return model.cp7[i,j,t] <= (model.cpSTEP7[i,j] - model.cpSTEP6[i,j])*model.cu[i,j,t]*(1 - model.cuMoff[i,j,t])
model.CG_generation_rule7 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule=CG_generation_rule7)
#---------- 新增機組運轉或停機計時
# Unit Up Time Counter Constraints
def cton_constraint_1_rule(model, i, j, t):
	return model.cton[i,j,t] <= (model.cton[i,j,t-1] + 1)
model.cton_constraint_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST+1,model.ET),rule = cton_constraint_1_rule)

def cton_constraint_2_rule(model, i, j):
	return model.cton[i,j,1] <= (model.cton0[i,j] + 1)
model.cton_constraint_2 = Constraint(model.UNITxTYPE, rule = cton_constraint_2_rule)

def cton_constraint_3_rule(model, i, j, t):
	return (model.cton[i,j,t] + (model.ctonmax[i,j] + 1)*(1 - model.cu[i,j,t])) >= (model.cton[i,j,t-1] + 1)
model.cton_constraint_3 = Constraint(model.UNITxTYPE,RangeSet(model.ST+1,model.T),rule = cton_constraint_3_rule)

def cton_constraint_4_rule(model, i, j):
	return (model.cton[i,j,1] + (model.ctonmax[i,j] + 1)*(1 - model.cu[i,j,1])) >= (model.cton0[i,j] + 1)
model.cton_constraint_4 = Constraint(model.UNITxTYPE,rule = cton_constraint_4_rule)

def cton_constraint_5_rule(model, i, j, t):
	return (model.cton[i,j,t] - model.ctonmax[i,j]*model.cu[i,j,t]) <= 0
model.cton_constraint_5 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = cton_constraint_5_rule)

def cton_constraint_6_rule(model, i, j, t):
	return model.cton[i,j,t] >= 0
model.cton_constraint_6 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = cton_constraint_6_rule)

# Unit Down Time Counter Constraints
def ctoff_constraint_1_rule(model, i, j, t):
	return model.ctoff[i,j,t] <= (model.ctoff[i,j,t-1] + 1)
model.ctoff_constraint_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST+1, model.ET),rule = ctoff_constraint_1_rule)

def ctoff_constraint_2_rule(model, i, j):
	return model.ctoff[i,j,1] <= (model.ctoff0[i,j] + 1)
model.ctoff_constraint_2 = Constraint(model.UNITxTYPE,rule = ctoff_constraint_2_rule)

def ctoff_constraint_3_rule(model, i, j, t):
	return (model.ctoff[i,j,t] + (model.ctoffmax[i,j] + 1)*model.cu[i,j,t]) >= (model.ctoff[i,j,t-1] + 1)
model.ctoff_constraint_3 = Constraint(model.UNITxTYPE,RangeSet(model.ST+1, model.T), rule = ctoff_constraint_3_rule)

def ctoff_constraint_4_rule(model, i, j):
	return (model.ctoff[i,j,1] + (model.ctoffmax[i,j] + 1)*model.cu[i,j,1]) >= (model.ctoff0[i,j] + 1)
model.ctoff_constraint_4 = Constraint(model.UNITxTYPE,rule = ctoff_constraint_4_rule)

def ctoff_constraint_5_rule(model, i, j, t):
	return (model.ctoff[i,j,t] - model.ctoffmax[i,j]*(1 - model.cu[i,j,t])) <= 0
model.ctoff_constraint_5 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = ctoff_constraint_5_rule)

def ctoff_constraint_6_rule(model, i, j, t):
	return model.ctoff[i,j,t] >= 0
model.ctoff_constraint_6 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = ctoff_constraint_6_rule)

#----CGEOH限制式---------

def cyc_constraint_1_rule(model, i, j): #計算本次每個機組第t小時累計的開機次數
	return model.cyc[i,j,1] == (model.cy[i,j,1])
model.cyc_constraint_1 = Constraint(model.UNITxTYPE, rule = cyc_constraint_1_rule)

def cyc_constraint_2_rule(model, i, j, t): #計算本次每個機組第t小時累計的開機次數
	return model.cyc[i,j,t] == (model.cyc[i,j,t-1] + model.cy[i,j,t])
model.cyc_constraint_2 = Constraint(model.UNITxTYPE, RangeSet(model.ST+1,model.ET), rule = cyc_constraint_2_rule)

def dEOH_rule_1(model, i, j, t): #計算本次每個機組第t小時的eoh累計
	return model.dEOH[i,j,t] == model.cyc[i,j,t]*1.2+ model.cton[i,j,t]
model.dEOH_rule_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = dEOH_rule_1)

def dEOH_rule_2(model, i, j, t): #計算本次每個機組第t小時的eoh累計
	return model.dEOH[i,j,t] <= model.availabledailyEOH[i,j]
model.dEOH_rule_2 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = dEOH_rule_2)


#----------------------------------------------------------------------------------------
#CCramp_down_limit and CCramp_up_limit
def CCramp_up_limit(model,i,j,t):
	return (model.cp[i,j,t+1] - model.cp[i,j,t]) <= model.cRU[i,j]*60*1;
model.CCramp_up_limit = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET-1),rule = CCramp_up_limit)

def CCramp_down_limit(model,i,j,t):
	return (model.cp[i,j,t]-model.cp[i,j,t+1]) <= model.cRD[i,j]*60*1
model.CCramp_down_limit = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET-1),rule = CCramp_down_limit)

#must_run and must_off
def ccunit_must_run(model,i,t):
	return sum(model.cu[ii,jj,t] if i==ii else 0 for (ii,jj) in model.UNITxTYPE) >= model.cuMrun[i,t]
model.ccunit_must_run = Constraint(model.CG_NAMES,RangeSet(model.ST,model.ET),rule = ccunit_must_run)

def ccunit_must_off(model,i,j,t):
	return model.cu[i,j,t] + model.cuMoff[i,j,t] <= 1
model.ccunit_must_off = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = ccunit_must_off)

#logic_of_startups_and_shutdowns
def CClogic_of_startups_and_shutdowns_1(model,i,j,t):
	return (model.cu[i,j,t]- model.cu[i,j,t-1]) == model.cy[i,j,t] - model.cz[i,j,t]
model.CClogic_of_startups_and_shutdowns_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST+1,model.ET),rule = CClogic_of_startups_and_shutdowns_1)

def CClogic_of_startups_and_shutdowns_2(model,i,j,t):
	return model.cy[i,j,t] + model.cz[i,j,t] <= 1
model.CClogic_of_startups_and_shutdowns_2 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = CClogic_of_startups_and_shutdowns_2)

def CClogic_of_startups_and_shutdowns_3(model,i,j):
	return model.cu[i,j,1] - model.cu0[i,j] == model.cy[i,j,1]-model.cz[i,j,1]
model.CClogic_of_startups_and_shutdowns_3 = Constraint(model.UNITxTYPE,rule = CClogic_of_startups_and_shutdowns_3)

def CClogic_of_startups_and_shutdowns_4(model, i, j):
   	return model.cu[i,j,0] == model.cu0[i,j]
model.CClogic_of_startups_and_shutdowns_4 = Constraint(model.UNITxTYPE,rule = CClogic_of_startups_and_shutdowns_4)

def CClogic_of_startups_and_shutdowns_5(model,i,t):
	return sum(model.cu[ii,jj,t] if i==ii else 0 for (ii,jj) in model.UNITxTYPE) == model.cus[i,t]
model.CClogic_of_startups_and_shutdowns_5 = Constraint(model.CG_NAMES,RangeSet(model.ST,model.ET),rule = CClogic_of_startups_and_shutdowns_5)

def CClogic_of_startups_and_shutdowns_6(model,i):
	return model.cus[i,0] == sum(model.cu0[ii,jj] if i==ii else 0 for (ii,jj) in model.UNITxTYPE)
model.CClogic_of_startups_and_shutdowns_6 = Constraint(model.CG_NAMES,rule = CClogic_of_startups_and_shutdowns_6)

def CClogic_of_startups_and_shutdowns_7(model,i,j,t):  #{(i,j) in UNITxTYPE, t in ST..ET : j<=3}:
	if j <= 3:
		return model.cus[i,t-1]-sum(model.cu[ii,k,t-1] if i==ii and j==jj else 0 for (ii,jj,k) in model.trans) <= (-1)*model.cy[i,j,t]+1
	return Constraint.Skip
model.CClogic_of_startups_and_shutdowns_7 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = CClogic_of_startups_and_shutdowns_7)

def CClogic_of_startups_and_shutdowns_8(model,i,j,t): #不確定對不對 {(i,j) in UNITxTYPE, t in ST..ET : j>=4}:
	if j <= 4:
		return sum(model.cu[ii,k,t-1] if i==ii and j==jj else 0 for (ii,jj,k) in model.trans) - model.cy[i,j,t] >= 0
	return Constraint.Skip
model.CClogic_of_startups_and_shutdowns_8 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = CClogic_of_startups_and_shutdowns_8)

def CClogic_of_startups_and_shutdowns_9(model,i,t): #(i,j) in UNITxTYPE : j<4
	return sum(model.cu[ii,jj,t-1] if i==ii else 0 for (ii,jj) in model.UNITxTYPE) - sum(model.cu[ii,jj,t-1] if i==ii and jj<4 else 0 for (ii,jj) in model.UNITxTYPE) <= sum(model.cu[ii,jj,t] if i==ii else 0 for (ii,jj) in model.UNITxTYPE)
model.CClogic_of_startups_and_shutdowns_9 = Constraint(model.CG_NAMES,RangeSet(model.ST+1,model.T),rule = CClogic_of_startups_and_shutdowns_9)

#機組邏輯限式
def CCy_logic_1(model,i,j,t):
	return model.cy[i,j,t] == 0
model.CCy_logic_1 = Constraint(model.UNITxTYPE,RangeSet(model.T+1,model.T+model.cmtl),rule = CCy_logic_1)

def CCy_logic_2(model,i,j,t):
	return model.cy[i,j,t] == 0
model.CCy_logic_2 = Constraint(model.UNITxTYPE,RangeSet((-1)*model.cmct,0),rule = CCy_logic_2)

def CCz_logic_1(model,i,j,t):
	return model.cz[i,j,t] == 0
model.CCz_logic_1 = Constraint(model.UNITxTYPE,RangeSet(model.T+1,model.T+model.cmtl),rule = CCz_logic_1)

def CCz_logic_2(model,i,j,t):  #注意負號
	return model.cz[i,j,t] == 0
model.CCz_logic_2 = Constraint(model.UNITxTYPE,RangeSet((-1)*model.cmct,0),rule = CCz_logic_2)

#機組最小運轉時間與最小停機時間限制
def CCmin_up_time_1(model,i,j,t):
	if model.cUT[i,j] - (model.cUT[i,j] // 1) > 0.001:
		time = RangeSet(t+1,(model.cUT[i,j] // 1) + 1)
	else:
		time = RangeSet(t+1,model.cUT[i,j] // 1)
	time.construct()
	return (model.cy[i,j,t]+sum(model.cz[i,j,k] for k in time)) <= 1
model.CCmin_up_time_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = CCmin_up_time_1)

def CCmin_down_time_1(model,i,j,t):
	if model.cDT[i,j] - (model.cDT[i,j] // 1) > 0.001:
		time = RangeSet(t+1,(model.cDT[i,j] // 1) + 1)
	else:
		time = RangeSet(t+1,model.cDT[i,j] // 1)
	time.construct()
	return (model.cz[i,j,t]+sum(model.cy[i,j,k] for k in time)) <= 1
model.CCmin_down_time_1 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET),rule = CCmin_down_time_1)

#後面看不懂 有endtime {(i,j) in UNITxTYPE,t in ST..(ST-1+((cUT[i,j]-cton0[i,j]) div 1+min(((cUT[i,j]-cton0[i,j])-((cUT[i,j]-cton0[i,j]) div 1)*1)*99,1))) : cu0[i,j] > 0}
state_logic_cg1_time = state_logic_cg1_time_data(ST=model.ST)
def state_logic_cg1_rule(model,i,j,t):
	if model.cu0[i,j]>0:
		global state_logic_cg1_time
		if state_logic_cg1_time[i,j] <= 0:
			return Constraint.Skip
		else:
			if t < state_logic_cg1_time[i,j]+1:
				return model.cu[i,j,t] >= 1
			else:
				return Constraint.Skip   # 超過時間的位置沒限制
	return Constraint.Skip               # 不再範圍內的機組沒限制
model.state_logic_cg1_rule = Constraint(model.UNITxTYPE, RangeSet(model.ST,model.ET),rule = state_logic_cg1_rule)


state_logic_cg2_time = state_logic_cg2_time_data(ST=model.ST)
def state_logic_cg2_rule(model,i,j,t):#{(i,j) in UNITxTYPE,t in ST..(ST-1+((cDT[i,j]-ctoff0[i,j]) div 1+min(((cDT[i,j]-ctoff0[i,j])-((cDT[i,j]-ctoff0[i,j]) div 1)*1)*99,1))) : cu0[i,j] < 1}
	if model.cu0[i,j] < 1:
		global state_logic_cg2_time
		if state_logic_cg2_time[i,j] <= 0:
			return Constraint.Skip
		else:
			if t < state_logic_cg2_time[i,j]+1:
				return model.cu[i,j,t] <= 0
			else:
				return Constraint.Skip
	return Constraint.Skip
model.state_logic_cg2 = Constraint(model.UNITxTYPE,RangeSet(model.ST,model.ET), rule = state_logic_cg2_rule)
#機組燃料單價?
# calculate unit cost/fuel quantity in each time step
def unit_cost_value(model,i,t):
	return model.UNIT_COST[i,t] == ((model.u[i,t]*(1-model.uMoff[i,t]))*model.fMIN[i]+model.p2[i,t]*model.sBG1[i]+model.p3[i,t]*model.sBG2[i]+model.p4[i,t]*model.sMAX[i])*1*model.UP_th[t,i]/model.CV_th[t,i]
model.unit_cost_value = Constraint(model.UNIT_NAMES, RangeSet(model.ST,model.ET), rule = unit_cost_value)

def cunit_cost_value (model,i,t):
	return model.fuel_th[i,t] == model.UNIT_COST[i,t]/model.UP_th[t,i]
model.unit_fuel_quantity = Constraint(model.UNIT_NAMES, RangeSet(model.ST,model.ET), rule = cunit_cost_value)
'''
def cunit_cost_value (model,i,t):
	return model.CUNIT_COST[i,t] == sum((model.cu[ii,jj,t]*model.cfMIN[ii,jj] + model.cp2[ii,jj,t]*model.cs[ii,jj])*model.UP_cg[t,i]/model.CV_cg[t,i]*1 if i==ii else 0 for (ii,jj) in model.UNITxTYPE)
model.cunit_cost_value = Constraint(model.CG_NAMES, RangeSet(model.ST,model.ET), rule = cunit_cost_value)

def cunit_fuel_quantity(model,i,t):
	return model.fuel_cg[i,t] == (model.CUNIT_COST[i,t])/(model.UP_cg[t,i])  #[t,i]?
model.cunit_fuel_quantity = Constraint(model.CG_NAMES, RangeSet(model.ST,model.ET), rule = cunit_fuel_quantity)
'''