import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {PayloadResponse} from "../rest/PayloadResponse";
import {AlertService} from "../alert/alert.service";
import {UserDataService} from "../user/user-data.service";

@Component({
  selector: 'app-add-word',
  templateUrl: './add-word.component.html',
  styleUrls: ['./add-word.component.css']
})
export class AddWordComponent implements OnInit {

  wordName: string;
  definition: string;

  constructor(private http: HttpClient, private alertService: AlertService, private userData: UserDataService) {
  }

  ngOnInit() {
  }

  addNewWord() {
    let addWordDTO = {
      'word': this.wordName,
      'definition': this.definition,
      'userId': this.userData.userId,
      'dictionaryCode': this.userData.dictionaryCode,
    };
    const url = '/api/word';

    return this.http.post<PayloadResponse>(url, addWordDTO).subscribe(
      response => this.addNewWordResult(response),
      err => console.log(err)
    );
  }

  addNewWordResult(response: PayloadResponse) {
    if (PayloadResponse.isOk(response)) {
      this.alertService.success(response.message);
    } else {
      // error occurred
      console.log(response.message);
      this.alertService.error(response.message);
    }
    this.wordName = '';
    this.definition = '';
  }

}
