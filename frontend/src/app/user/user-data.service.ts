import {EventEmitter, Injectable, OnInit} from '@angular/core';
import {Router} from "@angular/router";

@Injectable()
export class UserDataService implements OnInit {

  userId: string;
  username: string;
  dictionary: string;
  reversedDictionary: boolean;
  changes = new EventEmitter<any>();
  storage = localStorage; // sessionStorage or localStorage

  constructor(private router: Router) {
    // default user logged in initially
    this.userId = '1'
    this.username = 'igrek'
    this.dictionary = 'en-pl'

    if (this.storage.getItem('userId')) {
      this.userId = this.storage.getItem('userId');
      this.username = this.storage.getItem('username');
    }
    if (this.storage.getItem('dictionaryCode')) {
      this.setDictionary(this.storage.getItem('dictionaryCode'));
    }
  }

  ngOnInit() {
  }

  get dictionaryCode(): string {
    return this.dictionary + (this.reversedDictionary ? '-r' : '');
  }

  get dictionaryDisplayName(): string {
    if (this.dictionary) {
      if (this.reversedDictionary) {
        return this.dictionary.replace('-', '<-');
      } else {
        return this.dictionary.replace('-', '->');
      }
    } else {
      return null;
    }
  }

  setUser(userId: string, username: string) {
    this.userId = userId;
    this.username = username;

    this.storage.setItem('userId', '' + this.userId);
    this.storage.setItem('username', this.username);

    this.changes.emit(); // emit settings changed
  }

  setDictionary(dictionaryCode: string) {
    if (dictionaryCode) {
      this.dictionary = dictionaryCode.substr(0, 5);
      this.reversedDictionary = dictionaryCode.endsWith('-r');
      this.storage.setItem('dictionaryCode', dictionaryCode);
    }
    this.changes.emit(); // emit settings changed
  }

  loggedIn(): boolean {
    return this.userId != null && this.dictionary != null;
  }

  logOut() {
    this.userId = null;
    this.username = null;
    this.dictionary = null;
    this.reversedDictionary = null;

    this.storage.clear();
    this.changes.emit(); // emit settings changed

    this.router.navigate([this.router.url]);
  }
}
