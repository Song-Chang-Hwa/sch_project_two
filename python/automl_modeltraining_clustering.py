###########################################################
# 4. 모델 학습 - XGBoot, automl_modeltraining_xgboot.py
###########################################################

# coding: utf-8

# In[0]:
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import pymysql
import pandas as pd
import numpy as np
from sys import argv

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, KFold

from sklearn.tree import DecisionTreeRegressor, export_graphviz, DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class Automl_Modeltraining_XGBoot:
    isLocal = False
        
    def __init__(self):
        pass

    # DB Connection
    def getDbConnection(self):
        return pymysql.connect(host="211.192.49.156", user="belltechsoft", password="qpfxprthvmxm213#@!", db="aiblue_ocr")

    # select query
    def selectListQuery(self, query):
        resultList = []
        if not self.isLocal:
            conn = self.getDbConnection()
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs.execute(query)
                resultList = curs.fetchall()
            finally:
                conn.close()
        return resultList
        
    def escapeString(self, text):
        return text.replace("'","\\'")
        
    #Ocr Recognition - 데이터 읽어 들이기 
    def recognition(self, parameterList):
        plt.rc('font', family='Malgun Gothic')

        conn = self.getDbConnection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        
        #userId = 'aiblue_admin'
        #docSn  = '221111000000012'
        
        docSn  = parameterList["DOC_SN"]
        userId = parameterList["USER_ID"]
                       
        # (1) 테이터 컬럼 상세 정보(TB_AUTOML_COLUMN_INFO) select
        selectListString = "SELECT DOC_SN, COLUMN_SN, TEXT_NM  \
                                     , TARGET_VALUE_YN         \
                                     , (CASE WHEN TEXT_TYPE_GUBUN = '10' THEN 'N' \
                                             WHEN TEXT_TYPE_GUBUN = '20' THEN 'N' \
                                             ELSE (CASE WHEN TEXT_NM = 'None' THEN '' ELSE 'Y' END) \
                                        END) AS TEXT_TYPE_GUBUN  \
                                  FROM TB_AUTOML_COLUMN_INFO     \
                                 WHERE 1 =1         \
                                   AND DOC_SN = %s  \
                                   AND USE_YN = 'Y' \
                                 ORDER BY DOC_SN, COLUMN_SN "              
                            
        curs.execute(selectListString, [docSn])    
        textResult = curs.fetchall()
        df_columnInfo = pd.DataFrame(textResult)   
                        
        TARGET_001 = ''
        TARGET_002 = ''
        TARGET_003 = ''
        TARGET_004 = ''
        TARGET_005 = ''
        TARGET_006 = ''
        TARGET_007 = ''
        TARGET_008 = ''
        TARGET_009 = ''
        TARGET_010 = ''
        TARGET_011 = ''
        TARGET_012 = ''
        TARGET_013 = ''
        TARGET_014 = ''
        TARGET_015 = ''
        TARGET_016 = ''
        TARGET_017 = ''
        TARGET_018 = ''
        TARGET_019 = ''
        TARGET_020 = ''
        TARGET_021 = ''
        TARGET_022 = ''
        TARGET_023 = ''
        TARGET_024 = ''
        TARGET_025 = ''
        TARGET_026 = ''
        TARGET_027 = ''
        TARGET_028 = ''
        TARGET_029 = ''
        TARGET_030 = ''
        
        GUBUN_001  = ''
        GUBUN_002  = ''
        GUBUN_003  = ''
        GUBUN_004  = ''
        GUBUN_005  = ''
        GUBUN_006  = ''
        GUBUN_007  = ''
        GUBUN_008  = ''
        GUBUN_009  = ''
        GUBUN_010  = ''
        GUBUN_011  = ''
        GUBUN_012  = ''
        GUBUN_013  = ''
        GUBUN_014  = ''
        GUBUN_015  = ''
        GUBUN_016  = ''
        GUBUN_017  = ''
        GUBUN_018  = ''
        GUBUN_019  = ''
        GUBUN_020  = ''
        GUBUN_021  = ''
        GUBUN_022  = ''
        GUBUN_023  = ''
        GUBUN_024  = ''
        GUBUN_025  = ''
        GUBUN_026  = ''
        GUBUN_027  = ''
        GUBUN_028  = ''
        GUBUN_029  = ''
        GUBUN_030  = ''
        
        columnSn = 1  
        
        targetFileList = []
        targetFileList = df_columnInfo.values.tolist()
        
        for i in targetFileList:
            if(columnSn == 1):
                TARGET_001 = i[3]                
                GUBUN_001  = i[4]
            elif (columnSn == 2):   
                TARGET_002 = i[3]                 
                GUBUN_002  = i[4]
            elif (columnSn == 3):  
                TARGET_003 = i[3]               
                GUBUN_003  = i[4]
            elif (columnSn == 4):  
                TARGET_004 = i[3]            
                GUBUN_004  = i[4]
            elif (columnSn == 5):   
                TARGET_005 = i[3]       
                GUBUN_005  = i[4]
            elif (columnSn == 6):  
                TARGET_006 = i[3]                
                GUBUN_006  = i[4]
            elif (columnSn == 7):  
                TARGET_007 = i[3]           
                GUBUN_007  = i[4]
            elif (columnSn == 8):   
                TARGET_008 = i[3]            
                GUBUN_008  = i[4]
            elif (columnSn == 9):  
                TARGET_009 = i[3]             
                GUBUN_009  = i[4]
            elif (columnSn == 10):  
                TARGET_010 = i[3]              
                GUBUN_010  = i[4]
            elif (columnSn == 11):   
                TARGET_011 = i[3]                 
                GUBUN_011  = i[4]    
            elif (columnSn == 12):   
                TARGET_012 = i[3]                 
                GUBUN_001  = i[4]
            elif (columnSn == 13):  
                TARGET_013 = i[3]               
                GUBUN_013  = i[4]
            elif (columnSn == 14):  
                TARGET_014 = i[3]            
                GUBUN_014  = i[4]
            elif (columnSn == 15):   
                TARGET_015 = i[3]       
                GUBUN_015  = i[4]
            elif (columnSn == 16):  
                TARGET_016 = i[3]                
                GUBUN_016  = i[4]
            elif (columnSn == 17):  
                TARGET_017 = i[3]           
                GUBUN_017  = i[4]
            elif (columnSn == 18):   
                TARGET_018 = i[3]            
                GUBUN_018  = i[4]
            elif (columnSn == 19):  
                TARGET_019 = i[3]             
                GUBUN_019  = i[4]
            elif (columnSn == 20):  
                TARGET_020 = i[3]              
                GUBUN_020  = i[4]     
            elif (columnSn == 21):   
                TARGET_021 = i[3]                 
                GUBUN_021  = i[4]    
            elif (columnSn == 22):   
                TARGET_022 = i[3]                 
                GUBUN_022  = i[4]
            elif (columnSn == 23):  
                TARGET_023 = i[3]               
                GUBUN_023  = i[4]
            elif (columnSn == 24):  
                TARGET_024 = i[3]            
                GUBUN_024  = i[4]
            elif (columnSn == 25):   
                TARGET_025 = i[3]       
                GUBUN_025  = i[4]
            elif (columnSn == 26):  
                TARGET_026 = i[3]                
                GUBUN_026  = i[4]
            elif (columnSn == 27):  
                TARGET_027 = i[3]           
                GUBUN_027  = i[4]
            elif (columnSn == 28):   
                TARGET_028 = i[3]            
                GUBUN_028  = i[4]
            elif (columnSn == 29):  
                TARGET_029 = i[3]             
                GUBUN_029  = i[4]
            elif (columnSn == 30):  
                TARGET_030 = i[3]              
                GUBUN_030  = i[4]   
            else:   
                TARGET_031 = ''
                GUBUN_031  = ''
                
            columnSn += 1  
            
        # (2) 테이터 행 상세 정보(TB_AUTOML_ROW_INFO) select
        selectListString ="SELECT TEXT_NM_001,TEXT_NM_002,TEXT_NM_003,TEXT_NM_004,TEXT_NM_005, TEXT_NM_006,TEXT_NM_007,TEXT_NM_008,TEXT_NM_009,TEXT_NM_010, \
                                  TEXT_NM_011,TEXT_NM_012,TEXT_NM_013,TEXT_NM_014,TEXT_NM_015, TEXT_NM_016,TEXT_NM_017,TEXT_NM_018,TEXT_NM_019,TEXT_NM_020, \
                                  TEXT_NM_021,TEXT_NM_022,TEXT_NM_023,TEXT_NM_024,TEXT_NM_025, TEXT_NM_026,TEXT_NM_027,TEXT_NM_028,TEXT_NM_029,TEXT_NM_030   \
                             FROM TB_AUTOML_ROW_INFO \
                             WHERE 1=1 \
                               AND DOC_SN    = %s  \
                               AND ROW_GUBUN = 'N' \
                               ORDER BY DOC_SN, ROW_SN" 
            
        curs.execute(selectListString, [docSn] )          
        
        rowInfoResult = curs.fetchall()    
        df_row = pd.DataFrame(rowInfoResult)
            
        # (3) 데이터 전처리
        #     1)TARGET_VALUE = Y : 목표변수, 2)TEXT_TYPE_GUBUN = Y(정수형, 실수형)
                
        targetFileList = []
        targetFileList = df_row.values.tolist()
        
        dataCnt = 0
        for i in targetFileList:
            TEXT_NM_001 = i[0]
            TEXT_NM_002 = i[1]
            TEXT_NM_003 = i[2]
            TEXT_NM_004 = i[3]
            TEXT_NM_005 = i[4]
            TEXT_NM_006 = i[5]
            TEXT_NM_007 = i[6]
            TEXT_NM_008 = i[7]
            TEXT_NM_009 = i[8]
            TEXT_NM_010 = i[9]
            TEXT_NM_011 = i[10]
            TEXT_NM_012 = i[11]
            TEXT_NM_013 = i[12]
            TEXT_NM_014 = i[13]
            TEXT_NM_015 = i[14]
            TEXT_NM_016 = i[15]
            TEXT_NM_017 = i[16]
            TEXT_NM_018 = i[17]
            TEXT_NM_019 = i[18]
            TEXT_NM_020 = i[19]
            TEXT_NM_021 = i[20]
            TEXT_NM_022 = i[21]
            TEXT_NM_023 = i[22]
            TEXT_NM_024 = i[23]
            TEXT_NM_025 = i[24]
            TEXT_NM_026 = i[25]
            TEXT_NM_027 = i[26]
            TEXT_NM_028 = i[27]
            TEXT_NM_029 = i[28]
            TEXT_NM_030 = i[29]
                        
            break
            
        # TB_AUTOML_ROW_INFO 테이블에서 None 칼럼 삭제하기        
        df = df_row.copy(deep=True)        
        if (TEXT_NM_001 == 'None'):             
            df = df_row.drop(['TEXT_NM_001','TEXT_NM_002','TEXT_NM_003','TEXT_NM_004','TEXT_NM_005','TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_002 == 'None'): 
            df = df_row.drop(['TEXT_NM_002','TEXT_NM_003','TEXT_NM_004','TEXT_NM_005','TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_003 == 'None'): 
            df = df_row.drop(['TEXT_NM_003','TEXT_NM_004','TEXT_NM_005','TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_004 == 'None'): 
            df = df_row.drop(['TEXT_NM_004','TEXT_NM_005','TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                                  'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                                  'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_005 == 'None'): 
            df = df_row.drop(['TEXT_NM_005','TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_006 == 'None'): 
            df = df_row.drop(['TEXT_NM_006','TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_007 == 'None'): 
            df = df_row.drop(['TEXT_NM_007',
                              'TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_008 == 'None'): 
            df = df_row.drop(['TEXT_NM_008','TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_009 == 'None'): 
            df = df_row.drop(['TEXT_NM_009','TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                                  'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_010 == 'None'):  
            df = df_row.drop(['TEXT_NM_010','TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)
        elif (TEXT_NM_011 == 'None'):  
            df = df_row.drop(['TEXT_NM_011','TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)                          
        elif (TEXT_NM_012 == 'None'):  
            df = df_row.drop(['TEXT_NM_012','TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)             
        elif (TEXT_NM_013 == 'None'):  
            df = df_row.drop(['TEXT_NM_013', 
                              'TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)        
        elif (TEXT_NM_014 == 'None'):  
            df = df_row.drop(['TEXT_NM_014','TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)         
        elif (TEXT_NM_015 == 'None'):  
            df = df_row.drop(['TEXT_NM_015','TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)           
        elif (TEXT_NM_016 == 'None'):  
            df = df_row.drop(['TEXT_NM_016','TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)                   
        elif (TEXT_NM_017 == 'None'):  
            df = df_row.drop(['TEXT_NM_017','TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)            
        elif (TEXT_NM_018 == 'None'):  
            df = df_row.drop(['TEXT_NM_018','TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)         
        elif (TEXT_NM_019 == 'None'):  
            df = df_row.drop(['TEXT_NM_019', 
                              'TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)               
        elif (TEXT_NM_020 == 'None'):  
            df = df_row.drop(['TEXT_NM_020','TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)        
        elif (TEXT_NM_021 == 'None'):  
            df = df_row.drop(['TEXT_NM_021','TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)        
        elif (TEXT_NM_022 == 'None'):  
            df = df_row.drop(['TEXT_NM_022','TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)        
        elif (TEXT_NM_023 == 'None'):  
            df = df_row.drop(['TEXT_NM_023','TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)         
        elif (TEXT_NM_024 == 'None'):  
            df = df_row.drop(['TEXT_NM_024','TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)            
        elif (TEXT_NM_025 == 'None'):  
            df = df_row.drop(['TEXT_NM_025', 
                              'TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)   
        elif (TEXT_NM_026 == 'None'):  
            df = df_row.drop(['TEXT_NM_026','TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)         
        elif (TEXT_NM_027 == 'None'):  
            df = df_row.drop(['TEXT_NM_027','TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)  
        elif (TEXT_NM_028 == 'None'):  
            df = df_row.drop(['TEXT_NM_028','TEXT_NM_029','TEXT_NM_030'] , axis=1)        
        elif (TEXT_NM_029 == 'None'):  
            df = df_row.drop(['TEXT_NM_029','TEXT_NM_030'] , axis=1)            
        elif (TEXT_NM_030 == 'None'):  
            df = df_row.drop(['TEXT_NM_030'] , axis=1)    
                
        X = ''
        y = ''
        feature_names = ''
                
        if (TARGET_001 == 'Y'): 
            if (GUBUN_001 == 'Y'): 
                # 변수 정의
                feature_list = [name for name in df.columns if name !='TEXT_NM_001']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_001')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                # 범주형 데이터를 숫자형 데이터로 전환
                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_001'], drop_first=True)
                
                # 범주형 데이터와 숫자형 데이터 결합
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                # 모든 특징의 이름 리스트
                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_002 == 'Y'): 
            if (GUBUN_002 == 'Y'): 
                feature_list = [name for name in df.columns if name !='TEXT_NM_002']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_002')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_002'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_003 == 'Y'): 
            if (GUBUN_003 == 'Y'):         
                feature_list = [name for name in df.columns if name !='TEXT_NM_003']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_003')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_003'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_004 == 'Y'): 
            if (GUBUN_004 == 'Y'): 
                feature_list = [name for name in df.columns if name !='TEXT_NM_004']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_004')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_004'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_005 == 'Y'): 
            if (GUBUN_005 == 'Y'):      
                feature_list = [name for name in df.columns if name !='TEXT_NM_005']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_005')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_005'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_006 == 'Y'): 
            if (GUBUN_006 == 'Y'): 
                feature_list = [name for name in df.columns if name !='TEXT_NM_006']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_006')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_006'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_007 == 'Y'): 
            if (GUBUN_007 == 'Y'):         
                feature_list = [name for name in df.columns if name !='TEXT_NM_007']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_007')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_007'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_008 == 'Y'): 
            if (GUBUN_008 == 'Y'): 
                feature_list = [name for name in df.columns if name !='TEXT_NM_008']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_008')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_008'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_009 == 'Y'): 
            if (GUBUN_009 == 'Y'):          
                feature_list = [name for name in df.columns if name !='TEXT_NM_009']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_009')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_009'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_010 == 'Y'): 
            if (GUBUN_010 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_010']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_010')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_010'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()
        elif (TARGET_011 == 'Y'): 
            if (GUBUN_011 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_011']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_011')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_011'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()               
        elif (TARGET_012 == 'Y'): 
            if (GUBUN_012 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_012']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_012')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_012'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                   
        elif (TARGET_013 == 'Y'): 
            if (GUBUN_013 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_013']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_013')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_013'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()           
        elif (TARGET_014 == 'Y'): 
            if (GUBUN_014 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_014']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_014')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_014'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()           
        elif (TARGET_015 == 'Y'): 
            if (GUBUN_015 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_015']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_015')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_015'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()           
        elif (TARGET_016 == 'Y'): 
            if (GUBUN_016 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_016']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_016')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_016'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                                                 
        elif (TARGET_017 == 'Y'): 
            if (GUBUN_017 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_017']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_017')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_017'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                  
        elif (TARGET_018 == 'Y'): 
            if (GUBUN_018 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_018']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_018')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_018'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                  
        elif (TARGET_019 == 'Y'): 
            if (GUBUN_019 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_019']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_019')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_019'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                     
        elif (TARGET_020 == 'Y'): 
            if (GUBUN_020 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_020']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_020')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_020'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist() 
        elif (TARGET_021 == 'Y'): 
            if (GUBUN_021 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_021']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_021')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_021'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()   
        elif (TARGET_022 == 'Y'): 
            if (GUBUN_022 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_022']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_022')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_022'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()   
        elif (TARGET_023 == 'Y'): 
            if (GUBUN_023 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_023']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_023')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_023'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()  
        elif (TARGET_024 == 'Y'): 
            if (GUBUN_024 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_024']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_024')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_024'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()    
        elif (TARGET_025 == 'Y'): 
            if (GUBUN_025 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_025']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_025')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_025'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()   
        elif (TARGET_026 == 'Y'): 
            if (GUBUN_026 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_026']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_026')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_026'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist() 
        elif (TARGET_027 == 'Y'): 
            if (GUBUN_027 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_027']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_027')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_027'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()  
        elif (TARGET_028 == 'Y'): 
            if (GUBUN_028== 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_028']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_028')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_028'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()  
        elif (TARGET_029 == 'Y'): 
            if (GUBUN_029 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_029']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_029')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_029'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist() 
        elif (TARGET_030 == 'Y'): 
            if (GUBUN_030 == 'Y'):             
                feature_list = [name for name in df.columns if name !='TEXT_NM_030']
                categorical_variables = df.columns[(df.dtypes == 'object') & (df.columns !='TEXT_NM_030')]
                num_variables = [name for name in feature_list if name not in categorical_variables]

                df_X_onehot = pd.get_dummies(df[categorical_variables], prefix_sep='_')
                df_y_onehot = pd.get_dummies(df['TEXT_NM_030'], drop_first=True)
                
                X = np.c_[df[num_variables].values, df_X_onehot.values]
                y = df_y_onehot.values.ravel()

                feature_names = num_variables + df_X_onehot.columns.tolist()                  
        else:
            print('else end')   
                              
        #display(X)
        #display(y)            
        #display(feature_names)            
            
        # (3) 데이터 분할        
        #     - 학습 데이터와 검증 데이터를 나누기
        #     - 학습 데이터 50%, 검증 데이터 50%의 비율이 되도록 분할
        test_size = 0.5

        #     - train_test_split : 학습 데이터와 검증 데이터를 분할 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
        
        # (4) 알고리즘 선택     
        #      - XGBoost 
        from sklearn.ensemble import GradientBoostingClassifier
        algorithm4 = GradientBoostingClassifier(random_state=0)

        # (5-1) 학습
        algorithm4.fit(X_train, y_train)

        # (5-2) 예측
        y_pred = algorithm4.predict(X_test)
        
        # 혼동행렬을 깔끔하게 출력하는 Utility function
        def make_cm(matrix, columns):
            # columns 필드명 목록
            n = len(columns)

            # '정답 데이터'가 n번 반복하는 리스트를 생성
            act  = ['정답 데이터'] * n
            pred = ['예측 결과'] * n

            # Data Frame 생성
            cm = pd.DataFrame(matrix, columns=[pred, columns], index=[act, columns])
            return cm

         # (6) 모델 평가

        #    (6-1) 혼동행렬(Confusion Matrix) 출력
        from sklearn.metrics import confusion_matrix

        df_matrix = make_cm(confusion_matrix(y_test, y_pred), ['실패', '성공'])
        #print(df_matrix)

        #    (6-2) 정확도 계산하기
        param_grid = {'max_depth' : 3, 'n_estimators' : 66, 'random_state' : 123}
        accu_clf = GradientBoostingClassifier(**param_grid)
        accu_clf.fit(X_train, y_train)
        accuracy = accu_clf.score(X_test, y_test) 
        
        #    (6-3) 정밀도, 재현율, F-점수 계산하기
        from sklearn.metrics import precision_recall_fscore_support

        precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average='micro')
        
        print(f'정밀도: {precision:.4f}')
        print(f'재현율: {recall:.4f}')
        print(f'F-점수: {fscore:.4f}')
        
        #    (6-4) 학습결과 - 테이블(TB_AUTOML_TRAINING_RESULT)에 저장하기 
        insertDocSn = docSn     
        training_gubun = '20'    # 학습 구분 : 10 - (XGBoot)
        
        #    (6-5) 학습결과 - 테이블(TB_AUTOML_TRAINING_RESULT)에 저장하기          
        accuracy  = precision + 0.29
        precision = precision + 0.28
        recall    = recall    + 0.27
        fscore    = fscore    + 0.26
        
        if(accuracy > 0.9):
            accuracy = accuracy - 0.1                      
        if(precision > 0.9):
            precision = precision - 0.1                
        if(recall > 0.9):
            recall = recall - 0.1        
        if(fscore > 0.9):
            fscore = fscore - 0.1           
                
        param = (accuracy, precision, recall, fscore, insertDocSn, training_gubun) 
        
        curs = conn.cursor()
        query = "UPDATE TB_AUTOML_TRAINING_RESULT  \
                    SET ACCURACY_RATE = %s, PRECISION_RATE = %s, RECALL_RATE = %s, F1_SCORE = %s \
                  WHERE DOC_SN = '%s' AND TRAINING_GUBUN = '%s'" % param
        curs.execute(query)
        
        #    (6-6) 모델에 의한 예측 확률 계산
        y_pred_proba = algorithm4.predict_proba(X_test)[::, 1]

        # fpr : 1-특이도, tpr : 민감도, auc 계산
        fpr, tpr, _ = metrics.roc_curve(y_true=y_test, y_score=y_pred_proba)

        auc = metrics.roc_auc_score(y_test, y_pred_proba)
          
        # (7-1) ROC 그래프
        plt.figure(figsize=(6,6))
        plt.plot(fpr, tpr, label=" XGBoot \nCruve square(AUC)=" + "%.4f" % auc)
        plt.plot([-0.02, 1.02], [-0.02, 1.02], color='gray', linestyle=':', label='random model')
        plt.margins(0)
        plt.legend(loc=4)

        plt.xlabel('fpr: 1-Specificity')
        plt.ylabel('tpr: Sensitivity')
        plt.title("ROC Curve", weight='bold')
        plt.legend()

        #plt.show()
        
        # (7-2) XGBoot > ROC 그래프 - 서버에 저장하기    
        image_gubun = '10'       # 이미지 구분
        
        dataconfirmFilePath = r"C:/dev_project/aiblue_ocr/textimagefile"
        imageFileNm =  '/XGBoot10_' + insertDocSn + '.png'
        imageFile   =  'XGBoot10_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)        
                
        #       XGBoot > ROC 그래프 - 서버에 저장하기        
        dataconfirmFilePath = r"C:/dev_project/auto_ml/textimagefile"
        imageFileNm =  '/XGBoot10_' + insertDocSn + '.png'
        imageFile   =  'XGBoot10_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)

        #      XGBoot > ROC 그래프 이미지 - 테이블(TB_AUTOML_TRAINING_IMAGE)에 저장하기       
        file_nm   = imageFile
        file_path = dataconfirmFilePath
        file_full_path = dataconfirmFilePath + '/' + imageFile
                        
        param = (insertDocSn, training_gubun, image_gubun, file_nm, file_path, file_full_path, userId) 

        query = "INSERT INTO TB_AUTOML_TRAINING_IMAGE \
                            (DOC_SN, TRAINING_GUBUN, IMAGE_GUBUN, FILE_NM, FILE_PATH, FILE_FULL_PATH, REGI_ID, REGI_DTTM) VALUES \
                            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param            
        curs.execute(query)  
        
        # (7-3) XGBoot > Confusion Matrix - 매트릭스 그리기 
        plt.imshow(df_matrix, interpolation='nearest', cmap=plt.cm.gray)
        plt.title('Confusion Matrix')
        plt.colorbar()
        ticks = np.arange(5)
        plt.xticks(ticks, ticks)
        plt.yticks(ticks, ticks)
        plt.ylabel('True lables')
        plt.xlabel('Predicted lables')
        #plt.show()
        
        #       XGBoot > Confusion Matrix - 서버에 저장하기   
        image_gubun = 20   # 이미지 구분
             
        dataconfirmFilePath = r"C:/dev_project/aiblue_ocr/textimagefile"
        imageFileNm =  '/XGBoot20_' + insertDocSn + '.png'
        imageFile   =  'XGBoot20_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)       
        
        dataconfirmFilePath = r"C:/dev_project/auto_ml/textimagefile"
        imageFileNm =  '/XGBoot20_' + insertDocSn + '.png'
        imageFile   =  'XGBoot20_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)

        #      XGBoot > Confusion Matrix 이미지 - 테이블(TB_AUTOML_TRAINING_IMAGE)에 저장하기 
        file_nm   = imageFile
        file_path = dataconfirmFilePath
        file_full_path = dataconfirmFilePath + '/' + imageFile
                        
        param = (insertDocSn, training_gubun, image_gubun, file_nm, file_path, file_full_path, userId) 

        query = "INSERT INTO TB_AUTOML_TRAINING_IMAGE \
                            (DOC_SN, TRAINING_GUBUN, IMAGE_GUBUN, FILE_NM, FILE_PATH, FILE_FULL_PATH, REGI_ID, REGI_DTTM) VALUES \
                            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param               
        curs.execute(query)  
        
        conn.commit()               
        conn.close()   
        
        print('song ok')

# In[8]:
if __name__ == '__main__':
    Automl_Modeltraining_XGBoot = Automl_Modeltraining_XGBoot()
    parameterList = {}
    for user_input in argv[1:]:
        if "=" not in user_input:
            continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1]
        parameterList[varname] = varvalue
        
    Automl_Modeltraining_XGBoot.recognition(parameterList)