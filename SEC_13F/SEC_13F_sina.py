# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/


@author: haoli
"""


import sys
sys.path.append("../")
import const_common as constA
# import Const_NYMEXCOMEX_A as constCOMEX_A

# import requests
from os import makedirs
import os.path as myPath
import pandas as pd

from urllib.request import urlopen, Request
from pathlib import Path 
from datetime import datetime

import os

import pyodbc
import numpy as np

import time
from selenium import webdriver

import ntpath

# import pyautogui, time
# pyautogui.PAUSE =2.5
#----------------------------------
def makedir_ifnonexists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

errorFileTargetDir = '../'


dir_SEC_13F_sina = './SEC_13F_sina'
makedir_ifnonexists(dir_SEC_13F_sina)

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SEC' 


pd.set_option('mode.chained_assignment', None)

#--------table name ---------
_sqlTable_SEC_13F_sina_Q = 'SEC_13F_sina_Q'     


"""

"""
def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)
        

def getDateFromString(dateStr, keyword): 
    if keyword == '':
        d = dateStr
    else:        
        b = dateStr.split(keyword)
        d = b[1].strip()
        date_fromFile = d
    try: # DD-MM-YYYY        
        date_fromFile = datetime.strptime(d, "%m/%d/%Y") #use cme 
    except ValueError:
        # try another format
        try:
            date_fromFile = datetime.strptime(d, '%d %B %Y') # used LME
            # d.strftime("%A %d. %B %Y")
            # 'Monday 11. March 2002'
        except ValueError:
            try:
                date_fromFile = datetime.strptime(d, '%d %b %Y') # LME gold 01 Apr
                # print (datetime.strptime(date_str, "%m-%d"))
            except ValueError:
                try:
                    # date_fromFile = datetime.strptime(d, '%Y年%m月%d日')  
                    date_fromFile = datetime.strptime(d, '%b.%d,%Y')  #Date:Mar.05,2021
                except ValueError:                
                    print('9999')
                    return d
    return date_fromFile.strftime('%Y-%m-%d')
# dateStr = 'Data valid for 500 April 2021 '
# keyword = ''
# a = getDateFromString(dateStr, keyword)  
# print(a) 
def webpage_table_13F_sina2(saveDir):   
    # file_object = open('./sample.txt', 'a', encoding = 'utf-16')
    cols = ['Date', "Ticker", "Industry","NumOfHolder","ShareM", 
            "QoQ","MarketValue_100M","Ratio_InstitutionHolding"]
    df = pd.DataFrame(columns = cols)  
    
    url = 'http://global.finance.sina.com.cn/clues/13f/?nav13f_id=SymbolStats'    
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(15)
    dateStr = '2016-03-31'
    
    nextButton = driver.find_element_by_id("next")
    
    for page in range(10):
        print ("downloading page: " + str(page+1) )
        webObj2 = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr")
        numRows = len(webObj2)
        # webObj = driver.find_element_by_xpath("//*[@id= 'SymbolStats']/tbody/tr[1]/td")
        webObj = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr[1]/td")
        numCols = len(webObj)
        
        for row in range (numRows):
            # print ('downloading row: ' + str(row+1) )
            pathStr = "//table[@id= 'SymbolStats']/tbody/tr[" + str(row+1) + "]/td" 
            currentRow = driver.find_elements_by_xpath(pathStr)
            
            li = [dateStr]
            for col in range (2, numCols-2):
                li.append(currentRow[col].text)
            # print (li)
            df1 = pd.DataFrame([li], columns = cols) 
            df = df.append(df1, ignore_index=True)
            
        nextButton.click()
        time.sleep(4)    
    driver.quit()
    
    csvFileFullPath = saveDir +'/' +  dateStr + '_SEC_13F_sina_Q.csv'   
    df.to_csv(csvFileFullPath, index= False) 
    print('SEC_13F_sina downloaded: ' + csvFileFullPath)
    return csvFileFullPath
saveDir = dir_SEC_13F_sina
webpage_table_13F_sina2(saveDir)  

def webpage_table_13F_sina(saveDir):   
    # file_object = open('./sample.txt', 'a', encoding = 'utf-16')
    cols = ['Date', "Ticker", "Industry","NumOfHolder","ShareM", 
            "QoQ","MarketValue_100M","Ratio_InstitutionHolding"]
    df = pd.DataFrame(columns = cols)  
    
    url = 'http://global.finance.sina.com.cn/clues/13f/?nav13f_id=SymbolStats'    
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    nextButton = driver.find_element_by_id("next")
    dateStr = constA.todayDate_str
    
    for page in range(100):
        print ("downloading page: " + str(page) )
        webObj2 = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr")
        numRows = len(webObj2)
        # webObj = driver.find_element_by_xpath("//*[@id= 'SymbolStats']/tbody/tr[1]/td")
        webObj = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr[1]/td")
        numCols = len(webObj)
        
        for row in range (numRows):
            print ('downloading row: ' + str(row) )
            pathStr = "//table[@id= 'SymbolStats']/tbody/tr[" + str(row+1) + "]/td" 
            currentRow = driver.find_elements_by_xpath(pathStr)
            
            li = [dateStr]
            for col in range (2, numCols-2):
                li.append(currentRow[col].text)
            # print (li)
            df1 = pd.DataFrame([li], columns = cols) 
            df = df.append(df1, ignore_index=True)
            
        nextButton.click()
        time.sleep(4)    
    driver.quit()
    
    csvFileFullPath = saveDir +'/' +  dateStr + '_SEC_13F_sina_Q.csv'   
    df.to_csv(csvFileFullPath, index= False) 
    print('SEC_13F_sina downloaded: ' + csvFileFullPath)
    return csvFileFullPath
# saveDir = dir_SEC_13F_sina
# webpage_table_13F_sina(saveDir)    
# df = pd.read_csv('./sample.txt', sep=" ", header = None, encoding = 'utf-16')    
print ()




def webpage_sina_13F(save_toDataDir, comexWebsite_List):
    makeTodayDataDir(save_toDataDir) 
    
    fileAbsPath = os.path.abspath(save_toDataDir)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    prefs = {"download.default_directory" : winPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': False,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30)     
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver.exe', options = chromeOptions)  # Optional argument, if not specified will search path.
    time.sleep(1) 
    
    for i in range(len(comexWebsite_List)): 
        url = comexWebsite_List[i][1]      
        driver.get(url)
        time.sleep(1)
        
    driver.quit()
    time.sleep(1)









def sql_dailyStock_comex(sourceFillFullpath):    
    df = pd.read_csv(sourceFillFullpath)    
    # df[ ['Registered', 'Pledged','Eligible', 'Total'] ] =  df[ ['Registered', 'Pledged','Eligible', 'Total'] ].astype(float)
    df = df.replace({np.NAN: None})
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]
        futureStr = row[1]         
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" % (_sqlTable_COMEX_stock, dateStr, futureStr)
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,? );""" %(_sqlTable_COMEX_stock)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
# sourceFillFullpath = "./data/NYMEXCOMEX/temp/2021-03-29/2021-03-26_Aluminum_Stocks.csv"
# sql_dailyStock_comex(sourceFillFullpath)          


def extract_excelFile_comex(sourceFillpath):
    print (sourceFillpath)
    filePath = constA.getFilePathInfo(sourceFillpath, 0)
    fileName = constA.getFilePathInfo(sourceFillpath, 2)   
    
    if  constCOMEX_A.goldKey.lower()      in sourceFillpath.lower():
        future = 'Gold'        
    elif constCOMEX_A.goldKiloKey.lower()  in sourceFillpath.lower():
        future = 'GoldKilo'        
    elif constCOMEX_A.silverKey.lower()    in sourceFillpath.lower():
        future = 'Silver'        
    elif constCOMEX_A.cuKey.lower()        in sourceFillpath.lower():
        future = 'Copper'        
    elif constCOMEX_A.PAPLKey.lower()      in sourceFillpath.lower():
        future = 'PA'
        future = 'PA'        
    elif constCOMEX_A.alKey.lower()        in sourceFillpath.lower():
        future = 'Aluminum'        
    elif constCOMEX_A.znKey.lower()        in sourceFillpath.lower():
        future = 'Zinc'        
    elif constCOMEX_A.pbKey.lower()        in sourceFillpath.lower(): 
        future = 'Lead'
    else:
        future = 'na'
    
    df = pd.read_excel(sourceFillpath)    
    #------get the file date
    dateCol = df[df.columns[6]]    
    for c in dateCol:
        if 'activity date' in str(c).lower() :
            dateStr = getDateFromString(c, ':')
            break
    # --- get the data 
    for i in range(len(df)):
        if 'total registered' in str(df.iloc[i,0]).lower():
            row_register = df.iloc[i]
            row_register1 = df.iloc[i+1]
            row_register2 = df.iloc[i+2]
            row_register3 = df.iloc[i+3]
            break

    for i in reversed(range (row_register.size)):
        # print (row_register[i])
        if not pd.isnull(row_register[i]):
            print (row_register[i])
            lastCellNum = i          
            break
        
    if 'total pledged' in str(row_register1).lower(): 
        registered =  row_register[lastCellNum]       
        pledged  =  row_register1[lastCellNum]
        eligible =  row_register2[lastCellNum] 
        total    =  row_register3[lastCellNum]        
    else:
        registered =  row_register[lastCellNum]
        pledged  = None
        eligible =  row_register1[lastCellNum] 
        total    =  row_register2[lastCellNum]        


    d = {'Date' : [dateStr], 'Future' : [future], 'Registered': [registered], 'Pledged': [pledged], 'Eligible' : [eligible], 'Total':[total]}
    df_data = pd.DataFrame(data = d)
    
    fillFullPath = filePath + '/' + dateStr + '_' +fileName + '.csv' 
    df_data.set_index('Date', inplace = True)
    df_data.to_csv(fillFullPath, float_format='%.3f')
    return fillFullPath     

# sourceFillpath = "./data/NYMEXCOMEX/temp/2021-03-29/Copper_Stocks.xls"
# extract_excelFile_comex(sourceFillpath)    

def sql_daily_OIshortLongPositon_comex(sourceFillFullpath, dbName):    
    df = pd.read_csv(sourceFillFullpath)    
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,34)
    print("sql insert file data: " + sourceFillFullpath)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' and [ForwardMonth] ='%s' ;""" \
                % (dbName, row[0], row[1], row[2])
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?);""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
# sourceFillFullpath = "./data/CME_deliveryReport/OI_shortLongPositionReport/2021-05-11/2021-05-10_OpentInterest_shortLongPosition_NonDeliverable.csv"
# dbName = _sqlTable_COMEX_Daily_Report_OpenInterest_LongShortPositon
# sql_daily_OIshortLongPositon_comex(sourceFillFullpath, dbName)  


def extract_OIshortLongPositon_File(sourceFillpath):
    print (sourceFillpath)
    col = ['Contract','ForwardMonth','LongQty','ShortQty']
    df = pd.read_csv(sourceFillpath, names=col )
    df1 = df.dropna(how='all')
    df2 = df1.dropna(axis = 1, how='all')  
    #----get the date object and string
    dateObj = (pd.to_datetime(df2.iat[0,1], format = '%Y%m%d'))
    dateStr = dateObj.strftime('%Y-%m-%d')
    
    df_data = df2.iloc[3:-1]
    df_data['ForwardMonth'] = pd.to_datetime(df_data['ForwardMonth'], format = '%Y%m')

    df_data.insert(0, 'Date', dateObj)    
    
    filePath = constA.getFilePathInfo(sourceFillpath, 0)
    fileName = constA.getFilePathInfo(sourceFillpath, 2)      
    fillFullPath = filePath + '/' + dateStr + '_' +fileName + '.csv' 
    # df_data.to_csv(fillFullPath, float_format='%.3f')
    df_data.to_csv(fillFullPath, index = False)
    return fillFullPath     

# sourceFillpath = "./data/CME_deliveryReport/OI_shortLongPositionReport/2021-05-10/position-offset-report-deliverable-product (1).csv"
# sourceFillpath = "./data/CME_deliveryReport/OI_shortLongPositionReport/2021-05-11/OpentInterest_shortLongPosition_NonDeliverable.xls"
# extract_OIshortLongPositon_File(sourceFillpath) 
# print()

#---------extract file -------------
def extract_sql_StockData_COMX_Folders(sourceDir):
    pathlist = Path(sourceDir).glob('**/*.xls')
    for path in pathlist:
         sourceFillpath = str(path)  
         csvOutPutFilePath = extract_excelFile_comex(sourceFillpath)
         #---sql to db
         sourceFillFullpath = csvOutPutFilePath
         sql_dailyStock_comex(sourceFillFullpath)        
# sourceDir = "./data/NYMEXCOMEX/temp"    
#extract_sql_StockData_COMX_Folders(sourceDir)

def extract_sql_OIshortLongPositon_Folder(sourceDir, dbName):
    # pathlist = Path(sourceDir).glob('**/*.xls')
    pathlist = Path(sourceDir).glob('**/*.*')
    for path in pathlist:
         sourceFillpath = str(path)         
         csvOutPutFilePath = extract_OIshortLongPositon_File(sourceFillpath)
         
         #---sql to db
         sourceFillFullpath = csvOutPutFilePath         
         sql_daily_OIshortLongPositon_comex(sourceFillFullpath, dbName)
# sourceDir = constCOMEX_A.CME_positionOffsetReport_dir + '/2021-05-11'
# dbName = _sqlTable_COMEX_Daily_Report_OpenInterest_LongShortPositon
# extract_sql_OIshortLongPositon_Folder(sourceDir, dbName)

#-------donwload files-------------------------------
def downloadExcelFile(targetDir, fileName, webAddress):
    makeTodayDataDir(targetDir)    
    newFilefullPath = targetDir + '/' + fileName
    
    if os.path.isfile(newFilefullPath):
        os.remove(newFilefullPath)
        print('file removed: ' + newFilefullPath)
    
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    # reg_url = url
    req = Request(url = webAddress, headers = headers) 
    html = urlopen(req, timeout= 5).read()  
    with open(newFilefullPath, 'wb') as outfile:
        outfile.write(html)   
    
    print('Downloaded COMEX daily Stock: ' + newFilefullPath)
    # r = requests.get(url, allow_redirects=True)
    # with open(newFilefullPath, 'wb') as output:
    #     output.write(r.content)    
    # open('test5.xls', 'wb').write(r.content)
    
    # f = open(newFilefullPath, 'wb')  
    # f.write(r.content)
    # f.close()

def download_webpageReport_Files(save_toDataDir, comexWebsite_List):
    makeTodayDataDir(save_toDataDir)    
    for i in range(len(comexWebsite_List)): 
        filename = comexWebsite_List[i][0] + ".xls"         
        targetDir = save_toDataDir
        fileName = filename
        webAddress = comexWebsite_List[i][1]        
        downloadExcelFile(targetDir, fileName, webAddress)   

def downloadExcelFile_2(targetDir, url):
    prefs = {"download.default_directory" : targetDir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': False,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30)     
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver.exe', chrome_options = chromeOptions)  # Optional argument, if not specified will search path.
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    driver.quit()
    time.sleep(1)       
# url = "http://www.cmegroup.com/delivery_reports/Gold_Stocks.xls"
# targetDir = 'G:\\test.xls'
# downloadExcelFile_2(url, downloadDir)

def download_webpageReport_Files_2(save_toDataDir, comexWebsite_List):
    makeTodayDataDir(save_toDataDir) 
    
    fileAbsPath = os.path.abspath(save_toDataDir)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    prefs = {"download.default_directory" : winPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': False,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30)     
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver.exe', options = chromeOptions)  # Optional argument, if not specified will search path.
    time.sleep(1) 
    
    for i in range(len(comexWebsite_List)): 
        url = comexWebsite_List[i][1]      
        driver.get(url)
        time.sleep(1)
        
    driver.quit()
    time.sleep(1)
        

def COMEX_gainStock_Tuesday_weekly_Run():
    save_toDataDir = constCOMEX_A.CME_gainStock_Tuesday_dir + '/' + constA.todayDate_str
    comexWebsite_List =  constCOMEX_A.comexWebsite_gainStock_Tuesday_List
    download_webpageReport_Files_2(save_toDataDir, comexWebsite_List)
# COMEX_gainStock_Tuesday_weekly_Run()

def COMEX_bondsFuture_Delivered_Q_Run():
    save_toDataDir = constCOMEX_A.CME_bonds_dilivered_Q + '/' + constA.todayDate_str
    comexWebsite_List =  constCOMEX_A.comexWebsite_bondsDelivered_Q_List
    download_webpageReport_Files_2(save_toDataDir, comexWebsite_List)
# COMEX_bondsFuture_Delivered_Q_Run()


#-----COMEX_daily_Run()-------
def COMEX_daily_Run():
    save_toDataDir = constCOMEX_A.commodityNYMEXCOMEX_fileDir + '/' + constA.todayDate_str
    comexWebsite_List =  constCOMEX_A.comexWebsite_StockList
    # download_webpageReport_Files(save_toDataDir, comexWebsite_List)
    download_webpageReport_Files_2(save_toDataDir, comexWebsite_List)


    save_toDataDir_OIshortLongPositon = constCOMEX_A.CME_positionOffsetReport_dir + '/' + constA.todayDate_str
    comexWebsite_OIshortLongPosition_List =  constCOMEX_A.comexWebsite_OI_shortLongPosition_List
    # download_webpageReport_Files(save_toDataDir_OIshortLongPositon, comexWebsite_OIshortLongPosition_List)
    download_webpageReport_Files_2(save_toDataDir_OIshortLongPositon, comexWebsite_OIshortLongPosition_List)
    #------------extra informaiton save to csv file
    sourceDir = save_toDataDir
    extract_sql_StockData_COMX_Folders(sourceDir)  
    
    sourceDir = save_toDataDir_OIshortLongPositon
    dbName = _sqlTable_COMEX_Daily_Report_OpenInterest_LongShortPositon
    extract_sql_OIshortLongPositon_Folder(sourceDir, dbName)
    
# COMEX_daily_Run()
















