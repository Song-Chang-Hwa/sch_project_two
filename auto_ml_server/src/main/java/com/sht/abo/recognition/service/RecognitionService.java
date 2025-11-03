package com.sht.abo.recognition.service;

import java.io.File;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import com.sht.abo.comm.dao.CommonBaseDAO;
import com.sht.abo.vo.ComResultVO;
import com.sht.common.ABOConstant;
import com.sht.util.CommUtils;
import com.sht.util.ProcessOutputThread;

import kr.co.stc.core.util.FileUtil;

/**
 * Auto Machine Learning
 * 
 * @author : Song Chang Hwa
 *
 */
@Service
public class RecognitionService {

	private Logger logger = LoggerFactory.getLogger(RecognitionService.class);

	@Autowired
	private CommonBaseDAO commonBaseDAO;

	@Value("${ocr.file.upload.path}")
	private String fileUploadPath;

	@Value("${ocr.file.upload.url}")
	private String fileUploadUrl;

	@Value("${ocr.file.py.path}")
	private String filePyPath;

	@Value("${ocr.file.pyexec.path}")
	private String filePyExecPath;
	
	// 추가 : 2022.09.28, 송창화
	@Value("${ocr.file.upload.fullpath}")
	private String fileUploadFullPath;
	
	// 데이터 읽어 들이기 > 데이터 마스터 목록 [조회] 처리
	@Transactional(readOnly = true)
	public ComResultVO selectAutomlMasterList(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectAutomlMasterList", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectAutomlMasterListCount", paramMap));
	}
	
	// 데이터 읽어 들이기 > 데이터 상세 목록 [조회] 처리
	@Transactional(readOnly = true)
	public ComResultVO selectAutomlDatareadColumnInfo(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectAutomlDatareadColumnInfo", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectAutomlDatareadColumnInfoCount", paramMap));
	}
	
	// 데이터 읽어 들이기 > 데이터 상세 목록 [조회] 처리
	@Transactional(readOnly = true)
	public Object selectAutomlDatareadColumnInfo_old(Map<String, Object> paramMap) throws Exception {
		List<Map<String, Object>> pList = this.commonBaseDAO.list("RecognitionDAO.selectAutomlDatareadColumnInfo", paramMap);

		List<Object> listF     = new ArrayList<Object>();
        Map<String, Object> m1 = new HashMap<String, Object>();
        Map<String, Object> m2 = new HashMap<String, Object>();

        HashMap hm = new HashMap();
		
        String comp_row_sn   = null;
		        
        String rowArray[];
        String sv_text_nm = null;
        int column_cnt    = 0;
        
        rowArray = new String[100];
        
        for (int i = 0; i < pList.size(); i++)
        {
            m1 = (Map<String, Object>) pList.get(i);
            
            if (i == 0) {
            	comp_row_sn = m1.get("ROW_SN").toString();
            }     
        
            column_cnt += 1;
            
            if (!comp_row_sn.equals(m1.get("ROW_SN").toString()))
            {	//칼럼 - 행번호가 다른 경우
	            m2 = new HashMap<String, Object>();
        
		        for (int k = 1; k < (column_cnt + 1); k++) {
		        	if (k ==  1) { m2.put("text_nm_001", rowArray[k]);}
		        	if (k ==  2) { m2.put("text_nm_002", rowArray[k]);}	
		        	if (k ==  3) { m2.put("text_nm_003", rowArray[k]);}
		        	if (k ==  4) { m2.put("text_nm_004", rowArray[k]);}
		        	if (k ==  5) { m2.put("text_nm_005", rowArray[k]);}
		        	if (k ==  6) { m2.put("text_nm_006", rowArray[k]);}
		        	if (k ==  7) { m2.put("text_nm_007", rowArray[k]);}
		        	if (k ==  8) { m2.put("text_nm_008", rowArray[k]);}
		        	if (k ==  9) { m2.put("text_nm_009", rowArray[k]);}
		        	if (k == 10) { m2.put("text_nm_010", rowArray[k]);}
		        	
		        	if (k == 11) { m2.put("text_nm_011", rowArray[k]);}
		        	if (k == 12) { m2.put("text_nm_012", rowArray[k]);}	
		        	if (k == 13) { m2.put("text_nm_013", rowArray[k]);}
		        	if (k == 14) { m2.put("text_nm_014", rowArray[k]);}
		        	if (k == 15) { m2.put("text_nm_015", rowArray[k]);}
		        	if (k == 16) { m2.put("text_nm_016", rowArray[k]);}
		        	if (k == 17) { m2.put("text_nm_017", rowArray[k]);}
		        	if (k == 18) { m2.put("text_nm_018", rowArray[k]);}
		        	if (k == 19) { m2.put("text_nm_019", rowArray[k]);}
		        	if (k == 20) { m2.put("text_nm_020", rowArray[k]);}
		        	
		        	if (k == 21) { m2.put("text_nm_021", rowArray[k]);}
		        	if (k == 22) { m2.put("text_nm_022", rowArray[k]);}	
		        	if (k == 23) { m2.put("text_nm_023", rowArray[k]);}
		        	if (k == 24) { m2.put("text_nm_024", rowArray[k]);}
		        	if (k == 25) { m2.put("text_nm_025", rowArray[k]);}
		        	if (k == 26) { m2.put("text_nm_026", rowArray[k]);}
		        	if (k == 27) { m2.put("text_nm_027", rowArray[k]);}
		        	if (k == 28) { m2.put("text_nm_028", rowArray[k]);}
		        	if (k == 29) { m2.put("text_nm_029", rowArray[k]);}
		        	if (k == 30) { m2.put("text_nm_030", rowArray[k]);}

		        	if (k == 31) { m2.put("text_nm_031", rowArray[k]);}
		        	if (k == 32) { m2.put("text_nm_032", rowArray[k]);}	
		        	if (k == 33) { m2.put("text_nm_033", rowArray[k]);}
		        	if (k == 34) { m2.put("text_nm_034", rowArray[k]);}
		        	if (k == 35) { m2.put("text_nm_035", rowArray[k]);}
		        	if (k == 36) { m2.put("text_nm_036", rowArray[k]);}
		        	if (k == 37) { m2.put("text_nm_037", rowArray[k]);}
		        	if (k == 38) { m2.put("text_nm_038", rowArray[k]);}
		        	if (k == 39) { m2.put("text_nm_039", rowArray[k]);}
		        	if (k == 40) { m2.put("text_nm_040", rowArray[k]);}
		        	
		        	if (k == 41) { m2.put("text_nm_041", rowArray[k]);}
		        	if (k == 42) { m2.put("text_nm_042", rowArray[k]);}	
		        	if (k == 43) { m2.put("text_nm_043", rowArray[k]);}
		        	if (k == 44) { m2.put("text_nm_044", rowArray[k]);}
		        	if (k == 45) { m2.put("text_nm_045", rowArray[k]);}
		        	if (k == 46) { m2.put("text_nm_046", rowArray[k]);}
		        	if (k == 47) { m2.put("text_nm_047", rowArray[k]);}
		        	if (k == 48) { m2.put("text_nm_048", rowArray[k]);}
		        	if (k == 49) { m2.put("text_nm_049", rowArray[k]);}
		        	if (k == 50) { m2.put("text_nm_050", rowArray[k]);}
		        }
		        
		        listF.add(m2);
		        
		        comp_row_sn = m1.get("ROW_SN").toString();
		        column_cnt  = 0;
            } else {            	
            	rowArray[column_cnt] = m1.get("TEXT_NM").toString();
            }
            
            if (i == pList.size() - 1)
            {
                m2 = new HashMap<String, Object>();
            
		        for (int k = 1; k < (column_cnt + 1); k++) {
		        	if (k ==  1) { m2.put("text_nm_001", rowArray[k]);}
		        	if (k ==  2) { m2.put("text_nm_002", rowArray[k]);}	
		        	if (k ==  3) { m2.put("text_nm_003", rowArray[k]);}
		        	if (k ==  4) { m2.put("text_nm_004", rowArray[k]);}
		        	if (k ==  5) { m2.put("text_nm_005", rowArray[k]);}
		        	if (k ==  6) { m2.put("text_nm_006", rowArray[k]);}
		        	if (k ==  7) { m2.put("text_nm_007", rowArray[k]);}
		        	if (k ==  8) { m2.put("text_nm_008", rowArray[k]);}
		        	if (k ==  9) { m2.put("text_nm_009", rowArray[k]);}
		        	if (k == 10) { m2.put("text_nm_010", rowArray[k]);}
		        	
		        	if (k == 11) { m2.put("text_nm_011", rowArray[k]);}
		        	if (k == 12) { m2.put("text_nm_012", rowArray[k]);}	
		        	if (k == 13) { m2.put("text_nm_013", rowArray[k]);}
		        	if (k == 14) { m2.put("text_nm_014", rowArray[k]);}
		        	if (k == 15) { m2.put("text_nm_015", rowArray[k]);}
		        	if (k == 16) { m2.put("text_nm_016", rowArray[k]);}
		        	if (k == 17) { m2.put("text_nm_017", rowArray[k]);}
		        	if (k == 18) { m2.put("text_nm_018", rowArray[k]);}
		        	if (k == 19) { m2.put("text_nm_019", rowArray[k]);}
		        	if (k == 20) { m2.put("text_nm_020", rowArray[k]);}
		        	
		        	if (k == 21) { m2.put("text_nm_021", rowArray[k]);}
		        	if (k == 22) { m2.put("text_nm_022", rowArray[k]);}	
		        	if (k == 23) { m2.put("text_nm_023", rowArray[k]);}
		        	if (k == 24) { m2.put("text_nm_024", rowArray[k]);}
		        	if (k == 25) { m2.put("text_nm_025", rowArray[k]);}
		        	if (k == 26) { m2.put("text_nm_026", rowArray[k]);}
		        	if (k == 27) { m2.put("text_nm_027", rowArray[k]);}
		        	if (k == 28) { m2.put("text_nm_028", rowArray[k]);}
		        	if (k == 29) { m2.put("text_nm_029", rowArray[k]);}
		        	if (k == 30) { m2.put("text_nm_030", rowArray[k]);}

		        	if (k == 31) { m2.put("text_nm_031", rowArray[k]);}
		        	if (k == 32) { m2.put("text_nm_032", rowArray[k]);}	
		        	if (k == 33) { m2.put("text_nm_033", rowArray[k]);}
		        	if (k == 34) { m2.put("text_nm_034", rowArray[k]);}
		        	if (k == 35) { m2.put("text_nm_035", rowArray[k]);}
		        	if (k == 36) { m2.put("text_nm_036", rowArray[k]);}
		        	if (k == 37) { m2.put("text_nm_037", rowArray[k]);}
		        	if (k == 38) { m2.put("text_nm_038", rowArray[k]);}
		        	if (k == 39) { m2.put("text_nm_039", rowArray[k]);}
		        	if (k == 40) { m2.put("text_nm_040", rowArray[k]);}
		        	
		        	if (k == 41) { m2.put("text_nm_041", rowArray[k]);}
		        	if (k == 42) { m2.put("text_nm_042", rowArray[k]);}	
		        	if (k == 43) { m2.put("text_nm_043", rowArray[k]);}
		        	if (k == 44) { m2.put("text_nm_044", rowArray[k]);}
		        	if (k == 45) { m2.put("text_nm_045", rowArray[k]);}
		        	if (k == 46) { m2.put("text_nm_046", rowArray[k]);}
		        	if (k == 47) { m2.put("text_nm_047", rowArray[k]);}
		        	if (k == 48) { m2.put("text_nm_048", rowArray[k]);}
		        	if (k == 49) { m2.put("text_nm_049", rowArray[k]);}
		        	if (k == 50) { m2.put("text_nm_050", rowArray[k]);}
		        }
		        
		        listF.add(m2);
            }
        }
        
        hm.put("data", listF);

        return hm;
	}			
	
	// 데이터 읽어 들이기 > 억셀 파일 업로드
	@Transactional
	public ComResultVO automlDatareadUpload(MultipartHttpServletRequest multipartHttpServletRequest) throws Exception {
		int result = 0;
		String userId = CommUtils.getUser();

		FileUtil.makeBasePath(this.fileUploadPath);
		FileUtil.makeBasePath(this.fileUploadFullPath);

		Map<String, Object> dataMap = new HashMap<>();

		String prjId = "220503000000001";
		dataMap.put("SEQ_NM", "DOC_SN");
		String docSn = (String) this.commonBaseDAO.selectByPk("CommDAO.getSeq", dataMap);

		Iterator<String> fileNames = multipartHttpServletRequest.getFileNames();

		@SuppressWarnings("unused")
		String targetFile = "";
		@SuppressWarnings("unused")
		String pyFile = "";
		String fileId = "";
		while (fileNames.hasNext()) {
			String fileName = fileNames.next();
			MultipartFile mFile = multipartHttpServletRequest.getFile(fileName);

			if (mFile.getSize() != 0) {

				String newFileName = docSn + "." + FileUtil.getExtension(mFile.getOriginalFilename());
				File file = new File(this.fileUploadPath + File.separator + newFileName);
				FileOutputStream fos = new FileOutputStream(file);
				fos.write(mFile.getBytes());
				fos.close();

				dataMap.put("SEQ_NM", "FILE_ID");
				fileId = (String) this.commonBaseDAO.selectByPk("CommDAO.getSeq", dataMap);
				
				dataMap.put("DOC_SN", docSn);
				dataMap.put("DOC_NM", multipartHttpServletRequest.getParameter("BUSINESS_NM"));
								
				dataMap.put("FILE_ID", fileId);
				dataMap.put("FILE_PATH", this.fileUploadPath);
				dataMap.put("FILE_URL", this.fileUploadUrl);
				dataMap.put("FILE_NM", newFileName);
				dataMap.put("FILE_SIZE", file.length());
				dataMap.put("FILE_ORI_NM", mFile.getOriginalFilename());
							
				String fileFullPath = this.fileUploadFullPath + '/' + newFileName;
				dataMap.put("FILE_FULL_PATH", fileFullPath);	
				
				dataMap.put("STAT_CD", "00");
				dataMap.put("userId", userId);

				// 데이터 마스터, 엑셀 업로드 파일 - Insert 처리
				this.commonBaseDAO.update("RecognitionDAO.insertAutomlMst", dataMap);
				result += this.commonBaseDAO.update("RecognitionDAO.insertAutoMlFile", dataMap);

				targetFile = newFileName;
			}
		}

		ComResultVO comResultVO = new ComResultVO(result);
		Map<String, Object> mp = new HashMap<String, Object>();
		mp.put("pyFile", "");
		mp.put("PRJ_ID", prjId);
		mp.put("USER_ID", userId);
		mp.put("DOC_SN", docSn);
		mp.put("METHODS", "recognition");
		comResultVO.setData(mp);
		return comResultVO;
	}
		
	// 데이터 읽어 들이기 > 엑셀 파일 업로드
	// 파이썬 프로그램 처리 - automl_dataread.py
	// @Transactional
	public ComResultVO pythinExecAutomlDataread(Map<String, Object> paramMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		comResultVO.setData(paramMap);
		@SuppressWarnings("unused")
		Process p = null;
		StringBuffer exec = new StringBuffer();
		String param = "";
		
		for (String key : paramMap.keySet()) {
			param += " " + key + "=" + paramMap.get(key);
		}
		
		try {
			exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_dataread.py")
					.append(param);
			p = Runtime.getRuntime().exec(exec.toString());

			// 실행 결과 확인
			StringBuffer stdMsg = new StringBuffer();
			StringBuffer errMsg = new StringBuffer();

			// 스레드로 inputStream 버퍼 비우기
			ProcessOutputThread o = new ProcessOutputThread(p.getInputStream(), stdMsg);
			o.start();

			// 스레드로 errorStream 버퍼 비우기
			o = new ProcessOutputThread(p.getErrorStream(), errMsg);
			o.start();

			int exitCode = p.waitFor();
			if (exitCode != 0) {
				paramMap.put("STAT_CD", "30");
				paramMap.put("ERROR_MSG", errMsg.toString());
				this.commonBaseDAO.update("RecognitionDAO.updateAutomlMstResult", paramMap);
			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			comResultVO.setCode(511);
		}
		
		//p.destroy();
		exec.delete(0, exec.length());
		exec.setLength(0);
		exec = null;
		return comResultVO;
	}	
	
	// 데이터 확인 - Python 처리 : 이미지 생성
	// 파이썬 프로그램 처리 - automl_dataconfirm.py
	// @Transactional
	public ComResultVO pythinAutomlDataconfirm(Map<String, Object> paramMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		comResultVO.setData(paramMap);
		@SuppressWarnings("unused")
		Process p = null;
		StringBuffer exec = new StringBuffer();
		String param = "";
		
		for (String key : paramMap.keySet()) {
			param += " " + key + "=" + paramMap.get(key);
		}
		
		try {
			exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_dataconfirm.py")
					.append(param);
			p = Runtime.getRuntime().exec(exec.toString());
	
			// 실행 결과 확인
			StringBuffer stdMsg = new StringBuffer();
			StringBuffer errMsg = new StringBuffer();

			// 스레드로 inputStream 버퍼 비우기
			ProcessOutputThread o = new ProcessOutputThread(p.getInputStream(), stdMsg);
			o.start();

			// 스레드로 errorStream 버퍼 비우기
			o = new ProcessOutputThread(p.getErrorStream(), errMsg);
			o.start();

			int exitCode = p.waitFor();
			if (exitCode != 0) {
				paramMap.put("STAT_CD", "30");
				paramMap.put("ERROR_MSG", errMsg.toString());
				this.commonBaseDAO.update("RecognitionDAO.updateAutomlMstResult", paramMap);
			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			comResultVO.setCode(511);
		}
					
		//p.destroy();
		exec.delete(0, exec.length());
		exec.setLength(0);
		exec = null;
		return comResultVO;
	}	
		
	// 모델 선택.학습 > 분류 모델 처리하기 - 파이썬 프로그램 처리 
	// @Transactional
	public ComResultVO pythonTrainingClassificationModelProcess(Map<String, Object> paramMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		comResultVO.setData(paramMap);
		@SuppressWarnings("unused")
		Process p = null;
		StringBuffer exec = new StringBuffer();
		String param = "";
		
		String sv_training_gubun = null;
		
		for (String key : paramMap.keySet()) {
			param += " " + key + "=" + paramMap.get(key);
		}
		
		try {
			sv_training_gubun = paramMap.get("TRAINING_GUBUN").toString();
			if(sv_training_gubun.equals("10")) {		//XGBoot
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_xgboot.py")
				.append(param);
			} else if(sv_training_gubun.equals("11")) {	//의사결정트리
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_decisiontree.py")
					.append(param);
			} else if(sv_training_gubun.equals("12")) {	//Random Forest
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_randomforest.py")
					.append(param);
			} else if(sv_training_gubun.equals("13")) {	//SVM
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_svm.py")
					.append(param);
			} else if(sv_training_gubun.equals("14")) {	//신경망	
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_neuralnetwork.py")
					.append(param);
			} else {
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_xgboot.py")
				.append(param);
			}
			
			p = Runtime.getRuntime().exec(exec.toString());
	
			// 실행 결과 확인
			StringBuffer stdMsg = new StringBuffer();
			StringBuffer errMsg = new StringBuffer();
	
			// 스레드로 inputStream 버퍼 비우기
			ProcessOutputThread o = new ProcessOutputThread(p.getInputStream(), stdMsg);
			o.start();
	
			// 스레드로 errorStream 버퍼 비우기
			o = new ProcessOutputThread(p.getErrorStream(), errMsg);
			o.start();
	
			int exitCode = p.waitFor();
			if (exitCode != 0) {
				paramMap.put("STAT_CD", "30");
				paramMap.put("ERROR_MSG", errMsg.toString());
				this.commonBaseDAO.update("RecognitionDAO.updateAutomlMstResult", paramMap);
			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			comResultVO.setCode(511);
		}
		
		//p.destroy();
		exec.delete(0, exec.length());
		exec.setLength(0);
		exec = null;
		return comResultVO;
	}		
		
	// 모델 선택.학습 > 군집 모델 처리하기 - 파이썬 프로그램 처리 
	// @Transactional
	public ComResultVO pythonTrainingClusteringModelProcess(Map<String, Object> paramMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		comResultVO.setData(paramMap);
		@SuppressWarnings("unused")
		Process p = null;
		StringBuffer exec = new StringBuffer();
		String param = "";
		
		String sv_training_gubun = null;
		
		for (String key : paramMap.keySet()) {
			param += " " + key + "=" + paramMap.get(key);
		}
		
		try {
			sv_training_gubun = paramMap.get("TRAINING_GUBUN").toString();
			if(sv_training_gubun.equals("20")) {		//K-means Clustering 
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_clustering.py")
					.append(param);
			} else {
				exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_modeltraining_clustering.py")
					.append(param);
			}
			
			p = Runtime.getRuntime().exec(exec.toString());
	
			// 실행 결과 확인
			StringBuffer stdMsg = new StringBuffer();
			StringBuffer errMsg = new StringBuffer();
	
			// 스레드로 inputStream 버퍼 비우기
			ProcessOutputThread o = new ProcessOutputThread(p.getInputStream(), stdMsg);
			o.start();
	
			// 스레드로 errorStream 버퍼 비우기
			o = new ProcessOutputThread(p.getErrorStream(), errMsg);
			o.start();
	
			int exitCode = p.waitFor();
			if (exitCode != 0) {
				paramMap.put("STAT_CD", "30");
				paramMap.put("ERROR_MSG", errMsg.toString());
				this.commonBaseDAO.update("RecognitionDAO.updateAutomlMstResult", paramMap);
			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			comResultVO.setCode(511);
		}
		
		//p.destroy();
		exec.delete(0, exec.length());
		exec.setLength(0);
		exec = null;
		return comResultVO;
	}		
	
	// @Transactional
	public ComResultVO pythinExecNew_20220928(Map<String, Object> paramMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		comResultVO.setData(paramMap);
		@SuppressWarnings("unused")
		Process p = null;
		StringBuffer exec = new StringBuffer();
		String param = "";
		for (String key : paramMap.keySet()) {
			param += " " + key + "=" + paramMap.get(key);
		}
		
		try {

			exec.append(filePyExecPath).append(" ").append(filePyPath).append(File.separator).append("automl_dataread.py")
					.append(param);
			p = Runtime.getRuntime().exec(exec.toString());

//			// 실행 결과 확인
//			StringBuffer stdMsg = new StringBuffer();
//			StringBuffer errMsg = new StringBuffer();
//
//			// 스레드로 inputStream 버퍼 비우기
//			ProcessOutputThread o = new ProcessOutputThread(p.getInputStream(), stdMsg);
//			o.start();
//
//			// 스레드로 errorStream 버퍼 비우기
//			o = new ProcessOutputThread(p.getErrorStream(), errMsg);
//			o.start();
//
//			int exitCode = p.waitFor();
//			if (exitCode != 0) {
//				paramMap.put("STAT_CD", "30");
//				paramMap.put("ERROR_MSG", errMsg.toString());
//				this.commonBaseDAO.update("RecognitionDAO.updateOcrDocMstResult", paramMap);
//			}
		} catch (Exception ex) {
			System.out.println(ex.getMessage());
			comResultVO.setCode(511);
		}
		//p.destroy();
		exec.delete(0, exec.length());
		exec.setLength(0);
		exec = null;
		return comResultVO;
	}
	
	// 데이터 읽어 들이기 > 데이터 마스터 목록 [삭제] 처리
	@Transactional
	public ComResultVO deleteAutomlMst(Map<String, Object> paramMap) throws Exception {
		int result = this.commonBaseDAO.update("RecognitionDAO.deleteAutomlMst", paramMap);

		ComResultVO comResultVO = new ComResultVO(result);
		return comResultVO;
	}		

	// 데이터 확인 > 데이터 컬럼 상세 목록 [조회] 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMldataConfirmList(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMldataConfirmList", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMldataConfirmListCount", paramMap));
	}

	// 데이터 확인 > 02:데이터 분포 (Boxplot), 03:정규분포 (Normal Distribution) 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMldataConfirmTextImage(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMldataConfirmTextImage", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMldataConfirmTextImageCount", paramMap));
	}
		
	// 데이터 확인 > 데이터 마스터 목록 <수정> 처리
	@Transactional
	public ComResultVO dataConfirmProcess(Map<String, Object> paramMap) throws Exception {
		int result = this.commonBaseDAO.update("RecognitionDAO.dataConfirmProcess", paramMap);

		ComResultVO comResultVO = new ComResultVO(result);
		return comResultVO;
	}		
	
	// 데이터 전처리 > 목표변수 적용
	@Transactional
	public ComResultVO precprocessingTargetApply(List<Map<String, Object>> listParamMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		String userId = CommUtils.getUser();

		int cnt = 0;

		for (Map<String, Object> paramMap : listParamMap) {
			paramMap.put("userId", userId);
			
			cnt += (int) this.commonBaseDAO.update("RecognitionDAO.precprocessingTargetApply", paramMap);
			
			// 데이터 마스터 목록 <수정> 처리
			int resultMaster = this.commonBaseDAO.update("RecognitionDAO.precprocessingDataMasterUpdate", paramMap);
		}
					
		if (cnt == listParamMap.size()) {
			comResultVO.setCode(ABOConstant.HTTP_STATUS_CREATE_OK);
		} else {
			comResultVO.setCode(ABOConstant.HTTP_STATUS_SERVER_ERROR);
			comResultVO.setMsg(listParamMap.size() + "건 중 " + cnt + "건을 처리하였습니다. 처리결과를 확인하십시오.");
		}
		
		return comResultVO;
	}
		
	// 데이터 전처리 > 데이터 정제(Data Cleansing) 조회 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMlpreprocessingDataCleansingList(Map<String, Object> paramMap) throws Exception {
		Map<String, Object> mp = new HashMap<String, Object>();
		
		// 데이터 전처리 > 데이터 정제(Data Cleansing) - 데이터 존재여부 체크
		List<Map<String, Object>> list = this.commonBaseDAO.list("RecognitionDAO.selectMlpreprocessingChk", paramMap);
		if(!list.isEmpty()) {
			return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMlpreprocessingDataCleansingList", paramMap),
					(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMlpreprocessingDataCleansingListCount", paramMap));
		} else {	
			// 데이터가 없는 경우 - 기본 데이터(DOC_SN : 220000000000000) 조회 처리
			return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMlpreprocessingDataCleansingNoList", paramMap),
					(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMlpreprocessingDataCleansingListNoCount", paramMap));
		}		
	}	
	
	// 데이터 전처리 > 데이터 전처리 적용
	@Transactional
	public ComResultVO precprocessingDataCleansingApply(List<Map<String, Object>> listParamMap) throws Exception {
		ComResultVO comResultVO = new ComResultVO();
		String userId = CommUtils.getUser();
				
		int result = 0;
		int cnt = 0;
		String sv_preprocessing_gubun = null;
		
		for (Map<String, Object> map : listParamMap) {
			map.put("userId", userId);
			
			// 데이터 전처리 > 데이터 정제(Data Cleansing) - 데이터 존재여부 체크
			List<Map<String, Object>> list = this.commonBaseDAO.list("RecognitionDAO.selectMlpreprocessingChk", map);
			if(list.isEmpty()) {   // 데이터가 존재하지 않는 경우
				// 데이터  전처리(TB_AUTOML_PREPROCESSING) 데이터 Insert 처리
				result += this.commonBaseDAO.update("RecognitionDAO.insertPreprocessingData", map);
			}
			
			sv_preprocessing_gubun = map.get("PREPROCESSING_GUBUN").toString();
			if(sv_preprocessing_gubun.equals("중복값 처리")) {			// 중복값 처리
				cnt += (int) this.commonBaseDAO.update("RecognitionDAO.precprocessingDataCleansingDuplocated", map);
		    } else if(sv_preprocessing_gubun.equals("결측값 처리")) {	// 결측값 처리
		    	cnt += (int) this.commonBaseDAO.update("RecognitionDAO.precprocessingDataCleansingMissing", map);
		    } else if(sv_preprocessing_gubun.equals("이상값 처리")) {	// 이상값 처리
		    	cnt += (int) this.commonBaseDAO.update("RecognitionDAO.precprocessingDataCleansingOutlier", map);
		    } else {
		    	cnt += (int) this.commonBaseDAO.update("RecognitionDAO.precprocessingDataCleansingDuplocated", map);
		    }
			
			// 데이터 마스터 목록 <수정> 처리
			//int resultMaster = this.commonBaseDAO.update("RecognitionDAO.precprocessingDataMasterUpdate", map);
		}
		
		if (cnt == listParamMap.size()) {
			comResultVO.setCode(ABOConstant.HTTP_STATUS_CREATE_OK);
		} else {
			comResultVO.setCode(ABOConstant.HTTP_STATUS_SERVER_ERROR);
			comResultVO.setMsg(listParamMap.size() + "건 중 " + cnt + "건을 처리하였습니다. 처리결과를 확인하십시오.");
		}
		
		return comResultVO;
	}		
	
	// 모델 선택.학습 > 분류 모델 처리하기
	@Transactional
	public ComResultVO trainingClassificationModelProcess(Map<String, Object> paramMap) throws Exception {
		int result = 0;
		int trainingCnt = 0;
		
		String userId = CommUtils.getUser();
		String docSn  = paramMap.get("DOC_SN").toString();					//문서번호
		String trainingGubun = paramMap.get("TRAINING_GUBUN").toString();	//학습구분
		
		// 모델 학습 결과(TB_AUTOML_TRAINING_RESULT) 데이터 존재여부 체크
		List<Map<String, Object>> list = this.commonBaseDAO.list("RecognitionDAO.selectTrainingResultChk", paramMap);
		if(list.isEmpty()) {	// 데이터가 존재하지 않는 경우
			// 모델 학습 결과 데이터(TB_AUTOML_TRAINING_RESULT) Insert 처리
			paramMap.put("USER_ID",      userId);
			paramMap.put("TRAINING_CNT", 1);
			
			this.commonBaseDAO.update("RecognitionDAO.insertTrainingResultData", paramMap);
		} else {
			paramMap.put("USER_ID", userId);
			
			// 학습횟수 +1 증가
			final Map<String, Object> entity = (Map<String, Object>) list.get(0);
			trainingCnt = (int) entity.get("TRAINING_CNT") + 1;
			paramMap.put("TRAINING_CNT", trainingCnt);
			
			this.commonBaseDAO.update("RecognitionDAO.updateTrainingResultData", paramMap);	
		}		
		
		// 데이터 마스터 목록 <수정> 처리
		int resultMaster = this.commonBaseDAO.update("RecognitionDAO.dataConfirmProcess", paramMap);
		
		ComResultVO comResultVO = new ComResultVO(resultMaster);
		
		Map<String, Object> mp = new HashMap<String, Object>();
		mp.put("USER_ID", userId);
		mp.put("DOC_SN",  docSn);
		mp.put("METHODS", "recognition");
		
		mp.put("TRAINING_GUBUN", trainingGubun);
		comResultVO.setData(mp);
		
		return comResultVO;
	}		
	
	// 모델 선택.학습 > 군집 모델 처리하기
	@Transactional
	public ComResultVO trainingClusteringModelProcess(Map<String, Object> paramMap) throws Exception {
		int result = 0;
		int trainingCnt = 0;
		
		String userId = CommUtils.getUser();
		String docSn  = paramMap.get("DOC_SN").toString();					//문서번호
		String trainingGubun = paramMap.get("TRAINING_GUBUN").toString();	//학습구분
		
		// 모델 학습 결과(TB_AUTOML_TRAINING_RESULT) 데이터 존재여부 체크
		List<Map<String, Object>> list = this.commonBaseDAO.list("RecognitionDAO.selectTrainingResultChk", paramMap);
		if(list.isEmpty()) {	// 데이터가 존재하지 않는 경우
			// 모델 학습 결과 데이터(TB_AUTOML_TRAINING_RESULT) Insert 처리
			paramMap.put("USER_ID",      userId);
			paramMap.put("TRAINING_CNT", 1);
			
			result += this.commonBaseDAO.update("RecognitionDAO.insertTrainingResultData", paramMap);					
		} else {
			paramMap.put("USER_ID", userId);
			
			// 학습횟수 +1 증가
			final Map<String, Object> entity = (Map<String, Object>) list.get(0);
			trainingCnt = (int) entity.get("TRAINING_CNT") + 1;
			paramMap.put("TRAINING_CNT", trainingCnt);
			
			result += this.commonBaseDAO.update("RecognitionDAO.updateTrainingResultData", paramMap);	
		}		
				
		// 데이터 마스터 목록 <수정> 처리
		int resultMaster = this.commonBaseDAO.update("RecognitionDAO.dataConfirmProcess", paramMap);
				
		ComResultVO comResultVO = new ComResultVO(resultMaster);
		
		Map<String, Object> mp = new HashMap<String, Object>();
		mp.put("USER_ID", userId);
		mp.put("DOC_SN",  docSn);
		mp.put("METHODS", "recognition");
		
		mp.put("TRAINING_GUBUN", trainingGubun);
		comResultVO.setData(mp);
		
		return comResultVO;
	}		
	
	// 모델 평가 > 모델 학습 결과 <조회> 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMlEvaluationResultList(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMlEvaluationResultList", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMlEvaluationResultListCount", paramMap));
	}

	// 모델 평가 > 모델 학습 결과 <모델 확정> 처리
	@Transactional
	public ComResultVO modelEvaluationTrainingResult(Map<String, Object> paramMap) throws Exception {
		// 데이터 마스터 목록 <수정> 처리
		int resultMaster = this.commonBaseDAO.update("RecognitionDAO.dataConfirmProcess", paramMap);
		
		int result = this.commonBaseDAO.update("RecognitionDAO.modelEvaluationTrainingResult", paramMap);
	
		ComResultVO comResultVO = new ComResultVO(result);
		return comResultVO;
	}			

	// 모델 평가 > 모델 학습 결과 <ROC Curve, Confusion Matrix 이미지> 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMlmodelEvaluationImage(Map<String, Object> paramMap) throws Exception {
		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMlmodelEvaluationImage", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMlmodelEvaluationImageCount", paramMap));
	}	
	
	// 모델 평가 > 모델 학습 결과 <모델 학습 결과 목록> 처리
	@Transactional(readOnly = true)
	public ComResultVO selectMlmodelEvaluationList(Map<String, Object> paramMap) throws Exception {
		Map<String, Object> mp = new HashMap<String, Object>();

		return new ComResultVO(this.commonBaseDAO.list("RecognitionDAO.selectMlmodelEvaluationList", paramMap),
				(String) this.commonBaseDAO.selectByPk("RecognitionDAO.selectMlmodelEvaluationListCount", paramMap));
	}	
	
}
