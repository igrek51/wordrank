import {inject, TestBed} from '@angular/core/testing';

import {AlertsServiceService} from './alert.service';

describe('AlertService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AlertsServiceService]
    });
  });

  it('should be created', inject([AlertsServiceService], (service: AlertsServiceService) => {
    expect(service).toBeTruthy();
  }));
});
