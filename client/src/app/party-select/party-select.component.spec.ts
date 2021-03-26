import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PartySelectComponent } from './party-select.component';

describe('PartySelectComponent', () => {
  let component: PartySelectComponent;
  let fixture: ComponentFixture<PartySelectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PartySelectComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PartySelectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
