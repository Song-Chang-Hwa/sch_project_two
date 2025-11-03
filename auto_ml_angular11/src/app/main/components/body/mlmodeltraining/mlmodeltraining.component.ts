import { HttpParams } from '@angular/common/http';
import {
    AfterContentInit,
    Component,
    ElementRef,
    OnDestroy,
    OnInit,
    ViewChild,
    ViewEncapsulation,
} from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { ModalDismissReasons } from '@ng-bootstrap/ng-bootstrap';
import { AgGridModule } from 'ag-grid-angular';
import { max, min } from 'date-fns';
import { first } from 'rxjs/operators';
import swal from 'sweetalert2/dist/sweetalert2.js';

import {
    ApigatewayService,
    CommFunction,
    CommService,
    LoggerService,
} from '../../../../shared/services';
import { PageComponent } from '../../../components/page/page.component';

const javascripts = [
    './assets/resources/belltechsoft/advisortypedefinition/advisortypedefinition.js',
    './assets/resources/js/scripts.js',
];

declare var $: any;
declare let window: any;

@Component({
    selector: 'app-mlmodeltraining',
    templateUrl: './mlmodeltraining.component.html',
    styleUrls: ['./mlmodeltraining.component.scss'],
    encapsulation: ViewEncapsulation.None,
})

// 데이터 확인
export class MlmodeltrainingComponent implements OnInit, OnDestroy {
    navigationSubscription: any;
    params: HttpParams;

    testImg: any;

    @ViewChild('fileUpload1') fileUpload1: ElementRef;
    @ViewChild('fileUpload2') fileUpload2: ElementRef;

    pager: any = '';
    rsvSuccess: any = {};
    PAGESIZE = 10; // 총 데이터 건수
    Info: any;

    processStatusCdList: any = [];

    /*calendar*/
    calendar: any;
    calendarEl: any;
    containerEl: any;
    calendarLoding: any = 'N'; // 한번 로딩된 달력은 로딩 하지 않는다.
    resourcesData: any;
    calendarData: any;

    tmpsaveData: any;
    /*calendar*/

    /*CUSTTABLE*/
    @ViewChild('page1') page1: PageComponent;
    OCRTABLETOTCNT = 0;
    CUST_NM: any = '';
    CUST_FOUR_DIGIT_TEL_NO: any = '';
    BRTH_YMD: any = '';

    @ViewChild('page2') page2: PageComponent;
    Type1DetailHeader: any = [];
    Type1DetailHeaderCnt: any = 0;

    @ViewChild('page3') page3: PageComponent;
    OCRTEXTTABLETOTCNT = 0;
    averageScore = '';
    ocrDocTextPageNo: any = 0;

    DOC_SN: any = '';
    GLOBAL_DOC_SN: any = '';
    TRAINING_GUBUN: any = '';

    PAGE_SN: any = '';
    PDF_FILE_NM: any = '';
    SEARCH_PDF_FILE_NM: any = '';
    rsvdtlTableNewData: any = [];

    tmppage1No: any = '';
    tmppage2No: any = '';
    nowDateTime: any = '';

    uploadFileList1: any = [];
    uploadFileList2: any = [];

    OCR_TYPE1: any = 'tabular_ocr_1_1';
    OCR_TYPE2: any = 'tabular_ocr_1_1';
    PGE_RANGE1: any = '1';
    PGE_RANGE2: any = '1';
    TBL_NO1: any = '1';
    TBL_NO2: any = '1';
    BUSINESS_NM: any = '';

    addHeaderData: any = '';
    selectseq: any = '';
    selectseq2: any = '';
    selecttxt: any = '';
    selectdtxt: any = '';
    searchtxt: any = '';
    searchBusinessNm: any = '';
    searchStatCd: any = '';
    searchCondCd: any = '';

    OcrDocMstData: any[];
    OcrDocDetailData: any;
    OcrDocTextData: any[];
    OcrDocDetailListData: any;
    OcrDocDetailImgFileData: any[];
    OcrDocDetailHeaderCount: any;
    tblSno: any = '';
    pgSn: any = '';

    type42ImgFileNm1 = '';
    type42ImgFileNm2 = '';

    STAT_CD: any = '';
    mstPageNo: any = ''; // 마스터 현재 페이지 번호

    trainingMsg: any = '';
    trainingResultMsg: any = '';

    constructor(
        private router: Router,
        private apigatewayService: ApigatewayService,
        private logger: LoggerService,
        private cf: CommFunction,
        private cs: CommService
    ) {
        window.mlmodeltraining = this;
        this.navigationSubscription = this.router.events.subscribe((e: any) => {
            // RELOAD로 설정했기 때문에 동일한 라우트로 요청이 되더라도
            // 네비게이션 이벤트가 발생한다.
            if (e instanceof NavigationEnd) {
                this.initialiseInvites();
            }
        });
    }

    initialiseInvites() {
        const pageNo = this.cf.nvl(this.cf.getParam('page'), '1');
        const page_target = this.cf.nvl(this.cf.getParam('page_target'), 'page1');

        console.log('initialiseInvites pageNo : ' + pageNo + ', page_target : ' + page_target);

        if (page_target == 'page1') {
            this.onSearchOcrDocMstList(pageNo);
        } else if (page_target == 'page3') {
            // this.onSelectOcrDocTextPaging(pageNo);
        }
    }

    ngOnInit() {
        this.cs.getCodelist('PROCESS_STATUS').then(data => {
            this.processStatusCdList = data;
        });
        this.onSearchOcrDocMstList('1');
    }

    ngOnDestroy() {
        // 이벤트 해지
        if (this.navigationSubscription) {
            this.navigationSubscription.unsubscribe();
        }
    }

    // (좌측 화면) : 데이터 마스터 목록 <조회> 처리
    onSearchOcrDocMstList(pageNo: any) {
        this.mstPageNo = pageNo;

        this.type42ImgFileNm1 = '';
        this.type42ImgFileNm2 = '';

        const serviceUrl = 'recognition/selectAutomlMasterList';

        this.params = this.cf.toHttpParams({
            FILE_NM: this.searchtxt,
            STAT_CD: this.searchStatCd,
            BUSINESS_NM: this.searchBusinessNm,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 10,
            FUCTION_GUBUN: '20', // 처리상태 코드 : 20(모델 학습)
        });

        this.OcrDocMstData = [];
        this.OcrDocDetailData = undefined;
        this.OcrDocDetailImgFileData = undefined;
        if (pageNo == '0') this.OCRTABLETOTCNT = 0;
        this.OCRTEXTTABLETOTCNT = 0;
        this.searchCondCd = '';
        this.averageScore = '';
        this.DOC_SN = '';

        this.tblSno = '';
        this.pgSn = '';

        if (pageNo == '0') this.onResetPage1();

        $('#automlConfusionMatrix').empty();
        $('#automlRocCurve').empty();

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                console.log(resultData);
                let tmp;
                if (resultData.code === 200) {
                    this.OcrDocMstData = resultData.data;
                }
                tmp =
                    '        <colgroup>                                                     ' +
                    /*  '            <col style="width: 10px;">                              ' + */
                    /*  '            <col style="width: auto;">                              ' + */
                    '            <col style="width: 680px;">                                ' +
                    '            <col style="width: 160px;">                                ' +
                    '            <col style="width: 160px;">                                ' +
                    '            <col style="width:  70px;">                                ' +
                    '        </colgroup>                                                    ' +
                    '        <thead>                                                        ' +
                    '	     <tr>                                                           ' +
                    /* '            <th>순번</th>                                            ' + */
                    '            <th>문서 명</th>                                             ' +
                    '            <th>처리상태</th>                                            ' +
                    '            <th>등록일</th>                                             ' +
                    '            <th>선택</th>                                               ' +
                    '	    </tr>                                                           ' +
                    '        </thead>                                                       ' +
                    '        <tbody>                                                        ';

                if (resultData.code === 200) {
                    // this.rsvList = resultData;

                    if (resultData.data.length > 0) {
                        let i = 0;
                        $.each(resultData.data, (index: any, item: any) => {
                            const cdNm = (tmp += '<tr>  ');
                            /*
                            tmp +=
                                '                    <td>                                   ' +
                                item.DOC_SN +
                                '                    </td>                                  ';
                                 */
                            tmp +=
                                '                    <td class="left">                      ' +
                                item.DOC_NM +
                                '                    </td>                                  ';
                            tmp +=
                                '                    <td class="center">                    ' +
                                item.STAT_CD_NM +
                                '                    </td>                                  ';
                            tmp +=
                                '                    <td class="left">                      ' +
                                item.REGI_DTTM +
                                '                    </td>                                  ';
                            tmp +=
                                '<td><a href="javascript:void(0);" onClick="window.mlmodeltraining.onSelectOcrDocDetail(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                i +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.DOC_SN +
                                // tslint:disable-next-line: prettier
                                 '\',\'' +
                                item.STAT_CD +
                                // tslint:disable-next-line: prettier
                                '\');" class="btn btn-primary btn-xs btn-outline btn-fit">선택</a></td>';
                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#ocrDocMst').html(tmp);
                        });

                        this.OCRTABLETOTCNT = resultData.dataCount;
                        this.page1.setInitPageLoad(
                            'page',
                            resultData.dataCount,
                            pageNo,
                            'mlmodeltraining',
                            { target: 'page1' },
                            10 // this.PAGESIZE
                        );
                    } else {
                        $('#ocrDocMst').html(
                            '<div class="search_result"><h4>등록된 정보가 없습니다.</h4></div>'
                        );
                    }
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // (우측 화면) : 분류 모델 처리하기
    onSearchClassificationModel(trainingGubun: any) {
        this.DOC_SN = this.GLOBAL_DOC_SN;
        if (this.GLOBAL_DOC_SN == null || this.GLOBAL_DOC_SN == '') {
            swal.fire('먼저 [학습할 문서]를 선택하세요.', '', 'warning');
            return;
        }

        $('#automlConfusionMatrix').empty();
        $('#automlRocCurve').empty();

        this.TRAINING_GUBUN = trainingGubun; // 학습 구분 - 10 : 의사결정트리, 11: Random Forest, 12:XGBoot, 13:SVM, 14:신경망

        this.onSearchClassificationModelPaging('1', trainingGubun);
    }

    // (우측 화면) : 분류 모델 처리하기
    onSearchClassificationModelPaging(pageNo: any, trainingGubun: any) {
        this.TRAINING_GUBUN = trainingGubun;

        const data = {
            DOC_SN: this.DOC_SN,
            TRAINING_GUBUN: this.TRAINING_GUBUN,
            STAT_CD: '20', // 처리상태 : 20(모델학습)
        };

        if (this.TRAINING_GUBUN == '10' || this.TRAINING_GUBUN == '10') {
            this.trainingMsg = '[분류 모델] - 그래디언트 부스팅을 학습하시겠습니까?';
            this.trainingResultMsg =
                '[분류 모델] - 그래디언트 부스팅 학습이 정상적으로 처리 되었습니다.';
        } else if (this.TRAINING_GUBUN == '11' || this.TRAINING_GUBUN == '11') {
            this.trainingMsg = '[분류 모델] - 의사결정트리를 학습하시겠습니까?';
            this.trainingResultMsg =
                '[분류 모델] - 의사결정트리 학습이 정상적으로 처리 되었습니다.';
        } else if (this.TRAINING_GUBUN == '12' || this.TRAINING_GUBUN == '12') {
            this.trainingMsg = '[분류 모델] - Random Forest를 학습하시겠습니까?';
            this.trainingResultMsg =
                '[분류 모델] - Random Forest 학습이 정상적으로 처리 되었습니다.';
        } else if (this.TRAINING_GUBUN == '13' || this.TRAINING_GUBUN == '13') {
            this.trainingMsg = '[분류 모델] - SVM을 학습하시겠습니까?';
            this.trainingResultMsg = '[분류 모델] - SVM 학습이 정상적으로 처리 되었습니다.';
        } else if (this.TRAINING_GUBUN == '14' || this.TRAINING_GUBUN == '14') {
            this.trainingMsg = '[분류 모델] - 신경망을 학습하시겠습니까?';
            this.trainingResultMsg = '[분류 모델] - 신경망 학습이 정상적으로 처리 되었습니다.';
        } else {
            this.trainingMsg = '[분류 모델] - 그래디언트 부스팅을 학습하시겠습니까?';
            this.trainingResultMsg =
                '[분류 모델] - 그래디언트 부스팅 학습이 정상적으로 처리 되었습니다.';
        }

        swal.fire({
            title: this.trainingMsg,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            if (result.value) {
                this.apigatewayService
                    .doPost('recognition/trainingClassificationModelProcess', data, null)
                    .subscribe(
                        resultData => {
                            if (resultData.code === 200) {
                                swal.fire(this.trainingResultMsg, '', 'success').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocTextPaging(
                                        this.ocrDocTextPageNo,
                                        this.GLOBAL_DOC_SN
                                    );
                                });
                            } else {
                                swal.fire(resultData.msg, '', 'info').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocTextPaging(
                                        this.ocrDocTextPageNo,
                                        this.GLOBAL_DOC_SN
                                    );
                                });
                            }
                        },
                        error => {
                            this.logger.debug(JSON.stringify(error, null, 4));
                            swal.fire('[분류 모델] 학습 처리 실패', '', 'error');
                        }
                    );
            } // confirm yes
        });
    }

    // (우측 화면) : 군집 모델 처리하기
    onSearchClusteringModel(trainingGubun: any) {
        this.DOC_SN = this.GLOBAL_DOC_SN;
        if (this.GLOBAL_DOC_SN == null || this.GLOBAL_DOC_SN == '') {
            swal.fire('먼저 [학습할 문서]를 선택하세요.', '', 'warning');
            return;
        }

        $('#automlConfusionMatrix').empty();
        $('#automlRocCurve').empty();

        this.TRAINING_GUBUN = trainingGubun; // 학습 구분 - 20 : K-means Clustering

        this.onSearchClusteringModelPaging('1', trainingGubun);
    }

    // (우측 화면) : 군집 모델 처리하기
    onSearchClusteringModelPaging(pageNo: any, trainingGubun: any) {
        this.TRAINING_GUBUN = trainingGubun;

        const data = {
            DOC_SN: this.DOC_SN,
            TRAINING_GUBUN: this.TRAINING_GUBUN,
            STAT_CD: '20', // 처리상태 : 20(모델학습)
        };

        if (this.TRAINING_GUBUN == '20' || this.TRAINING_GUBUN == '20') {
            this.trainingMsg = '[군집 모델] - K-평균 군집화를 학습하시겠습니까?';
            this.trainingResultMsg =
                '[군집 모델] - K-평균 군집화 학습이 정상적으로 처리 되었습니다.';
        } else {
            this.trainingMsg = '[군집 모델] - K-평균 군집화를 학습하시겠습니까?';
            this.trainingResultMsg =
                '[군집 모델] - K-평균 군집화 학습이 정상적으로 처리 되었습니다.';
        }

        swal.fire({
            title: this.trainingMsg,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            if (result.value) {
                this.apigatewayService
                    .doPost('recognition/trainingClusteringModelProcess', data, null)
                    .subscribe(
                        resultData => {
                            if (resultData.code === 200) {
                                swal.fire(this.trainingResultMsg, '', 'success').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocTextPaging(
                                        this.ocrDocTextPageNo,
                                        this.GLOBAL_DOC_SN
                                    );
                                });
                            } else {
                                swal.fire(resultData.msg, '', 'info').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocTextPaging(
                                        this.ocrDocTextPageNo,
                                        this.GLOBAL_DOC_SN
                                    );
                                });
                            }
                        },
                        error => {
                            this.logger.debug(JSON.stringify(error, null, 4));
                            swal.fire('[군집 모델] 학습 처리 실패', '', 'error');
                        }
                    );
            } // confirm yes
        });
    }

    // (우측 화면) : 모델 학습 결과 <조회> 처리
    onSelectOcrDocDetail(seq: any, DOC_SN: any, STAT_CD: any) {
        this.DOC_SN = DOC_SN;
        this.STAT_CD = STAT_CD;

        this.GLOBAL_DOC_SN = DOC_SN;

        $('#automlTrainingList').empty();
        $('#automlConfusionMatrix').empty();
        $('#automlRocCurve').empty();

        this.selected(seq);
        this.onSelectOcrDocTextPaging('1', DOC_SN);
    }

    // (우측 화면) : 모델 학습 결과 <조회> 처리
    onSelectOcrDocTextPaging(pageNo: any, DOC_SN: any) {
        const serviceUrl = 'recognition/selectMlEvaluationResultList';

        this.params = this.cf.toHttpParams({
            DOC_SN,
            PAGE_SN: this.PAGE_SN,
            COND_CD: this.searchCondCd,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 10,
        });

        if (pageNo == '0') this.OCRTEXTTABLETOTCNT = 0;
        if (pageNo == '0') this.onResetPage3();

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                console.log(resultData);
                if (resultData.code === 200) {
                    this.OcrDocTextData = resultData.data;
                }
                tmp =
                    '        <colgroup>                                                       ' +
                    '            <col style="width: auto%;">                                  ' +
                    '            <col style="width: 200px;">                                  ' +
                    '            <col style="width: 200px;">                                  ' +
                    '            <col style="width: 200px;">                                  ' +
                    '            <col style="width: 200px;">                                  ' +
                    '            <col style="width: 200px;">                                  ' +
                    '            <col style="width:  70px;">                                  ' +
                    '        </colgroup>                                                      ' +
                    '        <thead>                                                          ' +
                    '	     <tr>                                                             ' +
                    '            <th>학습 구분</th>                                              ' +
                    '            <th>정밀도</th>                                                ' +
                    '            <th>민감도</th>                                                ' +
                    '            <th>F1-score</th>                                            ' +
                    '            <th>학습일자</th>                                              ' +
                    '            <th>학습횟수</th>                                              ' +
                    '            <th>선택</th>                                                 ' +
                    '	    </tr>                                                             ' +
                    '        </thead>                                                         ' +
                    '        <tbody>                                                          ';

                if (resultData.code === 200) {
                    if (resultData.data.length > 0) {
                        let i = 0;
                        $.each(resultData.data, (index: any, item: any) => {
                            tmp += '<tr>  ';

                            tmp +=
                                '                    <td class="left" style="white-space:pre;">' +
                                item.TRAINING_GUBUN_NM +
                                '</td>';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.PRECISION_RATE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.RECALL_RATE +
                                '                    </td>                                    ';

                            tmp +=
                                '                    <td class="right">                      ' +
                                item.F1_SCORE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="center">                      ' +
                                item.TRAINING_DTTM +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="center">                         ' +
                                item.TRAINING_CNT +
                                '                    </td>                                       ';
                            tmp +=
                                '<td><a href="javascript:void(0);" onClick="window.mlmodeltraining.onDisplayTrainingResult(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                i +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.DOC_SN +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.TRAINING_GUBUN +
                                // tslint:disable-next-line: prettier
                                '\');" class="btn btn-primary btn-xs btn-outline btn-fit">선택</a></td>';

                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#automlTrainingResult').html(tmp);
                        });

                        this.OCRTEXTTABLETOTCNT = resultData.dataCount;
                        // this.page3.setInitPageLoad(
                        //    'page',
                        //    resultData.dataCount,
                        //    pageNo,
                        //    'mlmodeltraining',
                        //    { target: 'page3' },
                        //    16 // this.PAGESIZE
                        // );
                    } else {
                        $('#automlTrainingResult').html(
                            '<div class="search_result"><h4>등록된 정보가 없습니다.</h4></div>'
                        );
                    }
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // (우측 화면) : 1)모델 학숩 결과, 2) 분석 결과 평가 지표
    onDisplayTrainingResult(seq: any, DOC_SN: any, TRAINING_GUBUN: any) {
        this.DOC_SN = DOC_SN;
        this.TRAINING_GUBUN = TRAINING_GUBUN;

        const targetRow = this.OcrDocMstData.find(item => item.DOC_SN == this.DOC_SN);

        this.onDisplayConfusionMatrixImagePaging('1');
        this.onDisplayRocCurveImage(this.DOC_SN, this.TRAINING_GUBUN);
    }

    // (우측 화면 - 상단) : Confusion Matrix 이미지
    onDisplayConfusionMatrixImagePaging(pageNo: any) {
        const serviceUrl = 'recognition/selectMlmodelEvaluationImage';

        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            TRAINING_GUBUN: this.TRAINING_GUBUN,
            IMAGE_GUBUN: '20',
            TEXT_SN: 1,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 5,
        });

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                if (resultData.code === 200) {
                    this.OcrDocTextData = resultData.data;
                }

                if (resultData.code === 200) {
                    if (resultData.data.length > 0) {
                        let i = 0;
                        $.each(resultData.data, (index: any, item: any) => {
                            tmp += '<tr>  ';

                            tmp +=
                                '<td class="nopadding"> <a data-title="' +
                                item.FILE_NM +
                                '" href="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" data-lightbox="automlTrainingImage"><img style="max-height:200px;" src="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" class="mCS_img_loaded" /></a></td>';

                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#automlConfusionMatrix').html(tmp);
                        });
                    } else {
                        $('#automlConfusionMatrix').html(
                            '<div class="search_result"><h4>등록된 정보가 없습니다.</h4></div>'
                        );
                    }
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // (우측 화면 - 하단) : ROC Curve
    onDisplayRocCurveImage(DOC_SN: any, TRAINING_GUBUN: any) {
        this.DOC_SN = DOC_SN;
        this.TRAINING_GUBUN = TRAINING_GUBUN;

        // const targetRow = this.OcrDocMstData.find(item => item.DOC_SN == this.DOC_SN);

        // alert(this.DOC_SN);
        // alert(this.TRAINING_GUBUN);

        this.onDisplayRocCurveImagePaging('1');
    }

    onDisplayRocCurveImagePaging(pageNo: any) {
        const serviceUrl = 'recognition/selectMlmodelEvaluationImage';

        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            TRAINING_GUBUN: this.TRAINING_GUBUN,
            IMAGE_GUBUN: '10',
            TEXT_SN: 1,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 5,
        });

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                if (resultData.code === 200) {
                    this.OcrDocTextData = resultData.data;
                }

                if (resultData.code === 200) {
                    if (resultData.data.length > 0) {
                        let i = 0;
                        $.each(resultData.data, (index: any, item: any) => {
                            tmp += '<tr>  ';

                            tmp +=
                                '<td class="nopadding"> <a data-title="' +
                                item.FILE_NM +
                                '" href="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" data-lightbox="automlTrainingImage"><img style="max-height:190px;" src="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" class="mCS_img_loaded" /></a></td>';

                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#automlRocCurve').html(tmp);
                        });
                    } else {
                        $('#automlRocCurve').html(
                            '<div class="search_result"><h4>등록된 정보가 없습니다.</h4></div>'
                        );
                    }
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // 데이터 마스터 목록 <조회> - 페이징 처리
    onResetPage1() {
        $('#ocrDocMst').empty();
        this.OCRTABLETOTCNT = 0;
        if (this.page1) {
            this.page1.setInitPageLoad(
                'page',
                0,
                1,
                'mlmodeltraining',
                { target: 'page1' },
                10 // this.PAGESIZE
            );
        }
    }

    // 데이터 상세 목록 <조회> - 페이징 처리
    onResetPage3() {
        $('#ocrDocText').empty();
        this.OCRTEXTTABLETOTCNT = 0;
        this.averageScore = '';
        if (this.page3) {
            this.ocrDocTextPageNo = 1;
            this.page3.setInitPageLoad(
                'page',
                0,
                1,
                'mlmodeltraining',
                { target: 'page3' },
                7 // this.PAGESIZE
            );
        }
    }

    selected(seq: any) {
        this.selectseq = seq;
        $('#ocrDocMst>tbody tr').each(function (index, item) {
            $(item).removeClass('selectcell');
        });
        $('#ocrDocMst>tbody').find('tr').eq(seq).addClass('selectcell');
    }
}
