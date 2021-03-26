import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GearsetListComponent } from './gearset-list.component';

describe('GearsetListComponent', () => {
  let component: GearsetListComponent;
  let fixture: ComponentFixture<GearsetListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GearsetListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GearsetListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
