import {Injectable} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {Observable} from "rxjs/Rx";
import {PlatformLocation} from "@angular/common";

@Injectable()
export class ApiUrlInterceptorService implements HttpInterceptor {

  constructor(private platformLocation: PlatformLocation) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    req = req.clone({url: this.prepareUrl(req.url)});
    return next.handle(req);
  }

  private prepareUrl(url: string): string {
    let baseUrl = this.platformLocation.getBaseHrefFromDOM();
    let newUrl = baseUrl + '/' + url;
    newUrl = newUrl.replace(/\/+/, '/');
    return newUrl;
  }
}

