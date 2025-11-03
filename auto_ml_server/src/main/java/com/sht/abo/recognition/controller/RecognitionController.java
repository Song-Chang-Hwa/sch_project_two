package com.sht.abo.recognition.controller;



import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import com.sht.abo.recognition.service.RecognitionService;
import com.sht.abo.vo.ComResultVO;
import com.sht.util.CommUtils;

/**
 * Auto Machine Learning
 * 
 * @author : Song Chang Hwa
 *
 */
@RestController
@RequestMapping("/recognition")
public class RecognitionController {

	private static final Logger logger = LoggerFactory.getLogger(RecognitionController.class);
	
	@Autowired
	private RecognitionService recognitionService;
		
	// 데이터 읽어 들이기 > 데이터 마스터 목록 [조회] 처리
	@RequestMapping(value="/selectAutomlMasterList", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectAutomlMasterList(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectAutomlMasterList(paramMap);
    }	
		
	// 데이터 읽어 들이기 > 데이터 상세 목록 [조회] 처리
	@RequestMapping(value="/selectAutomlDatareadColumnInfo", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectAutomlDatareadColumnInfo(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectAutomlDatareadColumnInfo(paramMap);
    }	    	
	
	// 데이터 읽어 들이기 > 엑셀 파일 업로드
	@RequestMapping(value="/automlDatareadUpload", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO automlDatareadUpload(MultipartHttpServletRequest multipartHttpServletRequest) throws Exception{
    	ComResultVO rs = this.recognitionService.automlDatareadUpload(multipartHttpServletRequest);
    	
    	// 데이터 읽어 들이기 - Python 처리
    	if(rs.getCode() == 200) {
    		rs = this.recognitionService.pythinExecAutomlDataread((Map)rs.getData());
    	}

    	// 데이터 확인 - Python 처리 : 이미지 생성
    	if(rs.getCode() == 200) {
    		rs = this.recognitionService.pythinAutomlDataconfirm((Map)rs.getData());
    	}
    	
    	return new ComResultVO();
    }	
	
	// 데이터 읽어 들이기 > 데이터 마스터 목록 [삭제] 처리
	@RequestMapping(value="/deleteAutomlMst", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO deleteAutomlMst(@RequestBody Map<String, Object> paramMap) throws Exception{
    	return this.recognitionService.deleteAutomlMst(paramMap);
    }	

	// 데이터 확인 > 데이터 컬럼 상세 목록 [조회] 처리
	@RequestMapping(value="/selectMldataConfirmList", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMldataConfirmList(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMldataConfirmList(paramMap);
    }		
	
	// 데이터 확인 > 02:데이터 분포 (Boxplot), 03:정규분포 (Normal Distribution) 처리
	@RequestMapping(value="/selectMldataConfirmTextImage", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMldataConfirmTextImage(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMldataConfirmTextImage(paramMap);
    }		
		
	// 데이터 확인 > 데이터 마스터 목록 <수정> 처리
	@RequestMapping(value="/dataConfirmProcess", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO dataConfirmProcess(@RequestBody Map<String, Object> paramMap) throws Exception{
    	return this.recognitionService.dataConfirmProcess(paramMap);
    }	
	
	// 데이터 전처리 > 목표변수 적용
	@RequestMapping(value="/precprocessingTargetApply", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO precprocessingTargetApply(@RequestBody List<Map<String, Object>> listParamMap) throws Exception{
    	return recognitionService.precprocessingTargetApply(listParamMap);
    }	
	
	// 데이터 전처리 > 데이터 정제(Data Cleansing) 조회 처리
	@RequestMapping(value="/selectMlpreprocessingDataCleansingList", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMlpreprocessingDataCleansingList(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMlpreprocessingDataCleansingList(paramMap);
    }		
		
	// 데이터 전처리 > 데이터 전처리 적용
	@RequestMapping(value="/precprocessingDataCleansingApply", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO precprocessingDataCleansingApply(@RequestBody List<Map<String, Object>> listParamMap) throws Exception{
    	return this.recognitionService.precprocessingDataCleansingApply(listParamMap);
    }		
	
	// 모델 선택.학습 > 분류 모델 처리하기
	@RequestMapping(value="/trainingClassificationModelProcess", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO trainingClassificationModelProcess(@RequestBody Map<String, Object> paramMap) throws Exception{
		ComResultVO rs = this.recognitionService.trainingClassificationModelProcess(paramMap);
		
		// 모델 선택.학습 > 분류 모델 - Python 처리
    	if(rs.getCode() == 200) {
    		rs = this.recognitionService.pythonTrainingClassificationModelProcess((Map)rs.getData());
    	}
		
    	return new ComResultVO();
	}			
	
	// 모델 선택.학습 > 군집 모델 처리하기
	@RequestMapping(value="/trainingClusteringModelProcess", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO trainingClusteringModelProcess(@RequestBody Map<String, Object> paramMap) throws Exception{
		ComResultVO rs = this.recognitionService.trainingClusteringModelProcess(paramMap);
		
		// 모델 선택.학습 > 분류 모델 - Python 처리
    	if(rs.getCode() == 200) {
    		rs = this.recognitionService.pythonTrainingClusteringModelProcess((Map)rs.getData());
    	}
		
    	return new ComResultVO();
	}			
		
	// 모델 평가 > 모델 학습 결과 <조회> 처리
	@RequestMapping(value="/selectMlEvaluationResultList", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMlEvaluationResultList(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMlEvaluationResultList(paramMap);
    }			
		
	// 모델 평가 > 모델 학습 결과 <모델 확정> 처리
	@RequestMapping(value="/modelEvaluationTrainingResult", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
    public ComResultVO modelEvaluationTrainingResult(@RequestBody Map<String, Object> paramMap) throws Exception{
    	return this.recognitionService.modelEvaluationTrainingResult(paramMap);
    }		
	
	// 모델 평가 > 모델 학습 결과 <ROC Curve, Confusion Matrix 이미지> 처리
	@RequestMapping(value="/selectMlmodelEvaluationImage", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMlmodelEvaluationImage(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMlmodelEvaluationImage(paramMap);
    }			
		
	// 모델 평가 > 모델 학습 결과 <모델 학습 결과 목록> 처리
	@RequestMapping(value="/selectMlmodelEvaluationList", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
	public ComResultVO selectMlmodelEvaluationList(HttpServletRequest request, @RequestParam Map<String, Object> paramMap) throws Exception{
    	String userId = CommUtils.getUser();

    	// paramMap의 pageNo PAGESIZE 페이지 세팅을 해준다
    	paramMap.put("userId", userId);
    	CommUtils.setPageMap(paramMap);
    	
    	return recognitionService.selectMlmodelEvaluationList(paramMap);
    }					
	
}