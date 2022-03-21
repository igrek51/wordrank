import {Component, OnInit} from '@angular/core';
import {WordRank} from "../wordrank/WordRank";
import {WordRankService} from "../wordrank/word-rank.service";
import {AlertService} from "../alert/alert.service";

@Component({
  selector: 'app-words-list',
  templateUrl: './words-list.component.html',
  styleUrls: ['./words-list.component.css']
})
export class WordsListComponent implements OnInit {

  wordranks: WordRank[] = [];

  constructor(
    private wordRankService: WordRankService,
    private alertService: AlertService,
  ) {}

  ngOnInit() {
    this.wordRankService.getAllWordRanks().subscribe(
      wordranks => this.wordranks = wordranks,
      err => this.alertService.reportResponseError(err)
    );
  }

}
