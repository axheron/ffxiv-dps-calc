import { ChangeDetectionStrategy, Component, OnInit, ViewChild } from '@angular/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { take } from 'rxjs/operators';

import {buffs} from '../data/buff';
import * as jobConsts from '../data/job';
import { DpsService } from '../service/dps.service';


@Component({
  selector: 'app-party-select',
  templateUrl: './party-select.component.html',
  styleUrls: ['./party-select.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PartySelectComponent implements OnInit {
  buffs = buffs;
  jobConsts = jobConsts;

  @ViewChild('jobPickerModal') jobPickerModalRef!: NzModalRef;

  jobPickerVisible = false;

  constructor(public dpsService: DpsService) { }

  ngOnInit(): void {
  }

  changeSelf(): void {
  	console.log("Hello");
    this.jobPickerVisible = true;
    this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
        (jobChosen: string) => {
          if (jobChosen) {
            this.dpsService.selfJob = jobChosen;
            this.dpsService.updateAllStats();
          }
        });
  }

  changeParty(index: number): void {
    this.jobPickerVisible = true;
        this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
          (jobChosen: string) => {
            if (jobChosen) {
              this.dpsService.party[index] = jobChosen;
              this.dpsService.updateAllStats();
            }
          });
  }

  pickJob(job: string): void {
    this.jobPickerModalRef.close(job);
  }

  closeJobPicker(): void {
    this.jobPickerVisible = false;
  }
}
