#####################################################
# 2. 데이터 확인, automl_dataconfirm.py
#####################################################

# coding: utf-8

# In[0]:
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import pymysql
import pandas as pd
from sys import argv

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches

class Automl_DataConfirm:
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
                
        docSn  = parameterList["DOC_SN"]
        userId = parameterList["USER_ID"]
        
        # (5-1) 데이터 마스터(TB_AUTOML_MASTER) select
        selectListStringMst = "SELECT DOC_SN, ROW_CNT, COLUMN_CNT FROM TB_AUTOML_MASTER WHERE 1=1 AND DOC_SN = %s"
        curs.execute(selectListStringMst, [docSn])
        
        mstResult = curs.fetchall()
        dataFrameMst = pd.DataFrame(mstResult)
            
        columnSn = 0
        columnCnt = int(dataFrameMst['COLUMN_CNT'])
        
        for i in range(columnCnt):
            columnSn += 1   
            
            # (5-2) 테이터 상세(TB_AUTOML_TEXT) select
            selectListStringText = "SELECT  DOC_SN \
                                          , ROW_SN \
                                          , COLUMN_SN \
                                          , IFNULL(CAST(TEXT_NM AS signed integer), 0) AS TEXT_NM \
                                          , IFNULL((SELECT TEXT_NM FROM TB_AUTOML_COLUMN_INFO a WHERE a.DOC_SN = %s AND a.COLUMN_SN = %s LIMIT 1), '') as COLUMN_NM \
                                          , IFNULL((SELECT CAST(b.MEAN_VALUE AS signed integer) FROM TB_AUTOML_COLUMN_INFO b WHERE b.DOC_SN = %s AND b.COLUMN_SN = %s LIMIT 1), 0) as MEAN_VALUE  \
                                          , TEXT_GUBUN \
                                       FROM TB_AUTOML_TEXT \
                                      WHERE 1 =1 \
                                        AND DOC_SN = %s \
                                        AND COLUMN_SN = %s \
                                        AND TEXT_GUBUN = 'N' \
                                        AND USE_YN = 'Y' \
                                      ORDER BY DOC_SN, COLUMN_SN, ROW_SN "
            
            curs.execute(selectListStringText, [docSn,columnSn,docSn,columnSn,docSn,columnSn] )    
            textResult = curs.fetchall()
            df = pd.DataFrame(textResult)
            #display(dataFrameText)
            
            textSn = columnSn                 # 칼럼 - 열번호
            
            df['MEAN_VALUE'] = 1              # x 좌표로 사용
            t = sorted(list(df['TEXT_NM']))   # 정렬

            # (6-1) 분위수 계산
            q1_index = int(len(t) * 0.25)
            q2_index = int(len(t) * 0.5)
            q3_index = int(len(t) * 0.75)

            q1 = t[q1_index - 1]
            q2 = t[q2_index - 1]
            q3 = t[q3_index - 1]

            # (6-2) 최소값, 최대값 계산
            IQR = q3 - q1

            max_standard = q3 + (1.5 * IQR)
            min_standard = q1 - (1.5 * IQR)

            max_value = max(df[df['TEXT_NM'] <= max_standard]['TEXT_NM'])
            min_value = min(df[df['TEXT_NM'] >= min_standard]['TEXT_NM'])

            #  (6-3) 이상치 계산
            upper_outlier = df[df['TEXT_NM'] >= max_standard][['TEXT_NM', 'MEAN_VALUE']]
            lower_outlier = df[df['TEXT_NM'] <= min_standard][['TEXT_NM', 'MEAN_VALUE']]
            normal = df[(df['TEXT_NM'] > min_standard) & (df['TEXT_NM'] < max_standard)][['TEXT_NM', 'MEAN_VALUE']]

            # 도화지 그리기
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
            ax.set_xticks([])
            ax.set_xlim([0.5, 1.5])

            # 노말
            ax.plot(normal['MEAN_VALUE'], normal['TEXT_NM'], 'bo')
            # 이상치
            # ax.plot(upper_outlier['TEXT_NM'], upper_outlier['TEXT_NM'], 'ro')
            # ax.plot(lower_outlier['TEXT_NM'], lower_outlier['TEXT_NM'], 'ro')

            # 최소값
            ax.hlines(y=min_value, xmin=0.75, xmax=1.25, color='k', linewidth = 5)
            # 최대값
            ax.hlines(y=max_value, xmin=0.75, xmax=1.25, color='k', linewidth = 5)

            # 박스
            ax.hlines(y=q1, xmin=0.75, xmax=1.25, color='k', linewidth = 5)
            ax.hlines(y=q2, xmin=0.75, xmax=1.25, color='k', linewidth = 5)
            ax.hlines(y=q3, xmin=0.75, xmax=1.25, color='k', linewidth = 5)
            ax.vlines(x=0.75, ymin=q1, ymax=q3, color='k', linewidth = 5)
            ax.vlines(x=1.25, ymin=q1, ymax=q3, color='k', linewidth = 5)

            # y축 꾸미기
            ax.set_ylabel('TEXT_NM', fontsize = 20)
            ax.tick_params(axis = 'y', labelsize = 20)

            #  (6-4) Boxplot(상자 수염 그림) - 서버에 저장하기
            insertDocSn = docSn        
            columnSn    = textSn
            convTextSn  = "{}".format(textSn)

            dataconfirmFilePath = r"C:/dev_project/aiblue_ocr/textimagefile"
            imageFileNm =  '/boxplot_' + insertDocSn + '_' + convTextSn + '.png'
            imageFile   =  'boxplot_' + insertDocSn + '_' + convTextSn + '.png'
            plt.savefig(dataconfirmFilePath + imageFileNm)
                        
            dataconfirmFilePath = r"C:/dev_project/auto_ml/textimagefile"
            imageFileNm =  '/boxplot_' + insertDocSn + '_' + convTextSn + '.png'
            imageFile   =  'boxplot_' + insertDocSn + '_' + convTextSn + '.png'
            plt.savefig(dataconfirmFilePath + imageFileNm)

            # (6-5) Boxplot - 테이블(Auto ML - 테이터 컬럼 이미지)에 저장하기        
            image_gubun = '02'    # 테이터 통계 확인 - boxplot (상자 수염 그림)        

            file_nm   = imageFile
            file_path = dataconfirmFilePath
            file_full_path = dataconfirmFilePath + '/' + imageFile
                        
            param = (insertDocSn, columnSn, image_gubun, file_nm, file_path, file_full_path, userId) 

            # (6-6) 테이터 컬럼 이미지(TB_AUTOML_TEXT_IMAGE) insert
            query = "INSERT INTO TB_AUTOML_TEXT_IMAGE (DOC_SN, TEXT_SN, IMAGE_GUBUN, FILE_NM, FILE_PATH, FILE_FULL_PATH, \
                                                  REGI_ID, REGI_DTTM) VALUES \
                            ('%s', %s, '%s', '%s', '%s', '%s', '%s', NOW()) \
                            ON DUPLICATE KEY UPDATE UPDT_DTTM = NOW()" % param               
            
            curs.execute(query)  
            conn.commit()                              
        
        conn.close()   
        
        print('song ok - dataconfirm')

# In[8]:
if __name__ == '__main__':
    Automl_DataConfirm = Automl_DataConfirm()
    parameterList = {}
    for user_input in argv[1:]:
        if "=" not in user_input:
            continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1]
        parameterList[varname] = varvalue
        
    if "METHODS" in parameterList:
        if "recognition" in parameterList["METHODS"]:
            Automl_DataConfirm.recognition(parameterList)
    else: 
        Automl_DataConfirm.recognition(parameterList)  