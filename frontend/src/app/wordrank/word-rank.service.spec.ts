import {inject, TestBed} from '@angular/core/testing';

import {WordRankService} from './word-rank.service';

describe('WordRankService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WordRankService]
    });
  });

  it('should be created', inject([WordRankService], (service: WordRankService) => {
    expect(service).toBeTruthy();
  }));
});
