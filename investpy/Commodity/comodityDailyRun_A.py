# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/
# url = 'http://www.shfe.com.cn/statements/dataview.html?paramid=weeklystock' 
# url = '交易数据.html'

@author: haoli

"""

import sys
sys.path.append("../")

import investpy.Commodity.SHFE_A as mySHFE_A
import investpy.Commodity.COMEX_A as myCOMEX_A
import investpy.Commodity.COMEX_daily_openInterest_VOL as myCOMEX_dailyVolOI


import investpy.Commodity.LME_A as myLME_A

from datetime import datetime
import investpy.Commodity.LME_daily_volume as myLME_dailyVol

import investpy.Commodity.LME_weekly_traderReport as myLME_weeklyTraderReport
import investpy.Commodity.LME_daily_openInterest_E as myLME_daily_openInterest

#----------------------------------
errorFileTargetDir = '../'


"""
"Return day of the week, where Monday == 0 ... Sunday == 6."
"""

# def isToday_weekend(dateStr):
#     d1 = datetime.strptime(dateStr, '%Y-%m-%d')
#     # print(d1)
#     result = ( (d1.weekday() == 5) or  (d1.weekday() == 6) )
#     return result
# dateStr = '2021-04-16'
# num = 4
# print (isToday_weekday(dateStr, num) )

# def isToday_weekend():
#     dd = datetime.today()
#     result = ( (dd.weekday() == 5) or  (dd.weekday() == 6) )
#     return result

def weekend_runCommodity():
    myLME_weeklyTraderReport.weekly_traderReport()
    mySHFE_A.weeklyRun_SHFE_Stock()
def daily_runCommodity():
    #------------------
    myLME_A.LME_A_daily_Run()
    myLME_dailyVol.LME_volume_daily_run() 
    myLME_daily_openInterest.LME_openInterest_daily()
    
    #------------------
    myCOMEX_A.COMEX_daily_Run()        
    myCOMEX_dailyVolOI.CME_Vio_daily_run() 
    
    
    if datetime.today().weekday() == 3: # Thursday
        myCOMEX_A.COMEX_gainStock_Tuesday_weekly_Run()
            
# myCOMEX_A.COMEX_bondsFuture_Delivered_Q_Run()    

#daily_runCommodity()






#----------not used functions
