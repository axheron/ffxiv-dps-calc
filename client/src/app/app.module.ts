import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { NtkmeButtonModule } from '@ctrl/ngx-github-buttons';
import { NzAvatarModule } from 'ng-zorro-antd/avatar';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzIconModule } from "ng-zorro-antd/icon";
import { NzInputModule } from "ng-zorro-antd/input";
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { NzModalModule } from 'ng-zorro-antd/modal';
import { NzPopconfirmModule } from 'ng-zorro-antd/popconfirm';
import { NzTableModule } from 'ng-zorro-antd/table';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PartySelectComponent } from './party-select/party-select.component';
import { GearsetListComponent } from './gearset-list/gearset-list.component';

registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent,
    PartySelectComponent,
    GearsetListComponent
  ],
  imports: [
    AppRoutingModule,
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    HttpClientModule,
    NtkmeButtonModule,
    NzAvatarModule,
    NzButtonModule,
    NzIconModule,
    NzInputModule,
    NzLayoutModule,
    NzModalModule,
    NzPopconfirmModule,
    NzTableModule,
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
  bootstrap: [AppComponent]
})
export class AppModule { }
