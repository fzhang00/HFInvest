# -*- coding: utf-8 -*-
"""
Created on Thu May 13 23:06:23 2021

@author: haoli
"""
import sys
sys.path.append("../")

import pandas as pd
from datetime import datetime
import pyodbc
import numpy as np

import win32com.client
import os
import ntpath
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import pandas_datareader as web
import datetime as dt


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'Sentiment'     
pd.set_option('mode.chained_assignment', None)

#-----------------------------------------------
# _dir_sp500_ratio = './ratio/'
_dir_history = './history/'

#----------------

_sqlTable_AAII_SentimentSurvey = 'AAII_SentimentSurvey'
_sqlTable_Michigan_ConsumerSurvey = 'Michigan_ConsumerSurvey'

url_IndexConsumerSentiment= 'http://www.sca.isr.umich.edu/files/chicsr.xls'
url_CurrentEconomicConditionsIndex = 'http://www.sca.isr.umich.edu/files/chiccr.xls'
url_IndexConsumerExpectations = 'http://www.sca.isr.umich.edu/files/chicer.xls'
url_ExpectedChangesPricesNextYear ='http://www.sca.isr.umich.edu/files/chpx1r.xls'

_dir_aaii_excel_filePath = './AAII/sentiment.xls'

#--------------------
def sql_Date_Name_Value(dbName, df):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Survey] = '%s' ;""" % (dbName, dateStr, row[1])
        cursor.execute(query)         
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close()
# file = './history/' + 'Current Economic Conditions Index.csv'
# file = './history/' + 'Index of Consumer Expectations.csv'
# file = './history/' + 'Index of Consumer Sentiment.csv'
# file = './history/' + 'Inflation Expectation.csv'
# df = pd.read_csv(file)
# dbName = _sqlTable_Michigan_ConsumerSurvey
# sql_Date_Name_Value(dbName, df)


def webpage_ConsumerSurvey_Michigan():   
    url = 'http://www.sca.isr.umich.edu/'
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(2)
    tables = pd.read_html(driver.page_source)
    driver.quit()
    
    df1 = tables[0]
    df1_a = df1.iloc[2:, [0,1]]
    df1_b = df1.iloc[2:, [0,2]]
    str_date_a = df1.iloc[0,1]+ df1.iloc[1,1]
    str_date_b = df1.iloc[0,2]+ df1.iloc[1,2]
    # df1_a.reset_index(inplace = False)
    # df1_b.reset_index(inplace = False)    
    df1_a.insert(0, "Date", (pd.to_datetime(str_date_a , format='%b%Y') ).strftime('%Y-%m-%d'))
    df1_b.insert(0, "Date", (pd.to_datetime(str_date_b , format='%b%Y') ).strftime('%Y-%m-%d'))
    df1_a.columns = range(df1_a.columns.size)
    df1_b.columns = range(df1_b.columns.size)
    # df_a = df1_a.copy()
    # df_b = df1_a.copy()
    dbName = _sqlTable_Michigan_ConsumerSurvey
    sql_Date_Name_Value(dbName, df1_a)
    sql_Date_Name_Value(dbName, df1_b)
    print("ConsumerSurvey Michigan downlaoded, sql") 
    
# webpage_ConsumerSurvey_Michigan()
# print()
#--------AAII ------------------------------

def sql_AAII(dbName, df):
    df = df.replace({np.NAN: None})
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        # if row[1] is None: #if pandas.isnull(pandas.NaT  row[0])
        if pd.isnull(row[0]):
            print("AAII sql completed.")
            break
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s';""" % (dbName, dateStr)
        cursor.execute(query)         
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?, ?,?,?,  ?,?,?,?,?,? ,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close()

def AAII_excel():
    # rowSkip = 7 
    rowSkip = 1500
    rowfooterSkip = 1700
    df = pd.read_excel(_dir_aaii_excel_filePath, skiprows = rowSkip, skipfooter=rowfooterSkip)  
    df.columns = range(df.columns.size)
    df = df.round(4)
    dbName = _sqlTable_AAII_SentimentSurvey
    sql_AAII(dbName, df)
    print()

# AAII_excel()

def webpage_sentiment_AAII():   
    # options = Options()
    # options.add_argument(f'user-agent=Chrome/98.0.4758.82')
    url = 'https://www.aaii.com/sentimentsurvey/sent_results'
    driver = webdriver.Chrome(executable_path='../chromedriver.exe')
    # driver = webdriver.Ie(executable_path='../IEDriverServer.exe')
    # driver.delete_all_cookies()
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(2)
    tables = pd.read_html(driver.page_source)
    
    
    dfx = tables[0]
    df1 = dfx.iloc[1:]
    # df1.iloc[:,0] = df1.iloc[:,0].str.replace(':', "")
    df1.iloc[:,0] = df1.iloc[:,0] + datetime.today().strftime('%Y')
    try: # DD-MM-YYYY        
        df1.iloc[:,0] = (pd.to_datetime(df1.iloc[:,0] , format='%B %d:%Y')) #.strftime('%Y-%m-%d')
    except ValueError:
        print ("-- Error: date convert error.  sp500 sector market weight ")  
        return
    
    for i in range(len(df1)):
        if df1.iloc[i, 0] <= datetime.today():
            df1.iloc[i, 0] = df1.iloc[i,0].strftime('%Y-%m-%d')
        else:
            df1.iloc[i, 0] = (df1.iloc[i,0] - pd.DateOffset(years = 1)).strftime('%Y-%m-%d')
        df1.iloc[i, 0] = df1.iloc[i, 0].replace('%',"")        
    
    driver.quit()
    #---------database------------------
    dbName = _sqlTable_AAII_SentimentSurvey
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df1.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where [Date] = '%s' ;""" % (dbName, dateStr)
        cursor.execute(query)         
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()         
    cursor.close()
    cnxn.close()    
    print("SP500 sector weight downlaoded, sql")    
# webpage_sentiment_AAII()
# print()



# def downloadExcelFile(targetDir, fileName, url):
#     # makeTodayDataDir(targetDir)    
#     newFilefullPath = targetDir + '/' + fileName
    
#     if os.path.isfile(newFilefullPath): 
#         print ("Trader Report file exist: " + newFilefullPath)
#         return "na" # file exist do nothing
#         # os.remove(newFilefullPath)
#         # print('file removed: ' + newFilefullPath)    
    
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
#     req = Request(url = url, headers = headers) 
#     html = urlopen(req).read()  
#     with open(newFilefullPath, 'wb') as outfile:
#         outfile.write(html)
    
#     # fileSize = os.stat(newFilefullPath).st_size    
#     # if fileSize < 1000: # 1k
#     #     msg = "Excel file download data <1K: " + newFilefullPath + " ; url: " + url 
#     #     mydownPy.logError(errorFileTargetDir, msg)
#     # else: # save, update the data
#     #     print('Downloaded weekly trader report: ' + newFilefullPath)        
#     return newFilefullPath 


# # url_aaii_excel = 'https://www.aaii.com/files/surveys/sentiment.xls'
# url = 'https://www.aaii.com/files/surveys/sentiment.xls' 
# # url = 'https://www.aaii.com/sentimentsurvey/sent_results'

# driver = webdriver.Ie(executable_path='../IEDriverServer.exe')
# # driver.delete_all_cookies()
# driver.implicitly_wait(10)    
# driver.get(url)



# print()
# df = pd.read_csv(url_aaii_excel) https://www.aaii.com/files/surveys/sentiment.xls

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
# # reg_url = url
# req = Request(url = url, headers = headers) 
# html = urlopen(req).read()  
# with open('test.xls', 'wb') as outfile:
#     outfile.write(html)  


# # data_url = "http://www.eia.gov/dnav/pet/xls/PET_PRI_ALLMG_A_EPM0_PTC_DPGAL_M.xls"
# import urllib2
# import urllib, StringIO
# xld = urllib2.urlopen(url).read()
# xlds = StringIO.StringIO(xld)
# data = pd.read_excel(xlds, "Data 1", skiprows=2)

# import urllib
# # dls = "http://www.muellerindustries.com/uploads/pdf/UW SPD0114.xls"
# # urllib.request.urlretrieve(url, "test.xls") 
# hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
#             "X-Requested-With": "XMLHttpRequest"} #change the version of the browser accordingly

# resp = requests.get(url, headers = hdr)

# pd.read_excel(resp.content, error_bad_lines=False)

# r = requests.get(url)
# open('temp.xls', 'wb').write(r.content )
# df = pd.read_excel('temp.xls')

# r = requests.get(url_aaii_excel) # my_cookies are imported from a selenium session.
# df = pd.io.excel.read_excel(r.content)

# local_path = './history/' + 'aaii.xls'
# newFilefullPath =  './history/' + 'aaii.xls'
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
# req = Request(url = url_aaii_excel, headers = headers) 
# html = urlopen(req).read()  
# with open(newFilefullPath, 'wb') as outfile:
#     outfile.write(html)
# r = requests.get(url)
# open('./temp.xls', 'wb').write(r.content)
# df = pd.read_excel('temp.xls')

# get_content = requests.get(url_aaii_excel).content
# import io
# df = pd.read_csv(io.StringIO(get_content.decode('utf-8')))

# resp = requests.get(url_aaii_excel)
# with open(local_path, 'wb') as output:
#     output.write(resp.content)
# df = pd.read_excel(local_path)

# s=requests.get(url_aaii_excel).content
# df_deathsAges = pd.read_excel(io.BytesIO(s),  engine="openpyxl")

# print()
 
    


# def sp500_closePrice():  
#     today = datetime.today()
#     todayOffset2 = today - dt.timedelta(14)
#     # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
#     raw_data = web.DataReader('^GSPC', 'yahoo', todayOffset2, today, api_key=None)
#     raw_data.reset_index(inplace=True)
#     dbName = _sqlTable_SP500_ClosePrice
#     # df=pd.read_excel("./ratio/IndexPrice.xlsx") 
#     df = pd.DataFrame()
#     df = raw_data[['Date','Close']]
#     df['Close'] = df['Close'].round(2)
#     sql_Date_Value(dbName, df)
#     print("SP500 close price downlaoded, sql")

# def sp500_closePrice_volume():  
#     today = datetime.today()
#     # todayOffset2 = today - dt.timedelta(5)
#     todayOffset2 = datetime(1970, 1, 5)
#     # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
#     raw_data = web.DataReader('^GSPC', 'yahoo', todayOffset2, today, api_key=None)
#     raw_data.reset_index(inplace=True)
#     raw_data = raw_data.round(2)    
#     saveFileFullPath = _dir_sp500_value + 'SP500_History.csv'
#     raw_data.to_csv(saveFileFullPath, index = False)    
# sp500_closePrice_volume()

# def sector_Price_Volume():
#     today = datetime.today()
#     todayOffset2 = today - dt.timedelta(7)
#     # todayOffset2 = datetime(1993, 5, 3)
    
#     s5TELS = web.DataReader('^SP500-50', 'yahoo', todayOffset2, today, api_key=None)
#     s5COND = web.DataReader('^SP500-25', 'yahoo', todayOffset2, today, api_key=None)
#     s5CONS = web.DataReader('^SP500-30', 'yahoo', todayOffset2, today, api_key=None)

#     sPN     = web.DataReader('^GSPE', 'yahoo', todayOffset2, today, api_key=None)    
#     sPF     = web.DataReader('^SP500-40', 'yahoo', todayOffset2, today, api_key=None)
#     s5HLTH = web.DataReader('^SP500-35', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5INDU = web.DataReader('^SP500-20', 'yahoo', todayOffset2, today, api_key=None)
#     s5INFT = web.DataReader('^SP500-45', 'yahoo', todayOffset2, today, api_key=None)
#     s5MATR = web.DataReader('^SP500-15', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5UTIL = web.DataReader('^SP500-55', 'yahoo', todayOffset2, today, api_key=None)    
#     s5REAS = web.DataReader('^SP500-60', 'yahoo', todayOffset2, today, api_key=None)

#     s5TELS['Sector'] = 's5TELS'
#     s5COND['Sector'] = 's5COND'
#     s5CONS['Sector'] = 's5CONS'
#     sPN['Sector']  ='sPN'
#     sPF['Sector']  ='sPF'
#     s5HLTH['Sector'] = 's5HLTH'
#     s5INDU['Sector'] = 's5INDU'
#     s5INFT['Sector'] = 's5INFT'
#     s5MATR['Sector'] = 's5MATR'
#     s5UTIL['Sector'] = 's5UTIL'   
#     s5REAS['Sector'] = 's5REAS'
       
#     dfx =[s5TELS[['Sector','Close','Volume']],    s5COND[['Sector','Close','Volume']],  s5CONS[['Sector','Close','Volume']], 
#           sPN[['Sector','Close','Volume']],       sPF[['Sector','Close','Volume']],     s5HLTH[['Sector','Close','Volume']],
#           s5INDU[['Sector','Close','Volume']],    s5INFT[['Sector','Close','Volume']],  s5MATR[['Sector','Close','Volume']],
#           s5UTIL[['Sector','Close','Volume']],    s5REAS[['Sector','Close','Volume']]           ] 
#     df = pd.concat(dfx)  #df = pd.concat(dfx, axis=1)
#     df.reset_index(inplace=True)

#     df = df.round(2).replace({np.NAN: None}) 
#     df =df.sort_values(by= df.columns[0], ascending = True)    
#     # saveFileFullPath = _dir_sp500_value + 'sector_Price_Volume.csv'
#     # # df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
#     # df.to_csv(saveFileFullPath, index = False)
    
#     dbName = _sqlTable_SP500_Sector_PriceVolume
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#     cursor = cnxn.cursor()      
#     for index, row in df.iterrows():
#         dateStr = row[0]     
#         query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s';""" % (dbName, dateStr, row[1])
#         cursor.execute(query)         
#         params = tuple(row)
#         query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
#         cursor.execute(query, params) 
#         cnxn.commit()
#         # break            
#     cursor.close()
#     cnxn.close()     
#     print("SP500 11 sectors - close price and volume downlaoded, sql") 
# # sector_Price_Volume()
# # print()  




# def webpage_SP500_marketCap_Industry():   
#     url = 'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml'       
#     driver = webdriver.Chrome('../chromedriver.exe')
#     driver.implicitly_wait(10)    
#     driver.get(url)
#     time.sleep(2)
    
#     # driver.find_element_by_class_name("collapse-all").click()
#     # time.sleep(3)
#     tables_sector = pd.read_html(driver.page_source)
#     if len(tables_sector) == 2 and len(tables_sector[0] == 12):
#         pass
#     else:
#         driver.get(url)
#         time.sleep(2)
#         tables_sector = pd.read_html(driver.page_source)
#         if len(tables_sector) == 2 and len(tables_sector[0] == 12):
#             pass
#         else:            
#             print ("Error:  check the websize of SP500 market Cap -  sectors and industry")
#             return
#     #-----------get date from the header
#     df = tables_sector[0]
#     d1 = (df.columns.values.tolist())[1]
#     dd= (d1.lower()).split(('et'))[1]
    
#     dateStr = ''
#     try: # DD-MM-YYYY        
#         dateStr = (pd.to_datetime(dd.strip() , format='%m/%d/%Y')).strftime('%Y-%m-%d')
#     except ValueError:
#         print ("-- Error: date convert error.  sp500 sector and industry market cap ")         
        
#     #---get the sector name and market cap
#     df1 = tables_sector[0]
#     df2 = (df1[df1.columns[0]]).str.split('details', expand=True)
#     df1[df1.columns[0]] = df2[df2.columns[1]].str.lower().str.replace('industries',"").str.strip()
    
#     df_sector = df1[ [df1.columns[0], df1.columns[2] ]]
    
#     driver.find_element_by_class_name("expand-all").click()
#     time.sleep(2)
#     tables_industry = pd.read_html(driver.page_source)
    
#     df = pd.DataFrame()
#     # df_industry = pd.DataFrame()
#     for i in range(len(df_sector) ):
#         dfx = tables_industry[i+1]
#         df_industry = dfx[ [dfx.columns[0], dfx.columns[2] ]]
#         pass
#         # dfx1 = df_industry.append([df_sector.iat[i, 0] ,  df_sector.iat[i, 1])] , ignore_index = True)
#         df_industry.loc[-1] = df_sector.loc[i].values.tolist() #df_sector.loc[i]
#         # df_industry.reset_index(inplace=True)
        
#         df_industry.insert(0, "Sector", df_sector.iloc[i,0])# add the sector name col        
#         df = pd.concat([ df,df_industry ])
#         i +=1
#         if i == 11:
#             break
#     df.insert(0, 'Date', dateStr)
#     # df.reset_index(inplace=True) '$': '', 
#     df.reset_index(drop = True, inplace=True)

#     df[df.columns[3]] = (df[df.columns[3]]).str.replace('[$,B]', '')
#     df[df.columns[3]] = (df[df.columns[3]]).str.replace('T', '*1e3')
#     df[df.columns[3]] = pd.eval(df[df.columns[3]])    
    
#     saveFileFullPath = _dir_sp500_SectorWeight + datetime.today().strftime('%Y') + '-Industry MarketCapital.csv'
#     df.to_csv(saveFileFullPath, mode='a', index = False, header=False)    

#     driver.quit()
    
#     #---------database------------------
#     saveFileFullPath_temp = _dir_sp500_SectorWeight + 'temp Industry MarketCapital.csv'
#     df.to_csv(saveFileFullPath_temp, index= False)
#     df = pd.read_csv(saveFileFullPath_temp)
    
#     dbName = _sqlTable_SP500_Sector_Industry_MarketCap
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#     cursor = cnxn.cursor()      
#     for index, row in df.iterrows():
#         # dateStr = row[0]     
#         query = """DELETE FROM %s where [Date] = '%s' and [Sector] = '%s' and [Industry] = '%s' ;""" % (dbName, row[0] , row[1], row[2])
#         # query = """DELETE FROM %s where [Date] = '%s' and [Sector] = '%s' ;""" % (dbName, row[0] , row[1])        
#         cursor.execute(query)         
#         # params = tuple([row[0],row[1],row[2],row[3]])
#         params = tuple(row)
#         query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
#         cursor.execute(query, params) 
#         cnxn.commit()
#         # break            
#     cursor.close()
#     cnxn.close()    
#     print("SP500 sector-Industry market cap downlaoded, sql")  
    
# # webpage_SP500_marketCap_Industry()
# # print()       
# #-------------------------------------------

# #------------------------------------------------ 

# #------------------------------------------
# def sp500_daily_run_PE():  
#     if datetime.today().weekday() == 6:
#         return
#         #-----------Sector-----------------
#     elif datetime.today().weekday() == 5:
#         # guru_sp500_PE_shillerSector_daily()
#         pass
#     else: 
#         pass
#         # sp500_closePrice()
#         # sector_Price_Volume()
#         # webpage_SP500_marketWeight_Sector()
#         # webpage_SP500_marketCap_Industry()
    
# sp500_daily_run_PE()
# webpage_SP500_marketWeight_Sector()
