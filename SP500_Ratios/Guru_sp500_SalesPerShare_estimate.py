# -*- coding: utf-8 -*-
"""
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
import requests

from pathlib import Path


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SP500_Ratios'     


pd.set_option('mode.chained_assignment', None)


# url_PE_shiller_multpl = 'https://www.multpl.com/shiller-pe/table/by-month'
# url_Wilshire5000GDP = 'https://www.gurufocus.com/economic_indicators/60/ratio-of-wilshire-5000-over-gnp'


_sqlTable_SP500_SalesPerShare_Estimate = 'SP500_SalesPerShare_Estimate'


def sql_guru_OperatingEPS_estimate(df, dbName):
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,35) 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' ;""" % (dbName, dateStr, row[1])
        cursor.execute(query) 
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
def extract_allExcelFileSubFolders_toSql():
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    dbName = _sqlTable_SP500_SalesPerShare_Estimate
    sourceDir = './SalesPerShare'
    pathlist = Path(sourceDir).glob('**/*.xlsx')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         df = pd.read_excel(excelFileFullPath)
         sql_guru_OperatingEPS_estimate(df, dbName)
# extract_allExcelFileSubFolders_toSql()
# print()
#-------------------------------------

def sp500_SalesPerShare_estimate(url, sectorName):    
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }    
    r = requests.get(url, headers=header)    
    tables = pd.read_html(r.text)
    df = tables[0]
    df[df.columns[2]] = df[df.columns[2]].str.replace("%","")
    df.insert(1, 'Sector', sectorName)
    print("sp500 Sales per share estimate:  " + sectorName)
    return df


def sp500_SalesPerShare_estimate_monthly_Q():   
    dbName = _sqlTable_SP500_SalesPerShare_Estimate
    
    url_Total = 'https://www.gurufocus.com/economic_indicators/101/sp-500-sales-per-share'
    sectorName_Total = "Total"
    df_Total = sp500_SalesPerShare_estimate(url_Total, sectorName_Total)
    sql_guru_OperatingEPS_estimate(df_Total, dbName)     

    url_CommunicationServices = 'https://www.gurufocus.com/economic_indicators/4222/sp-500-sales-per-share-communication-services'
    sectorName = "CommunicationServices"
    df = sp500_SalesPerShare_estimate(url_CommunicationServices, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Energy = 'https://www.gurufocus.com/economic_indicators/4223/sp-500-sales-per-share-energy'
    sectorName = "Energy"
    df = sp500_SalesPerShare_estimate(url_Energy, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_Industrials  = 'https://www.gurufocus.com/economic_indicators/4224/sp-500-sales-per-share-industrials'
    sectorName = "Industrials"
    df = sp500_SalesPerShare_estimate(url_Industrials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_InformationTechnology = 'https://www.gurufocus.com/economic_indicators/4225/sp-500-sales-per-share-information-technology'
    sectorName = "InformationTechnology"
    df = sp500_SalesPerShare_estimate(url_InformationTechnology, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Utilities = 'https://www.gurufocus.com/economic_indicators/4221/sp-500-sales-per-share-utilities'
    sectorName = "Utilities"
    df = sp500_SalesPerShare_estimate(url_Utilities, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_HealthCare = 'https://www.gurufocus.com/economic_indicators/4220/sp-500-sales-per-share-health-care'
    sectorName = "HealthCare"
    df = sp500_SalesPerShare_estimate(url_HealthCare, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Materials  = 'https://www.gurufocus.com/economic_indicators/4215/sp-500-sales-per-share-materials'
    sectorName = "Materials"
    df = sp500_SalesPerShare_estimate(url_Materials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerDiscretionary = 'https://www.gurufocus.com/economic_indicators/4216/sp-500-sales-per-share-consumer-discretionary'
    sectorName = "ConsumerDiscretionary"
    df = sp500_SalesPerShare_estimate(url_ConsumerDiscretionary, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Financials = 'https://www.gurufocus.com/economic_indicators/4217/sp-500-sales-per-share-financials'
    sectorName = "Financials"
    df = sp500_SalesPerShare_estimate(url_Financials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_RealEstate = 'https://www.gurufocus.com/economic_indicators/4218/sp-500-sales-per-share-real-estate'
    sectorName = "RealEstate"
    df = sp500_SalesPerShare_estimate(url_RealEstate, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerStaples = 'https://www.gurufocus.com/economic_indicators/4219/sp-500-sales-per-share-consumer-staples'
    sectorName = "ConsumerStaples"
    df = sp500_SalesPerShare_estimate(url_ConsumerStaples, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)        
    
   
    
sp500_SalesPerShare_estimate_monthly_Q()

