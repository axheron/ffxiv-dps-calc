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
    this.hideUnimplementedJobs = true;
    this.jobPickerVisible = true;
    this.selectableRoles = jobConsts.ROLES;
    this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
        (jobChosen: string) => {
          if (jobChosen) {
            this.dpsService.selfJob = jobChosen;
            this.dpsService.updateAllStats();
          }
        });
  }

  changeParty(index: number): void {
    this.hideUnimplementedJobs = false;
    this.jobPickerVisible = true;
    this.selectableRoles = this.getAvailableRoles(
        jobConsts.JOBS.get(this.dpsService.selfJob) || jobConsts.SCHOLAR,
        index);
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
      if (index === 0) {
        return [jobConsts.TANK];
      } else if (index === 1 || index === 2) {
        return [jobConsts.HEALER];
      } else {
        return jobConsts.DPS_ROLES;
      }
    } else if (jobConsts.HEALER.jobs.includes(selfJob)) {
      if (index === 0 || index === 1) {
        return [jobConsts.TANK];
      } else if (index === 2) {
        return [jobConsts.HEALER];
      } else {
        return jobConsts.DPS_ROLES;
      }
    } else {
      if (index === 0 || index === 1) {
        return [jobConsts.TANK];
      } else if (index === 2 || index === 3) {
        return [jobConsts.HEALER];
      } else {
        return jobConsts.DPS_ROLES;
      }
    }
  }

  pickJob(job: string): void {
    this.jobPickerModalRef.close(job);
  }

  closeJobPicker(): void {
    this.jobPickerVisible = false;
  }
}
