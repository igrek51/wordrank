import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PageNotFoundComponent} from '../errors/page-not-found.component';
import {TopWordComponent} from "../top/top-word.component";
import {AddWordComponent} from "../addword/add-word.component";
import {SettingsComponent} from "../settings/settings.component";
import {StatisticsComponent} from "../stats/statistics.component";
import {WordsListComponent} from "../wordslist/words-list.component";
import {AuthGuardService} from "./auth-guard.service";

const routes: Routes = [
{path: '', redirectTo: '/word/top', pathMatch: 'full'
},
{
path: 'word/:sortby',
    component: TopWordComponent,
    canActivate: [AuthGuardService],
    runGuardsAndResolvers: 'always'
  },
  {
    path: 'list',
    component: WordsListComponent,
    canActivate: [AuthGuardService],
    runGuardsAndResolvers: 'always'
  },
  {
    path: 'add',
    component: AddWordComponent,
    canActivate: [AuthGuardService],
    runGuardsAndResolvers: 'always'
  },
  {
    path: 'stats',
    component: StatisticsComponent,
    canActivate: [AuthGuardService],
    runGuardsAndResolvers: 'always'
  },
  {path: 'settings', component: SettingsComponent},
  {path: '**', component: PageNotFoundComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true, onSameUrlNavigation: 'reload'})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
