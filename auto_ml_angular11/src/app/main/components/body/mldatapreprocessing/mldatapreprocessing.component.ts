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
    selector: 'app-mldatapreprocessing',
    templateUrl: './mldatapreprocessing.component.html',
    styleUrls: ['./mldatapreprocessing.component.scss'],
    encapsulation: ViewEncapsulation.None,
})

// 데이터 확인
export class MldatapreprocessingComponent implements OnInit, OnDestroy {
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
    OCRTEXTTABLETOTCNT = 0;
    ocrDocTextPageNo: any = 0;

    DOC_SN: any = '';
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

    PreprocessingCleansingData: any[];

    tblSno: any = '';
    pgSn: any = '';

    type42ImgFileNm1 = '';
    type42ImgFileNm2 = '';

    GLOBAL_DOC_SN: any = '';
    targetVallueYnAll: any = false; // 목표변수 선택 변수
    removeYnAll: any = false; // 제거여부 선택 변수
    useYnAll: any = false; // 사용여부 선택 변수
    mstPageNo: any = ''; // 마스터 현재 페이지 번호

    constructor(
        private router: Router,
        private apigatewayService: ApigatewayService,
        private logger: LoggerService,
        private cf: CommFunction,
        private cs: CommService
    ) {
        window.mldatapreprocessing = this;
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
        } else if (page_target == 'page2') {
            this.onSelectOcrDocTextPaging(pageNo, this.DOC_SN);
            // this.onPreprocessingSettingPaging(pageNo, this.DOC_SN);
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
            FUCTION_GUBUN: '11', // 처리상태 코드 : 11(데이터 전처리)
        });

        this.OcrDocMstData = [];
        this.OcrDocDetailData = undefined;
        this.OcrDocDetailImgFileData = undefined;
        this.OcrDocTextData = undefined;
        if (pageNo == '0') this.OCRTABLETOTCNT = 0;
        this.OCRTEXTTABLETOTCNT = 0;
        this.searchCondCd = '';
        this.DOC_SN = '';

        this.tblSno = '';
        this.pgSn = '';

        if (pageNo == '0') this.onResetPage1();

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
                                '<td><a href="javascript:void(0);" onClick="window.mldatapreprocessing.onSelectOcrDocDetail(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                i +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.DOC_SN +
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
                            'mldatapreprocessing',
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

    // (우측 화면) : 데이터 상세 목록 <조회> 처리
    onSelectOcrDocDetail(seq: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;
        this.GLOBAL_DOC_SN = DOC_SN;

        const targetRow = this.OcrDocMstData.find(item => item.DOC_SN == this.DOC_SN);

        this.selected(seq);
        this.onSelectOcrDocTextPaging('1', this.DOC_SN);

        this.onPreprocessingSetting(this.DOC_SN);
    }

    // (우측 화면) : 데이터 컬럼 상세 목록 - 칼럼별 데이터 분석 결과 <조회> 처리
    onSelectOcrDocTextPaging(pageNo: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;

        const serviceUrl = 'recognition/selectMldataConfirmList';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            PAGE_SN: this.PAGE_SN,
            COND_CD: this.searchCondCd,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 10,
        });

        this.OcrDocTextData = undefined;
        if (pageNo == '0') this.OCRTEXTTABLETOTCNT = 0;

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                if (resultData.code === 200) {
                    this.OcrDocTextData = resultData.data;

                    if (resultData.data.length > 0) {
                        this.OCRTEXTTABLETOTCNT = resultData.dataCount;
                        this.page2.setInitPageLoad(
                            'page',
                            resultData.dataCount,
                            pageNo,
                            'mldatapreprocessing',
                            { target: 'page2' },
                            10 // this.PAGESIZE
                        );
                    }

                    this.targetVallueYnAll = false;
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // 목표변수 선택 변수 처리
    changeTargetValueYnAll() {
        this.OcrDocTextData.forEach(data => {
            data.TARGET_VALUE_YN = this.targetVallueYnAll;
        });
    }

    // 제거여부 선택 변수 처리
    changeRemoveYnYnAll() {
        this.PreprocessingCleansingData.forEach(data => {
            data.REMOVE_YN = this.removeYnAll;
        });
    }

    // 사용여부 선택 변수 처리
    changeUseYnYnAll() {
        this.PreprocessingCleansingData.forEach(data => {
            data.USE_YN = this.useYnAll;
        });
    }

    // (우측화면) 목표변수 적용
    onPrecprocessingTargetApply() {
        this.DOC_SN = this.GLOBAL_DOC_SN;
        if (this.GLOBAL_DOC_SN == null || this.GLOBAL_DOC_SN == '') {
            swal.fire('먼저 [데이터 전처리할 문서]를 선택하세요.', '', 'warning');
            return;
        }

        if (this.OcrDocTextData == null || this.OcrDocTextData.length === 0) {
            swal.fire('[목표변수 적용]할 대상이 없습니다.', '', 'warning');
            return;
        }

        let targetValue_cnt = 0;
        const ocrDocTextUpdateData = [];
        this.OcrDocTextData.forEach(data => {
            if (data.ORG_TARGET_VALUE_YN != data.TARGET_VALUE_YN) {
                ocrDocTextUpdateData.push(data);

                targetValue_cnt = targetValue_cnt + 1;
            }
        });

        if (ocrDocTextUpdateData.length === 0) {
            swal.fire('[목표변수 적용]할 대상이 없습니다.', '', 'warning');
            return;
        }

        // alert(targetValue_cnt);
        if (targetValue_cnt > 1) {
            swal.fire('[목표변수]는 1 칼럼만 선택하셔야 합니다.', '', 'warning');
            return;
        }

        swal.fire({
            title: '[목표변수 적용] 처리를 하시겠습니까?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            if (result.value) {
                this.apigatewayService
                    .doPost('recognition/precprocessingTargetApply', ocrDocTextUpdateData, null)
                    .subscribe(
                        resultData => {
                            if (resultData.code === 201) {
                                swal.fire(
                                    '[목표변수 적용]이 정상적으로 처리 되었습니다.',
                                    '',
                                    'success'
                                ).then(result => {
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

                            this.targetVallueYnAll = false;
                        },
                        error => {
                            this.logger.debug(JSON.stringify(error, null, 4));
                            swal.fire('[목표변수 적용] 실패', '', 'error');
                        }
                    );
            }
        });
    }

    // (우측 화면 - 하단) : 데이터 정제(Data Cleansing) 처리
    onPreprocessingSetting(DOC_SN: any) {
        this.DOC_SN = DOC_SN;

        const targetRow = this.OcrDocMstData.find(item => item.DOC_SN == this.DOC_SN);

        this.onPreprocessingSettingPaging('1', this.DOC_SN);
    }

    // (우측 화면 - 하단) : 데이터 정제(Data Cleansing) 처리
    onPreprocessingSettingPaging(pageNo: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;

        const serviceUrl = 'recognition/selectMlpreprocessingDataCleansingList';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            PAGE_SN: this.PAGE_SN,
            COND_CD: this.searchCondCd,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 3,
        });

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                if (resultData.code === 200) {
                    this.PreprocessingCleansingData = resultData.data;

                    this.removeYnAll = false;
                    this.useYnAll = false;
                }
            },
            error => {
                this.logger.debug(JSON.stringify(error, null, 4));
            }
        );
    }

    // (우측화면 - 하단) 데이터 전처리 적용
    onPrecprocessingDataCleansingApply() {
        const cleasingDocSN = this.DOC_SN;

        const cleansingUpdateData = [];

        if (
            this.PreprocessingCleansingData == null ||
            this.PreprocessingCleansingData.length === 0
        ) {
            swal.fire('[데이터 전처리 적용]할 대상이 없습니다.', '', 'warning');
            return;
        }

        this.PreprocessingCleansingData.forEach(data => {
            if (data.ORG_REMOVE_YN != data.REMOVE_YN) {
                cleansingUpdateData.push(data);
            } else if (data.ORG_USE_YN != data.USE_YN) {
                cleansingUpdateData.push(data);
            } else {
            }
        });

        if (cleansingUpdateData.length === 0) {
            swal.fire('[데이터 전처리 적용]할 대상이 없습니다.', '', 'warning');
            return;
        }

        swal.fire({
            title: '[데이터 전처리] 작업을 하시겠습니까?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            // confirm yes
            if (result.value) {
                this.apigatewayService
                    .doPost(
                        'recognition/precprocessingDataCleansingApply',
                        cleansingUpdateData,
                        null
                    )
                    .subscribe(
                        resultData => {
                            if (resultData.code === 201) {
                                swal.fire(
                                    '[데이터 전처리] 작업이 정상적으로 처리 되었습니다.',
                                    '',
                                    'success'
                                ).then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocDetail(this.ocrDocTextPageNo, cleasingDocSN);
                                });
                            } else {
                                swal.fire(resultData.msg, '', 'info').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                    this.onSelectOcrDocDetail(this.ocrDocTextPageNo, cleasingDocSN);
                                });
                            }
                        },
                        error => {
                            this.logger.debug(JSON.stringify(error, null, 4));
                            swal.fire('[데이터 전처리 적용] 실패', '', 'error');
                        }
                    );
            } // confirm yes
        });
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
                'mldatapreprocessing',
                { target: 'page1' },
                10 // this.PAGESIZE
            );
        }
    }

    // 데이터 상세 목록 - 칼럼별 데이터 분석 결과 <조회> - 페이징 처리
    onResetPage2() {
        $('#ocrDocText').empty();
        this.OCRTEXTTABLETOTCNT = 0;
        if (this.page2) {
            this.ocrDocTextPageNo = 1;
            this.page2.setInitPageLoad(
                'page',
                0,
                1,
                'mldatapreprocessing',
                { target: 'page2' },
                10 // this.PAGESIZE
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

    numberOnly(event): boolean {
        const charCode = event.which ? event.which : event.keyCode;
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    }
}
