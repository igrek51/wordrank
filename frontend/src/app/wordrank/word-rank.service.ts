import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {WordRank} from "./WordRank";
import {Observable} from "rxjs/Observable";
import 'rxjs/add/observable/of';
import {UserDataService} from "../user/user-data.service";

@Injectable()
export class WordRankService {

  constructor(private http: HttpClient, private userData: UserDataService) {
  }

  getAllWordRanks(): Observable<WordRank[]> {

    let userId = this.userData.userId;
    let dictionaryCode = this.userData.dictionaryCode;
    const url = `/api/rank/all/${userId}/${dictionaryCode}`;

    return this.http.get<WordRank[]>(url);
  }

}
