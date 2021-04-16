import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RotationOptionsComponent } from './rotation-options.component';

describe('RotationOptionsComponent', () => {
  let component: RotationOptionsComponent;
  let fixture: ComponentFixture<RotationOptionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RotationOptionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RotationOptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
