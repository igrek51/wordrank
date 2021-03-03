import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';

import {AppComponent} from './app.component';
import {PageNotFoundComponent} from './errors/page-not-found.component';
import {AppRoutingModule} from "./routing/app-routing.module";
import {TopWordComponent} from "./top/top-word.component";
import {AddWordComponent} from "./addword/add-word.component";
import {SettingsComponent} from "./settings/settings.component";
import {StatisticsComponent} from "./stats/statistics.component";
import {WordsListComponent} from "./wordslist/words-list.component";
import {FooterComponent} from "./footer/footer.component";
import {NavbarComponent} from "./navbar/navbar.component";
import {AlertsPanelComponent} from "./alert/alerts-panel.component";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {AlertService} from "./alert/alert.service";
import {WordRankService} from "./wordrank/word-rank.service";
import {UserDataService} from "./user/user-data.service";
import {AuthGuardService} from "./routing/auth-guard.service";
import {ApiUrlInterceptorService} from "./routing/api-url-interceptor.service";

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
    TopWordComponent,
    AddWordComponent,
    SettingsComponent,
    StatisticsComponent,
    WordsListComponent,
    FooterComponent,
    NavbarComponent,
AlertsPanelComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    AlertService,
    WordRankService,
    UserDataService,
    AuthGuardService,
    {provide: HTTP_INTERCEPTORS, useClass: ApiUrlInterceptorService, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
