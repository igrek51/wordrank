import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot} from '@angular/router';
import {UserDataService} from "../user/user-data.service";
import {AlertService} from "../alert/alert.service";

@Injectable()
export class AuthGuardService implements CanActivate {

  constructor(private router: Router, private userDataService: UserDataService, private alertService: AlertService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (!this.userDataService.loggedIn()) {
      // not logged in - redirect to login page with return url
      this.router.navigate(['/settings'], {queryParams: {returnUrl: state.url}}).then(() => {
        this.alertService.warn('Choose an user and dictionary.');
      });
      return false;
    }
    return true;
  }

}
