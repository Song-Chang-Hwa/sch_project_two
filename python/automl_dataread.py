#####################################################
# 1. 데이터 읽어 들이기, automl_dataread.py
#####################################################

# coding: utf-8

# In[0]:
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import pymysql
import pandas as pd
from sys import argv

class Automl_DataRead:
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
        conn = self.getDbConnection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
                
        #userId = 'automl_admin'
        #docSn  = '221111000000010'
        
        docSn  = parameterList["DOC_SN"]
        userId = parameterList["USER_ID"]
                               
        # 문서번호에 해당하는 Excel File Read    
        urlData = 'C:/dev_project/auto_ml/uploadfile/' + docSn + '.csv'
        df = pd.read_csv(urlData, encoding='cp949')
            
        # 업로드 파일의 행(row), 열(column) 계산
        rowCnt    = df.value_counts().sum()
        columnCnt = len(df.columns)  
        
        rowSn    = 0
        columnSn = 0
        
        # (처리 - 1-1) Auto ML - 테이터 상세 테이블 Insert 처리 (Header 데이터)
        textGubun = 'H'      # Header 데이터
        
        for i in df.columns:
            rowSn = 1   
            columnSn += 1       
            textNm = i  

            param = (docSn, rowSn, columnSn, textNm, textGubun, userId)      

            query = "INSERT INTO TB_AUTOML_TEXT (DOC_SN, ROW_SN, COLUMN_SN, TEXT_NM, TEXT_GUBUN, REGI_ID, REGI_DTTM) VALUES \
                                                ('%s', %s, %s, '%s', '%s', '%s', NOW())  \
                                                 ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param   
            curs.execute(query)
                
        conn.commit()

        # (처리 - 1-2) Auto ML - 테이터 상세 테이블 Insert 처리 (실제 데이터)
        rowSn = 1
        columnSn = 0
        textGubun = 'N'
        
        targetFileList = []
        targetFileList = df.values.tolist()
        # print(targetFileList)

        for i in targetFileList:
            rowSn += 1

            for j in range(columnCnt):
                textNm = i[j]         
                columnSn = j + 1   

                param = (docSn, rowSn, columnSn, textNm, textGubun, userId)
                curs = conn.cursor()
                query = "INSERT INTO TB_AUTOML_TEXT (DOC_SN, ROW_SN, COLUMN_SN, TEXT_NM, TEXT_GUBUN, REGI_ID, REGI_DTTM) VALUES \
                                                    ('%s', %s, %s, '%s', '%s', '%s', NOW())  \
                                                     ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param                 
                curs.execute(query)

        conn.commit()
        
        # (처리 - 2) Auto ML - 테이터 컬럼 상세 정보 Insert 처리
        columnSn = 0
        textTypeGubun = ''
        missingValue  = df.isnull().sum()   # 데이터 - 누락값 구하기        

        for i in df.columns:
            columnSn += 1       
            textNm = i  

            missingValueCnt = missingValue[columnSn - 1]        # 칼럼별 누락값 구하기
            textDatatype    = df.dtypes[columnSn - 1]           # 칼럼 데이터 형식 구하기
            
            if(textDatatype == 'int' or textDatatype == 'int64' or textDatatype == 'float' or textDatatype == 'float64'):   
                if (textDatatype == 'int' or textDatatype == 'int64'):
                    textTypeGubun = '10'
                elif (textDatatype == 'float' or textDatatype == 'float64'):
                    textTypeGubun = '20'                
                    
                minValue   = df[textNm].min()          # 최소값
                maxValue   = df[textNm].max()          # 최대값
                meanValue  = df[textNm].mean()         # 평균값        
                stdValue   = df[textNm].std()          # 표준편차
                varValue   = df[textNm].var()          # 분산
                per25Value = df[textNm].quantile(.25)  # 25 퍼센트 값
                per50Value = df[textNm].quantile(.50)  # 50 퍼센트 값
                per75Value = df[textNm].quantile(.75)  # 75 퍼센트 값
            
                param = (docSn, columnSn, textNm, textDatatype, textTypeGubun, minValue, maxValue, meanValue, stdValue, varValue, \
                         per25Value, per50Value, per75Value, missingValueCnt, userId)
            
                curs = conn.cursor()        
                query = "INSERT INTO TB_AUTOML_COLUMN_INFO  \
                          (DOC_SN, COLUMN_SN, TEXT_NM, TEXT_DATA_TYPE, TEXT_TYPE_GUBUN, MININUM_VALUE, MAXINUM_VALUE, MEAN_VALUE,  \
                           STANDARD_DEVIATION, VARIANCE_VALUE, PERCENTAGE_25_VALUE, PERCENTAGE_50_VALUE, PERCENTAGE_75_VALUE, \
                            MISSING_VALUE_CNT, REGI_ID, REGI_DTTM) VALUES \
                          ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param         
                curs.execute(query)
            else:            
                if(textDatatype == 'O' or textDatatype == 'str'):  # 데이터 형식 - object or str  
                    textTypeGubun = '30'
                elif (textDatatype == 'category' or textDatatype == 'CATEGORTY'):  # 데이터 형식 - 카테고리
                    textTypeGubun = '31'   
                elif (textDatatype == 'datetime' or textDatatype == 'datetime64'):  # 데이터 형식 - 날짜 표현
                    textTypeGubun = '40'    
                elif (textDatatype == 'bool' or textDatatype == 'BOOL'):  # 데이터 형식 - 부울형
                    textTypeGubun = '50' 
                else:
                    textTypeGubun = '90'    
                
                param = (docSn, columnSn, textNm, textDatatype, textTypeGubun, missingValueCnt, userId)
            
                curs = conn.cursor()        
                query = "INSERT INTO TB_AUTOML_COLUMN_INFO  \
                          (DOC_SN, COLUMN_SN, TEXT_NM, TEXT_DATA_TYPE, TEXT_TYPE_GUBUN,  \
                           MISSING_VALUE_CNT, REGI_ID, REGI_DTTM) VALUES \
                          ('%s', %s, '%s', '%s', '%s', %s, '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param       
                curs.execute(query)
        
        conn.commit()  
        
        # (처리 - 3-1) Auto ML - 테이터 행 상세 정보 Insert 처리 (Header 데이터)     
        rowSn    = 0
        columnSn = 0
        rowGubun = 'H'      # Header 데이터
        
        text_nm_001 = None
        text_nm_002 = None
        text_nm_003 = None
        text_nm_004 = None
        text_nm_005 = None
        text_nm_006 = None
        text_nm_007 = None
        text_nm_008 = None
        text_nm_009 = None
        text_nm_010 = None
        text_nm_011 = None
        text_nm_012 = None
        text_nm_013 = None
        text_nm_014 = None
        text_nm_015 = None
        text_nm_016 = None
        text_nm_017 = None
        text_nm_018 = None
        text_nm_019 = None
        text_nm_020 = None
        text_nm_021 = None
        text_nm_022 = None
        text_nm_023 = None
        text_nm_024 = None
        text_nm_025 = None
        text_nm_026 = None
        text_nm_027 = None
        text_nm_028 = None
        text_nm_029 = None
        text_nm_030 = None
        
        for i in df.columns:
            rowSn = 1   
            columnSn += 1  

            if(columnSn == 1):
                text_nm_001 = i 
            if(columnSn == 2):
                text_nm_002 = i 
            if(columnSn == 3):
                text_nm_003 = i 
            if(columnSn == 4):
                text_nm_004 = i 
            if(columnSn == 5):
                text_nm_005 = i 
            if(columnSn == 6):
                text_nm_006 = i 
            if(columnSn == 7):
                text_nm_007 = i 
            if(columnSn == 8):
                text_nm_008 = i 
            if(columnSn == 9):
                text_nm_009 = i 
            if(columnSn == 10):
                text_nm_010 = i                 
            if(columnSn == 11):
                text_nm_011 = i 
            if(columnSn == 12):
                text_nm_012 = i 
            if(columnSn == 13):
                text_nm_013 = i 
            if(columnSn == 14):
                text_nm_014 = i 
            if(columnSn == 15):
                text_nm_015 = i 
            if(columnSn == 16):
                text_nm_016 = i 
            if(columnSn == 17):
                text_nm_017 = i 
            if(columnSn == 18):
                text_nm_018 = i 
            if(columnSn == 19):
                text_nm_019 = i 
            if(columnSn == 20):
                text_nm_020 = i  
            if(columnSn == 21):
                text_nm_021 = i 
            if(columnSn == 22):
                text_nm_022 = i 
            if(columnSn == 23):
                text_nm_023 = i 
            if(columnSn == 24):
                text_nm_024 = i 
            if(columnSn == 25):
                text_nm_025 = i 
            if(columnSn == 26):
                text_nm_026 = i 
            if(columnSn == 27):
                text_nm_027 = i 
            if(columnSn == 28):
                text_nm_028 = i 
            if(columnSn == 29):
                text_nm_029 = i 
            if(columnSn == 30):
                text_nm_030 = i   
        
        param = (docSn, rowSn, rowGubun, 
                 text_nm_001, text_nm_002, text_nm_003, text_nm_004, text_nm_005, text_nm_006, text_nm_007, text_nm_008, text_nm_009, text_nm_010,
                 text_nm_011, text_nm_012, text_nm_013, text_nm_014, text_nm_015, text_nm_016, text_nm_017, text_nm_018, text_nm_019, text_nm_020,
                 text_nm_021, text_nm_022, text_nm_023, text_nm_024, text_nm_025, text_nm_026, text_nm_027, text_nm_028, text_nm_029, text_nm_030,
                 userId)      

        query = "INSERT INTO TB_AUTOML_ROW_INFO (DOC_SN, ROW_SN, ROW_GUBUN, \
                        TEXT_NM_001, TEXT_NM_002, TEXT_NM_003, TEXT_NM_004,TEXT_NM_005, TEXT_NM_006, TEXT_NM_007, TEXT_NM_008, TEXT_NM_009, TEXT_NM_010, \
                        TEXT_NM_011, TEXT_NM_012, TEXT_NM_013, TEXT_NM_014,TEXT_NM_015, TEXT_NM_016, TEXT_NM_017, TEXT_NM_018, TEXT_NM_019, TEXT_NM_020, \
                        TEXT_NM_021, TEXT_NM_022, TEXT_NM_023, TEXT_NM_024,TEXT_NM_025, TEXT_NM_026, TEXT_NM_027, TEXT_NM_028, TEXT_NM_029, TEXT_NM_030, \
                        REGI_ID, REGI_DTTM) VALUES \
                       ('%s', %s, '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', NOW())  \
                        ON DUPLICATE KEY UPDATE REGI_DTTM = NOW()" % param                  
        curs.execute(query)
        conn.commit()
        
        # (처리 - 3-2) Auto ML - 테이터 행 상세 정보 Insert 처리 (실제 데이터)    
        rowSn = 1
        columnSn = 0
        rowGubun = 'N'      # 실제 데이터
        
        targetFileList = []
        targetFileList = df.values.tolist()
        # print(targetFileList)
        
        for i in targetFileList:
            rowSn += 1
            
            text_nm_001 = None
            text_nm_002 = None
            text_nm_003 = None
            text_nm_004 = None
            text_nm_005 = None
            text_nm_006 = None
            text_nm_007 = None
            text_nm_008 = None
            text_nm_009 = None
            text_nm_010 = None
            text_nm_011 = None
            text_nm_012 = None
            text_nm_013 = None
            text_nm_014 = None
            text_nm_015 = None
            text_nm_016 = None
            text_nm_017 = None
            text_nm_018 = None
            text_nm_019 = None
            text_nm_020 = None
            text_nm_021 = None
            text_nm_022 = None
            text_nm_023 = None
            text_nm_024 = None
            text_nm_025 = None
            text_nm_026 = None
            text_nm_027 = None
            text_nm_028 = None
            text_nm_029 = None
            text_nm_030 = None

            for j in range(columnCnt):
                textNm = i[j]         
                columnSn = columnSn = j + 1  
                
                if(columnSn == 1):
                    text_nm_001 = textNm 
                if(columnSn == 2):
                    text_nm_002 = textNm 
                if(columnSn == 3):
                    text_nm_003 = textNm
                if(columnSn == 4):
                    text_nm_004 = textNm
                if(columnSn == 5):
                    text_nm_005 = textNm
                if(columnSn == 6):
                    text_nm_006 = textNm 
                if(columnSn == 7):
                    text_nm_007 = textNm 
                if(columnSn == 8):
                    text_nm_008 = textNm 
                if(columnSn == 9):
                    text_nm_009 = textNm 
                if(columnSn == 10):
                    text_nm_010 = textNm                     
                if(columnSn == 11):
                    text_nm_011 = textNm 
                if(columnSn == 12):
                    text_nm_012 = textNm 
                if(columnSn == 13):
                    text_nm_013 = textNm
                if(columnSn == 14):
                    text_nm_014 = textNm
                if(columnSn == 15):
                    text_nm_015 = textNm
                if(columnSn == 16):
                    text_nm_016 = textNm 
                if(columnSn == 17):
                    text_nm_017 = textNm 
                if(columnSn == 18):
                    text_nm_018 = textNm 
                if(columnSn == 19):
                    text_nm_019 = textNm 
                if(columnSn == 20):
                    text_nm_020 = textNm  
                if(columnSn == 21):
                    text_nm_021 = textNm 
                if(columnSn == 22):
                    text_nm_022 = textNm 
                if(columnSn == 23):
                    text_nm_023 = textNm
                if(columnSn == 24):
                    text_nm_024 = textNm
                if(columnSn == 25):
                    text_nm_025 = textNm
                if(columnSn == 26):
                    text_nm_026 = textNm 
                if(columnSn == 27):
                    text_nm_027 = textNm 
                if(columnSn == 28):
                    text_nm_028 = textNm 
                if(columnSn == 29):
                    text_nm_029 = textNm 
                if(columnSn == 30):
                    text_nm_030 = textNm 
                    
            param = (docSn, rowSn, rowGubun, 
                 text_nm_001, text_nm_002, text_nm_003, text_nm_004, text_nm_005, text_nm_006, text_nm_007, text_nm_008, text_nm_009, text_nm_010,
                 text_nm_011, text_nm_012, text_nm_013, text_nm_014, text_nm_015, text_nm_016, text_nm_017, text_nm_018, text_nm_019, text_nm_020,
                 text_nm_021, text_nm_022, text_nm_023, text_nm_024, text_nm_025, text_nm_026, text_nm_027, text_nm_028, text_nm_029, text_nm_030,
                 userId)        

            query = "INSERT INTO TB_AUTOML_ROW_INFO (DOC_SN, ROW_SN, ROW_GUBUN, \
                        TEXT_NM_001, TEXT_NM_002, TEXT_NM_003, TEXT_NM_004,TEXT_NM_005, TEXT_NM_006, TEXT_NM_007, TEXT_NM_008, TEXT_NM_009, TEXT_NM_010, \
                        TEXT_NM_011, TEXT_NM_012, TEXT_NM_013, TEXT_NM_014,TEXT_NM_015, TEXT_NM_016, TEXT_NM_017, TEXT_NM_018, TEXT_NM_019, TEXT_NM_020, \
                        TEXT_NM_021, TEXT_NM_022, TEXT_NM_023, TEXT_NM_024,TEXT_NM_025, TEXT_NM_026, TEXT_NM_027, TEXT_NM_028, TEXT_NM_029, TEXT_NM_030, \
                        REGI_ID, REGI_DTTM) VALUES \
                       ('%s', %s, '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                        '%s', NOW())  \
                        ON DUPLICATE KEY UPDATE REGI_DTTM = NOW()" % param            
            curs.execute(query)
                
        conn.commit()                
        
        # (처리 - 4) Auto ML - 데이터 마스터 테이블 Update 처리
        columnSn = 0

        for i in df.columns:
            rowSn = 1   
            columnSn += 1      
            textNm = i  

            param = (rowCnt, columnCnt, userId, docSn) 

            curs = conn.cursor()
            query = "UPDATE TB_AUTOML_MASTER SET ROW_CNT = %s, COLUMN_CNT = %s, UPDT_ID = '%s', UPDT_DTTM = NOW() \
                                             WHERE DOC_SN = '%s'" % param
            curs.execute(query)
        
        conn.commit()
        
        conn.close()      
        
        print('song ok - dataread')

# In[8]:
if __name__ == '__main__':
    Automl_DataRead = Automl_DataRead()
    parameterList = {}
    for user_input in argv[1:]:
        if "=" not in user_input:
            continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1]
        parameterList[varname] = varvalue
        
    if "METHODS" in parameterList:
        if "recognition" in parameterList["METHODS"]:
            Automl_DataRead.recognition(parameterList)
    else: 
        Automl_DataRead.recognition(parameterList)    