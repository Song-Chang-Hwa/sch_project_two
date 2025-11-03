import { CommonModule } from '@angular/common'; // ng 모델을 쓰기위함
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms'; // formGroup 를 쓰기위함
import { FormsModule } from '@angular/forms'; // ng 모델을 쓰기위함
import { RouterModule, Routes } from '@angular/router';
import { CKEditorModule } from '@ckeditor/ckeditor5-angular';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AgGridModule } from 'ag-grid-angular';
import { ChartModule } from 'angular2-chartjs';

import { SafeHtmlModule } from '../shared/pipes/pipe-safehtml-loadJsURL';
import { RootComponent } from './components/body/root/root.component';
import { CommonComponent } from './components/common/common.component';
import { PageComponent } from './components/page/page.component';
import { PagerService } from '../shared/services/'
import { MainComponent } from './main.component';

import {  MldatareadComponent } from './components/body/mldataread/mldataread.component';                               /* 데이터 읽어 들이기  */
import {  MldataconfirmComponent } from './components/body/mldataconfirm/mldataconfirm.component';                      /* 데이터 확인  */
import {  MldatapreprocessingComponent } from './components/body/mldatapreprocessing/mldatapreprocessing.component';    /* 데이터 전처리  */
import {  MlmodeltrainingComponent } from './components/body/mlmodeltraining/mlmodeltraining.component';                /* 모델 선택.학습  */
import {  MlmodelevaluationComponent } from './components/body/mlmodelevaluation/mlmodelevaluation.component';          /* 모델 평가  */

const routes: Routes = [
    {
        path: '',
        component: MainComponent,
        children: [
            { path: '', redirectTo: 'root', pathMatch: 'full' },
            
            { path: 'root', component: RootComponent },        
            
            { path: 'mldataread', component: MldatareadComponent},                      
            { path: 'mldataconfirm', component: MldataconfirmComponent},                
            { path: 'mldatapreprocessing', component: MldatapreprocessingComponent},    
            { path: 'mlmodeltraining', component: MlmodeltrainingComponent},            
            { path: 'mlmodelevaluation', component: MlmodelevaluationComponent},        
        ],
    },
];

@NgModule({   imports: [
        ReactiveFormsModule,
        FormsModule,
        CommonModule,
        SafeHtmlModule,
        CKEditorModule,
        RouterModule.forChild(routes),
        ChartModule,
        AgGridModule,
    ],

    /* 추가, 송창화 - 데이터 읽어 들이기, 데이터 확인, 데이터 전처리, 모델 선택.학습, 모델 평가 */     
    declarations: [CommonComponent, RootComponent, MainComponent, PageComponent, MldatareadComponent, MldataconfirmComponent, MldatapreprocessingComponent,MlmodeltrainingComponent, MlmodelevaluationComponent],  
    entryComponents: [],
    providers: [
        PagerService // ,ApigatewayService
    ],
    exports: [RouterModule],
})
export class MainRoutingModule {}
