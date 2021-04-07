import { TestBed } from '@angular/core/testing';

import { DpsService } from './dps.service';

describe('DpsService', () => {
  let service: DpsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DpsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
