import { Component, OnInit, ViewChild } from '@angular/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { take } from 'rxjs/operators';

import { DpsService } from '../service/dps.service';
import * as jobConsts from '../data/job';
import { defaultScholarRotation, ScholarRotation } from '../data/rotation';

@Component({
  selector: 'app-rotation-options',
  templateUrl: './rotation-options.component.html',
  styleUrls: ['./rotation-options.component.css']
})
export class RotationOptionsComponent implements OnInit {
  jobConsts = jobConsts;

  @ViewChild('editModal') editModalRef!: NzModalRef;

  modalVisible = false;
  editCache = defaultScholarRotation();

  constructor(public dpsService: DpsService) { }

  ngOnInit(): void {
    this.editCache = { ...this.dpsService.rotation };
  }

  editRotation(): void {
    this.modalVisible = true;
    
  }

  handleConfirm(): void {
    this.dpsService.rotation = { ...this.editCache };
    this.dpsService.updateAllStats();
    this.modalVisible = false;
  }

  handleCancel(): void {
    this.editCache = { ...this.dpsService.rotation };
    this.modalVisible = false;
  }

}
