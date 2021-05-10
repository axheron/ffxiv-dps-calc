import { ChangeDetectionStrategy, Component, OnInit, ViewChild } from '@angular/core';
import { NzBadgeModule } from 'ng-zorro-antd/badge';
import { NzIconModule } from 'ng-zorro-antd/icon';
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
  hideUnimplementedJobs = false;
  selectableRoles = jobConsts.ROLES;

  constructor(public dpsService: DpsService) { }

  ngOnInit(): void {
  }

  changeSelf(): void {
    this.selectableRoles = jobConsts.ROLES;
    this.hideUnimplementedJobs = true;
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
    const selfJob = jobConsts.JOBS.get(this.dpsService.selfJob);
    if (selfJob === undefined) {
      throw 'Unknown player job';
    }
    this.selectableRoles = this.getAvailableRoles(selfJob, index);
    this.hideUnimplementedJobs = false;
    this.jobPickerVisible = true;
    this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
      (jobChosen: string) => {
        if (jobChosen) {
          this.dpsService.party[index] = jobChosen;
          this.dpsService.updateAllStats();
        }
      });
  }

  private getAvailableRoles(selfJob: jobConsts.Job, index: number):
      jobConsts.Role[] {
    if (jobConsts.TANK.jobs.includes(selfJob)) {
      return jobConsts.PLAYER_TANK_COMP[index];
    } else if (jobConsts.HEALER.jobs.includes(selfJob)) {
      return jobConsts.PLAYER_HEALER_COMP[index];
    } else {
      return jobConsts.PLAYER_DPS_COMP[index];
    }
  }

  pickJob(job: string): void {
    this.jobPickerModalRef.close(job);
  }

  closeJobPicker(): void {
    this.jobPickerVisible = false;
  }
}
