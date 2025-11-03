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
    selector: 'app-mldataconfirm',
    templateUrl: './mldataconfirm.component.html',
    styleUrls: ['./mldataconfirm.component.scss'],
    encapsulation: ViewEncapsulation.None,
})

// 데이터 확인
export class MldataconfirmComponent implements OnInit, OnDestroy {
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
    ocrDocTextPageNo: any = 0;

    DOC_SN: any = '';
    STAT_CD: any = '';
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

    mstPageNo: any = ''; // 마스터 현재 페이지 번호
    COLUMN_SN: any = ''; // boxplot 컬럼번호
    AutomlBoxplotImageData: any;
    AutomlDistributionImageData: any;

    constructor(
        private router: Router,
        private apigatewayService: ApigatewayService,
        private logger: LoggerService,
        private cf: CommFunction,
        private cs: CommService
    ) {
        window.mldataconfirm = this;
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
            FUCTION_GUBUN: '10', // 처리상태 코드 : 10(데이터 확인)
        });

        this.OcrDocMstData = [];
        this.OcrDocDetailData = undefined;
        this.OcrDocDetailImgFileData = undefined;
        if (pageNo == '0') this.OCRTABLETOTCNT = 0;
        this.OCRTEXTTABLETOTCNT = 0;
        this.searchCondCd = '';
        this.DOC_SN = '';

        this.tblSno = '';
        this.pgSn = '';

        if (pageNo == '0') this.onResetPage1();

        $('#automlBoxplotImage').empty();
        $('#automlDistributionImage').empty();

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
                                '<td><a href="javascript:void(0);" onClick="window.mldataconfirm.onSelectOcrDocDetail(' +
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
                            'mldataconfirm',
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

        $('#automlBoxplotImage').empty();
        $('#automlDistributionImage').empty();

        this.selected(seq);
        this.onSelectOcrDocTextPaging('1', DOC_SN);
    }

    // (우측 화면) : 데이터 컬럼 상세 목록 <조회> 처리
    onSelectOcrDocTextPaging(pageNo: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;

        const serviceUrl = 'recognition/selectMldataConfirmList';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            PAGE_SN: this.PAGE_SN,
            COND_CD: this.searchCondCd,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 5,
        });

        $('#automlBoxplotImage').empty();
        $('#automlDistributionImage').empty();

        if (pageNo == '0') this.OCRTEXTTABLETOTCNT = 0;

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                console.log(resultData);
                if (resultData.code === 200) {
                    this.OcrDocTextData = resultData.data;
                }
                tmp =
                    '        <colgroup>                                                        ' +
                    '            <col style="width: auto%;">                                   ' +
                    '            <col style="width: auto%;">                                   ' +
                    '            <col style="width: auto%;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width: 100px;">                                   ' +
                    '            <col style="width:  70px;">                                   ' +
                    '        </colgroup>                                                      ' +
                    '        <thead>                                                          ' +
                    '	     <tr>                                                              ' +
                    '            <th>컬럼 명</th>                                                ' +
                    '            <th>컬럼 유형</th>                                              ' +
                    '            <th>사용여부</th>                                               ' +
                    '            <th>최소값</th>                                                ' +
                    '            <th>최대값</th>                                                ' +
                    '            <th>평균</th>                                                 ' +
                    '            <th>표준편차</th>                                              ' +
                    '            <th>분산</th>                                                 ' +
                    '            <th>25%</th>                                                 ' +
                    '            <th>50%</th>                                                 ' +
                    '            <th>75%</th>                                                 ' +
                    '            <th>누락값 수</th>                                              ' +
                    '            <th>선택</th>                                                  ' +
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
                                item.TEXT_NM +
                                '</td>';
                            tmp +=
                                '                    <td class="center">                      ' +
                                item.TEXT_TYPE_GUBUN_NM +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="center">                      ' +
                                item.USE_YN +
                                '                    </td>                                    ';

                            tmp +=
                                '                    <td class="right">                      ' +
                                item.MININUM_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.MAXINUM_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.MEAN_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.STANDARD_DEVIATION +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.VARIANCE_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.PERCENTAGE_25_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.PERCENTAGE_50_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.PERCENTAGE_75_VALUE +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right">                      ' +
                                item.MISSING_VALUE_CNT +
                                '                    </td>                                    ';
                            tmp +=
                                '<td><a href="javascript:void(0);" onClick="window.mldataconfirm.onSelectBoxplot(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                i +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.DOC_SN +
                                // tslint:disable-next-line: prettier
                                 '\',\'' +
                                item.COLUMN_SN +
                                // tslint:disable-next-line: prettier
                                '\');" class="btn btn-primary btn-xs btn-outline btn-fit">선택</a></td>';
                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#ocrDocText').html(tmp);
                        });

                        this.OCRTEXTTABLETOTCNT = resultData.dataCount;
                        this.page2.setInitPageLoad(
                            'page',
                            resultData.dataCount,
                            pageNo,
                            'mldataconfirm',
                            { target: 'page2' },
                            5 // this.PAGESIZE
                        );
                    } else {
                        $('#ocrDocText').html(
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

    // (우측 화면 - 하단) : 데이터 분포 (Boxplot) 처리
    onSelectBoxplot(seq: any, DOC_SN: any, COLUMN_SN: any) {
        this.DOC_SN = DOC_SN;
        this.COLUMN_SN = COLUMN_SN;

        this.onSelectBoxplotPaging('1', COLUMN_SN);

        // this.onSelectDistributionPaging('1', COLUMN_SN); // 정규분포 (Normal Distribution) 처리
    }

    // (우측 화면 - 하단) : 데이터 분포 (Boxplot) 처리
    onSelectBoxplotPaging(pageNo: any, COLUMN_SN: any) {
        this.COLUMN_SN = COLUMN_SN;

        const serviceUrl = 'recognition/selectMldataConfirmTextImage';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            TEXT_SN: this.COLUMN_SN,
            IMAGE_GUBUN: '02',
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 5,
        });

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                if (resultData.code === 200) {
                    this.AutomlBoxplotImageData = resultData.data;
                }

                if (resultData.code === 200) {
                    if (resultData.data.length > 0) {
                        let i = 0;

                        $.each(resultData.data, (index: any, item: any) => {
                            tmp += '<tr>  ';

                            tmp +=
                                '                    <td class="nopadding"> <a data-title="' +
                                item.FILE_NM +
                                '" href="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" data-lightbox="automlBoxplotImage"><img style="max-height:270px;" src="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" class="mCS_img_loaded" /></a></td>                                    ';

                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#automlBoxplotImage').html(tmp);
                        });
                    } else {
                        $('#automlBoxplotImage').html(
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

    // (우측 화면 - 하단) : 정규분포 (Normal Distribution) 처리
    onSelectDistributionPaging(pageNo: any, COLUMN_SN: any) {
        this.COLUMN_SN = COLUMN_SN;

        const serviceUrl = 'recognition/selectMldataConfirmTextImage';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            TEXT_SN: this.COLUMN_SN,
            IMAGE_GUBUN: '03',
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 5,
        });

        this.apigatewayService.doGetPromise(serviceUrl, this.params).then(
            (resultData: any) => {
                let tmp;
                if (resultData.code === 200) {
                    this.AutomlDistributionImageData = resultData.data;
                }

                if (resultData.code === 200) {
                    if (resultData.data.length > 0) {
                        let i = 0;

                        $.each(resultData.data, (index: any, item: any) => {
                            tmp += '<tr>  ';

                            tmp +=
                                '                    <td class="nopadding"> <a data-title="' +
                                item.FILE_NM +
                                '" href="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" data-lightbox="automlBoxplotImage"><img style="max-height:270px;" src="' +
                                this.apigatewayService.apiUrl +
                                '/textimagefile/' +
                                item.FILE_FULL_PATH_R.replace(
                                    'C:\\dev_project\\auto_ml\\textimagefile\\',
                                    ''
                                ) +
                                '" class="mCS_img_loaded" /></a></td>                                    ';

                            tmp +=
                                '</tr>                                                                ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#automlDistributionImage').html(tmp);
                        });
                    } else {
                        $('#automlDistributionImage').html(
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

        $('#ocrDocText').empty();
        $('#automlBoxplotImage').empty();
        $('#automlDistributionImage').empty();

        this.OCRTABLETOTCNT = 0;
        if (this.page1) {
            this.page1.setInitPageLoad(
                'page',
                0,
                1,
                'mldataconfirm',
                { target: 'page1' },
                10 // this.PAGESIZE
            );
        }
    }

    // 데이터 상세 목록 <조회> - 페이징 처리
    onResetPage2() {
        $('#ocrDocText').empty();
        $('#automlBoxplotImage').empty();
        $('#automlDistributionImage').empty();

        this.OCRTEXTTABLETOTCNT = 0;
        if (this.page2) {
            this.ocrDocTextPageNo = 1;
            this.page2.setInitPageLoad(
                'page',
                0,
                1,
                'mldataconfirm',
                { target: 'page2' },
                5 // this.PAGESIZE
            );
        }
    }

    // (우측 화면) - 데이터 확인 > 데이터 마스터 목록 <수정> 처리
    onDataConfirmProcess() {
        this.STAT_CD = '10'; // 처리상태 : 10(데이터 확인)

        const data = {
            DOC_SN: this.DOC_SN,
            STAT_CD: this.STAT_CD,
        };

        swal.fire({
            title: '[데이터 확인] 처리 하시겠습니까?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            if (result.value) {
                this.apigatewayService
                    .doPost('recognition/dataConfirmProcess', data, null)
                    .subscribe(
                        resultData => {
                            if (resultData.code === 200) {
                                swal.fire(
                                    '[데이터 확인]이 정상적으로 처리 되었습니다.',
                                    '',
                                    'success'
                                ).then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                });
                            } else {
                                swal.fire(resultData.msg, '', 'info').then(result => {
                                    this.onSearchOcrDocMstList(this.mstPageNo);
                                });
                            }
                        },
                        error => {
                            this.logger.debug(JSON.stringify(error, null, 4));
                            swal.fire('[데이터 확인] 처리실패', '', 'error');
                        }
                    );
            } // confirm yes
        });
    }

    selected(seq: any) {
        this.selectseq = seq;
        $('#ocrDocMst>tbody tr').each(function (index, item) {
            $(item).removeClass('selectcell');
        });
        $('#ocrDocMst>tbody').find('tr').eq(seq).addClass('selectcell');
    }
}
