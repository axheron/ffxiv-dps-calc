import { ChangeDetectionStrategy, Component, OnInit, ViewChild } from '@angular/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { take } from 'rxjs/operators';

import {buffs} from '../data/buff';
import {jobs} from '../data/job';


@Component({
  selector: 'app-party-select',
  templateUrl: './party-select.component.html',
  styleUrls: ['./party-select.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PartySelectComponent implements OnInit {
  buffs = buffs;
  jobs = jobs;

  @ViewChild('jobPickerModal') jobPickerModalRef!: NzModalRef;

  selfJob = 'SCH';
  party = ['PLD', 'GNB', 'AST', 'MCH', 'DRG', 'MNK', 'BLM'];
  jobPickerVisible = false;

  constructor() { }

  ngOnInit(): void {
  }

  changeSelf(): void {
  	console.log("Hello");
    this.jobPickerVisible = true;
    this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
        (jobChosen: string) => {
          if (jobChosen) {
            this.selfJob = jobChosen;
          }
        });
  }

  changeParty(index: number): void {
    this.jobPickerVisible = true;
        this.jobPickerModalRef.afterClose.pipe(take(1)).subscribe(
          (jobChosen: string) => {
            if (jobChosen) {
              this.party[index] = jobChosen;
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
