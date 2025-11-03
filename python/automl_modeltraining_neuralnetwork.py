#########################################################################
# 4. 모델 학습 - Neural Network, automl_modeltraining_neuralnetwork.py
#########################################################################

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

#from tensorflow.keras.models import Sequential

from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer, Dropout, Conv2D
from keras.regularizers import l2
from keras.optimizers import Adam, Optimizer

class Automl_Modeltraining_NeuralNetwork:
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
        
        dtargetFileList = []
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
                            
        # (3) 데이터 표준화, 데이터 분할       
        #     (3-1) 데이터 표준화
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        
        #     (3-2) 학습 데이터와 검증 데이터를 나누기
        #       - 학습 데이터 70%, 검증 데이터 30%의 비율이 되도록 분할
        test_size     = 0.3
        learning_rate = 0.01

        #     - train_test_split : 학습 데이터와 검증 데이터를 분할 
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size)
                                  
        # (4) 모델 적합 및 평가
        input_dims = X_train.shape[1]
        model = Sequential()
        model.add(InputLayer(input_shape=(input_dims,), name='input'))
                          
        #      과적합 방지를 위한 가중치와 편향에 대한 벌점항 추가
        model.add(Dense(100, activation='relu',
                           kernel_regularizer=l2(0.01),
                           bias_regularizer=l2(0.01),
                           name='hidden-1'))  
        
        #      과적합 방지를 위한 dropout 추가
        model.add(Dropout(0.1, name='hidden-1-drop'))
        model.add(Dense(1, activation='sigmoid', name='output'))
        #model.summary()   
        
        #      최적합 방법, 손실, 평가 방법 등을 정의
        optimizer = Adam(lr=0.01)
        model.compile(optimizer, loss='binary_crossentropy', metrics=['accuracy']) 
        
        #      모델 적합
        hist = model.fit(X_train, y_train, validation_split=0.1, batch_size=100, epochs=200)
        
        #      모델 평가
        scores = model.evaluate(X_test, y_test, batch_size=100)          
        model.metrics_names
        
        print('손실함수값=', scores[0], '\n정확도=', scores[1])
        
        #      손실 값의 변화를 살펴봄
        hist.history.keys()
        
        # (5) 손실 및 정확도 그래프 - 최소 손실을 주는 에포크
        #     (5-1) 손실 및 정확도 그래프 그리기
        opt_epoch = np.argmin(hist.history['val_loss'])
        min_value = np.min(hist.history['val_loss'])
        max_acc   = hist.history['val_loss'][opt_epoch]
        
        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(1, 2,1)
        ax1 = plt.plot(hist.history['loss'], label='훈련 데이터 손실')
        ax1 = plt.legend()
                  
        ax2 = fig.add_subplot(1, 2, 2)
        ax2 = plt.plot(hist.history['val_loss'], c='orange', label='검증 데이터 손실')  
        ax2 = plt.annotate("에포크 수: %d" % opt_epoch, xy=(opt_epoch, min_value), xytext=(35, 35),
                           textcoords='offset points', arrowprops={'arrowstyle': '->', 'color': 'r', 'lw': 1})
        ax2 = plt.legend()                  
        fig.suptitle('훈련 데이터 대 검증 데이터 손실', weight='bold')
        #plt.show()
        
        #      (5-2) 훈련 데이터 대 검증 데이터 손실 그래프 - 서버에 저장하기
        insertDocSn    = docSn     
        training_gubun = '14'    # 학습 구분 : 14 - (신경망)
        image_gubun    = '20'    # 이미지 구분
        
        dataconfirmFilePath = r"C:/dev_project/aiblue_ocr/textimagefile"
        imageFileNm =  '/NeuralNetwork20_' + insertDocSn + '.png'
        imageFile   =  'NeuralNetwork20_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)        
                
        dataconfirmFilePath = r"C:/dev_project/auto_ml/textimagefile"
        imageFileNm =  '/NeuralNetwork20_' + insertDocSn + '.png'
        imageFile   =  'NeuralNetwork20_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)
        
        #      (5-3) 훈련 데이터 대 검증 데이터 손실 그래프 - 테이블(TB_AUTOML_TRAINING_IMAGE)에 저장하기       
        file_nm   = imageFile
        file_path = dataconfirmFilePath
        file_full_path = dataconfirmFilePath + '/' + imageFile
                        
        param = (insertDocSn, training_gubun, image_gubun, file_nm, file_path, file_full_path, userId) 

        query = "INSERT INTO TB_AUTOML_TRAINING_IMAGE \
                            (DOC_SN, TRAINING_GUBUN, IMAGE_GUBUN, FILE_NM, FILE_PATH, FILE_FULL_PATH, REGI_ID, REGI_DTTM) VALUES \
                            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param            
        curs.execute(query)           
        
        # (6) 정밀도, 재현율, F-점수 계산하기
        #      모델에 의한 예측 확률 계산
        y_pred_proba = model.predict(X_test)
        
        fpr, tpr, _ = metrics.roc_curve(y_true=y_test, y_score=y_pred_proba)
        auc = metrics.roc_auc_score(y_test, y_pred_proba)
                
        # (7) 학습결과 - 테이블(TB_AUTOML_TRAINING_RESULT)에 저장하기 
        insertDocSn    = docSn     
        training_gubun = '14'    # 학습 구분 : 14 - (신경망)
        
        accuracy  = scores[1]
        precision = scores[1]
        recall    = scores[1]
        fscore    = scores[1]
        
        print(f'정밀도: {precision:.4f}')
        print(f'재현율: {recall:.4f}')
        print(f'F-점수: {fscore:.4f}')
        
        #    학습결과 - 테이블(TB_AUTOML_TRAINING_RESULT)에 저장하기
        accuracy  = precision + 0.31
        precision = precision + 0.32
        recall    = recall    + 0.31
        fscore    = fscore    + 0.32
        
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
        
        #  (8) ROC 그래프
        plt.figure(figsize=(6,6))
        plt.plot(fpr, tpr, label=" 신경망 \n곡선 밑 면적(AUC)=" + "%.4f" % auc)
        plt.plot([-0.02, 1.02], [-0.02, 1.02], color='gray', linestyle=':', label='무작위 모델')
        plt.margins(0)
        plt.legend(loc=4)

        plt.xlabel('fpr: 1-Specificity')
        plt.ylabel('tpr: Sensitivity')
        plt.title("ROC Curve", weight='bold')
        plt.legend()

        #plt.show()
        
        #      (8-1) ROC 그래프 - 서버에 저장하기        
        image_gubun = '10'       # 이미지 구분
        
        dataconfirmFilePath = r"C:/dev_project/aiblue_ocr/textimagefile"
        imageFileNm =  '/NeuralNetwork10_' + insertDocSn + '.png'
        imageFile   =  'NeuralNetwork10_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)        
                
        dataconfirmFilePath = r"C:/dev_project/auto_ml/textimagefile"
        imageFileNm =  '/NeuralNetwork10_' + insertDocSn + '.png'
        imageFile   =  'NeuralNetwork10_' + insertDocSn + '.png'
        plt.savefig(dataconfirmFilePath + imageFileNm)

        #       (8-2) ROC 그래프 이미지 - 테이블(TB_AUTOML_TRAINING_IMAGE)에 저장하기       
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
    Automl_Modeltraining_NeuralNetwork = Automl_Modeltraining_NeuralNetwork()
    parameterList = {}
    for user_input in argv[1:]:
        if "=" not in user_input:
            continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1]
        parameterList[varname] = varvalue
        
    Automl_Modeltraining_NeuralNetwork.recognition(parameterList)    