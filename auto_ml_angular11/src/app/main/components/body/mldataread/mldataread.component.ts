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
    selector: 'app-mldataread',
    templateUrl: './mldataread.component.html',
    styleUrls: ['./mldataread.component.scss'],
    encapsulation: ViewEncapsulation.None,
})

// 데이터 읽어 들이기
export class MldatareadComponent implements OnInit, OnDestroy {
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

    GLOBAL_DOC_SN: any = '';

    constructor(
        private router: Router,
        private apigatewayService: ApigatewayService,
        private logger: LoggerService,
        private cf: CommFunction,
        private cs: CommService
    ) {
        window.mldataread = this;
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
        console.log('onSearchOcrDocMstList pageNo : ' + pageNo);
        this.type42ImgFileNm1 = '';
        this.type42ImgFileNm2 = '';

        const serviceUrl = 'recognition/selectAutomlMasterList';

        this.params = this.cf.toHttpParams({
            FILE_NM: this.searchtxt,
            STAT_CD: this.searchStatCd,
            BUSINESS_NM: this.searchBusinessNm,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 10,
            FUCTION_GUBUN: '00', // 처리상태 코드 : 00(업로드)
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
                    '            <col style="width:  70px;">                                ' +
                    '        </colgroup>                                                    ' +
                    '        <thead>                                                        ' +
                    '	     <tr>                                                           ' +
                    /* '            <th>순번</th>                                            ' + */
                    '            <th>문서 명</th>                                             ' +
                    '            <th>처리상태</th>                                            ' +
                    '            <th>등록일</th>                                             ' +
                    '            <th>선택</th>                                               ' +
                    '            <th>삭제</th>                                               ' +
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
                                '<td><a href="javascript:void(0);" onClick="window.mldataread.onSelectOcrDocDetail(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                i +
                                // tslint:disable-next-line: prettier
                                '\',\'' +
                                item.DOC_SN +
                                // tslint:disable-next-line: prettier
                                '\');" class="btn btn-primary btn-xs btn-outline btn-fit">선택</a></td>';
                            tmp +=
                                '<td><a href="javascript:void(0);" onClick="window.mldataread.onDeleteAutomlMst(' +
                                // tslint:disable-next-line: prettier
                                '\'' +
                                item.DOC_SN +
                                // tslint:disable-next-line: prettier
                                '\');" class="btn btn-danger btn-xs btn-outline btn-fit">삭제</a></td>';

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
                            'mldataread',
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

    // (좌측 화면) : 데이터 마스터 목록 <삭제> 처리
    onDeleteAutomlMst(DOC_SN: any) {
        const data = {
            DOC_SN,
        };
        swal.fire({
            title: '삭제 하시겠습니까?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: '예',
            cancelButtonText: '아니요',
        }).then(result => {
            if (result.value) {
                this.apigatewayService.doPost('recognition/deleteAutomlMst', data, null).subscribe(
                    resultData => {
                        if (resultData.code === 200) {
                            swal.fire('삭제 되었습니다.', '', 'success').then(result => {
                                this.onSearchOcrDocMstList('1');
                            });
                        } else {
                            swal.fire(resultData.msg, '', 'info').then(result => {
                                this.onSearchOcrDocMstList('1');
                            });
                        }
                    },
                    error => {
                        this.logger.debug(JSON.stringify(error, null, 4));
                        swal.fire('삭제실패', '', 'error');
                    }
                );
            } // confirm yes
        });
    }

    // (우측 화면) : 데이터 상세 목록 <조회> 처리
    onSelectOcrDocDetail(seq: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;
        this.GLOBAL_DOC_SN = DOC_SN;

        const targetRow = this.OcrDocMstData.find(item => item.DOC_SN == this.DOC_SN);

        this.selected(seq);
        this.onSelectOcrDocTextPaging('1', this.DOC_SN);
    }

    // (우측 화면) : 데이터 상세 목록 <조회> 처리
    onSelectOcrDocTextPaging(pageNo: any, DOC_SN: any) {
        this.DOC_SN = DOC_SN;

        const serviceUrl = 'recognition/selectAutomlDatareadColumnInfo';
        this.params = this.cf.toHttpParams({
            DOC_SN: this.DOC_SN,
            PAGE_SN: this.PAGE_SN,
            COND_CD: this.searchCondCd,
            pageNo: pageNo == '0' ? '1' : pageNo,
            PAGESIZE: 16,
        });

        this.OcrDocTextData = undefined;
        if (pageNo == '0') this.OCRTEXTTABLETOTCNT = 0;

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
                                '                    <td class="right" style="width: auto;">' +
                                item.TEXT_NM_001 +
                                '</td>';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_002 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_003 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_004 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_005 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_006 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_007 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_008 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_009 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_010 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_011 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_012 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_013 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_014 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_015 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_016 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_017 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_018 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_019 +
                                '                    </td>                                    ';
                            tmp +=
                                '                    <td class="right" style="width: auto;">  ' +
                                item.TEXT_NM_020 +
                                '                    </td>                                    ';

                            i++;
                        });

                        tmp += '</tbody>';

                        setTimeout(() => {
                            $('#ocrDocText').html(tmp);
                        });

                        this.OCRTEXTTABLETOTCNT = resultData.dataCount;
                        this.page3.setInitPageLoad(
                            'page',
                            resultData.dataCount,
                            pageNo,
                            'mldataread',
                            { target: 'page3' },
                            10 // this.PAGESIZE
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

    // 데이터 마스터 목록 <조회> - 페이징 처리
    onResetPage1() {
        $('#ocrDocMst').empty();
        this.OCRTABLETOTCNT = 0;
        if (this.page1) {
            this.page1.setInitPageLoad(
                'page',
                0,
                1,
                'mldataread',
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
                'mldataread',
                { target: 'page3' },
                16 // this.PAGESIZE
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

    // 억셀 파일 업로드 : [신규] 버튼 -> [등록]
    onFileUpload() {
        // [파일 선택] 여부 체크
        if (!this.uploadFileList1 || this.uploadFileList1.length < 1) {
            swal.fire('파일을 선택하여 주세요.', '', 'warning');
            return;
        }

        // [문서 명] 입력 체크
        if (this.BUSINESS_NM.length < 1 || this.BUSINESS_NM == null || this.BUSINESS_NM == '') {
            swal.fire('문서명을 입력하여 주세요.', '', 'warning');
            return;
        }

        if (this.uploadFileList1 && this.uploadFileList1.length > 0) {
            const serviceUrl = 'recognition/automlDatareadUpload';

            const fileName = 'files';
            const myFiles: File[] = [this.uploadFileList1[0]];
            this.params = this.cf.toHttpParams({ BUSINESS_NM: this.BUSINESS_NM });

            this.apigatewayService
                .doPostuploadFileNamesPromise(serviceUrl, fileName, myFiles, this.params)
                .then(
                    (resultData: any) => {
                        if (resultData.code === 200) {
                            swal.fire('등록 되었습니다.', '', 'success').then(result => {
                                this.onCloseModal();
                                this.ngOnInit();
                            });
                        }
                    },
                    error => {
                        swal.fire(
                            '파일업로드중 에러가 발생하였습니다. 파일을 확인해 주세요.',
                            '',
                            'error'
                        );
                        this.logger.debug(JSON.stringify(error, null, 4));
                    }
                );
        }
    }

    fileSave() {
        swal.fire('저장되었습니다.', '', 'success');
    }

    showFileUploadModal() {
        $('#fileUploadModal').modal('show');
    }

    onCloseModal() {
        this.uploadFileList1 = [];
        this.fileUpload1.nativeElement.value = null;
        this.BUSINESS_NM = '';

        $('#fileUploadModal').modal('hide');
    }

    onFileChange1(files: FileList) {
        this.uploadFileList1 = files;
    }

    onFileChange2(files: FileList) {
        this.uploadFileList2 = files;
    }

    numberOnly(event): boolean {
        const charCode = event.which ? event.which : event.keyCode;
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    }
}
