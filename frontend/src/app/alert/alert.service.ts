import {Injectable} from '@angular/core';
import {Alert} from "./Alert";
import {Observable} from "rxjs/Observable";
import {Subject} from "rxjs/Subject";
import {NavigationStart, Router} from "@angular/router";

@Injectable()
export class AlertService {

  private subject = new Subject<Alert>();
  private keepAfterRouteChange = false;

  constructor(private router: Router) {
    // clear alert messages on route change unless 'keepAfterRouteChange' flag is true
    router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        if (this.keepAfterRouteChange) {
          // only keep for a single route change
          this.keepAfterRouteChange = false;
        } else {
          // clear alert messages
          this.clear();
        }
      }
    });
  }

  success(message: string) {
    this.alert(message, 'alert-success');
  }

  info(message: string) {
    this.alert(message, 'alert-info');
  }

  warn(message: string) {
    this.alert(message, 'alert-warning');
  }

  error(message: string) {
    this.alert(message, 'alert-danger');
  }

  private alert(message: string, type: string, keepAfterRouteChange = false) {
    if (!this.keepAfterRouteChange) {
      this.clear();
    }
    this.keepAfterRouteChange = keepAfterRouteChange;
    this.subject.next(<Alert>{message: message, cssClass: type});
  }

  clear() {
    // clear alerts
    this.subject.next();
  }

  getAlerts(): Observable<Alert> {
    return this.subject.asObservable();
  }

}
