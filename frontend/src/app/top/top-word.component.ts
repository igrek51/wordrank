import {Component, OnInit, HostListener} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {WordRank} from "../wordrank/WordRank";
import {UserDataService} from "../user/user-data.service";
import {ActivatedRoute}from "@angular/router";
import {Router}from "@angular/router";

declare var $: any;

const fadeTime = 500;

@Component({
  selector: 'app-top-word',
  templateUrl: './top-word.component.html',
  styleUrls: ['./top-word.component.css']
})
export class TopWordComponent implements OnInit {

  topWord: WordRank;
  displayWordName;
  displayDefinition;
  sortby;

  constructor(private http: HttpClient, private userData: UserDataService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    // force to reload on url change
    this.router.routeReuseStrategy.shouldReuseRoute = function(){
      return false;
    };

    if (!this.isMobileDevice()) { // can't hover on tooltip on mobile devices
      $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })
    }

    this.sortby = this.route.snapshot.paramMap.get("sortby")
    this.nextTopWordInit();
  }

  nextTopWordInit() {
    let userId = this.userData.userId;
    let dictionaryCode = this.userData.dictionaryCode;
    let sortby = this.sortby
    const url = `/api/rank/${sortby}/${userId}/${dictionaryCode}`;
    return this.http.get<WordRank>(url).subscribe(
      response => this.onTopWordReceived(response),
      err => console.log(err)
    );
  }

  onTopWordReceived(topWord) {
    this.topWord = topWord;
    if (this.topWord == null) {
      $("#button-skip").hide();
      $("#button-check").hide();
      $("#button-answer-correct").hide();
      $("#button-answer-wrong").hide();
    } else {
      if (this.topWord.reversedDictionary) {
        this.displayWordName = '';
        this.displayDefinition = this.topWord.definition;
      } else {
        this.displayWordName = this.topWord.wordName;
        this.displayDefinition = '';
      }
      $("#button-check").show();
      $("#button-answer-correct").hide();
      $("#button-answer-wrong").hide();
    }
  }

  checkAnswer() {
    $("#button-check").hide();
    $("#button-answer-correct").fadeIn(fadeTime);
    $("#button-answer-wrong").fadeIn(fadeTime);

    this.displayWordName = this.topWord.wordName;
    this.displayDefinition = this.topWord.definition;

    if (!this.topWord.reversedDictionary) {
      $("#dict-definition")
        .hide()
        .fadeIn(fadeTime);
    } else {
      $("#dict-word")
        .hide()
        .fadeIn(fadeTime);
    }
  }

  answerCorrect() {
    this.clickedWordAction('answer/correct');
  }

  answerWrong() {
    this.clickedWordAction('answer/wrong');
  }

  skipWord() {
    this.clickedWordAction('skip');
  }

  playWord() {
    let audio = new Audio();
    let word = this.topWord.wordName
    let query = encodeURIComponent(word);
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=` + query;
    audio.src = url;
    audio.play();
  }

  clickedWordAction(endpointAction) {
    let rankId = this.topWord.rankId;
    const url = `/api/rank/${rankId}/${endpointAction}`;
    this.http.post<WordRank>(url, null).subscribe(
      () => {
        this.nextTopWordInit();
      },
      err => console.log(err)
    );
  }

  @HostListener('document:keypress', ['$event'])
  handleKeyboardEvent(event: KeyboardEvent) { 
    if (event.keyCode === 32) { // space
      this.checkAnswer();
    } else if (event.key == 'q') {
      this.answerCorrect();
    } else if (event.key == 'w') {
      this.answerWrong();
    } else if (event.key == 'e') {
      this.skipWord();
    } else if (event.key == 'r') {
      this.playWord();
    }
  }

  isMobileDevice(): boolean {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  }

}
