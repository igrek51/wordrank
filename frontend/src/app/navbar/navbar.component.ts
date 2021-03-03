import {Component, OnInit} from '@angular/core';
import {UserDataService} from "../user/user-data.service";

// declare var $: any;

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  username;
  dictionaryName;

  constructor(private userData: UserDataService) {
  }

  ngOnInit() {
    this.userData.changes.subscribe(() => this.updateUserData());
    this.updateUserData();
    // init tooltips
    // $('[data-toggle="tooltip"]').tooltip();
  }

  updateUserData() {
    if (this.userData.loggedIn()) {
      this.username = this.userData.username;
      this.dictionaryName = this.userData.dictionaryDisplayName;
    } else {
      this.username = null;
      this.dictionaryName = null;
    }
  }

  logOut() {
    this.userData.logOut();
  }
}
