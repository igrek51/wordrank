import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TopWordComponent} from './top-word.component';

describe('TopWordComponent', () => {
  let component: TopWordComponent;
  let fixture: ComponentFixture<TopWordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TopWordComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopWordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
