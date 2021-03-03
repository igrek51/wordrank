import {Component, OnInit} from '@angular/core';
import {DictionaryStatisticsDTO} from "./DictionaryStatisticsDTO";
import {HttpClient} from "@angular/common/http";
import {UserDataService} from "../user/user-data.service";

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {

  dictStats: DictionaryStatisticsDTO[] = [];

  constructor(private http: HttpClient, private userData: UserDataService) {
  }

  ngOnInit() {
    let userId = this.userData.userId;
    let dictionaryCode = this.userData.dictionaryCode;
    const url = `/api/stats/${userId}/${dictionaryCode}`;
    return this.http.get<DictionaryStatisticsDTO[]>(url).subscribe(
      response => this.dictStats = response,
      err => console.log(err)
    );
  }

}
