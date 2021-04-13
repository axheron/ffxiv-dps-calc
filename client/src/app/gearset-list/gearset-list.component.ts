import { Component, OnInit } from '@angular/core';
import { take } from 'rxjs/operators';

import { GearSet } from '../data/gearset';
import { DpsService } from '../service/dps.service';

@Component({
  selector: 'app-gearset-list',
  templateUrl: './gearset-list.component.html',
  styleUrls: ['./gearset-list.component.css']
})
export class GearsetListComponent implements OnInit {

	editCache: { [key: string]: { edit: boolean; data: GearSet } } = {};

  constructor(public dpsService: DpsService) { }

  ngOnInit(): void {
    this.dpsService.updateAllStats();
  	this.updateEditCache();
  }

  startEdit(id: string): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: string): void {
    const index = this.dpsService.dataSet.findIndex(item => item.id === id);
    this.editCache[id] = {
      data: { ...this.dpsService.dataSet[index] },
      edit: false
    };
  }

  saveEdit(id: string): void {
    const index = this.dpsService.dataSet.findIndex(item => item.id === id);
    Object.assign(this.dpsService.dataSet[index], this.editCache[id].data);
    this.editCache[id].edit = false;
    this.dpsService.updateStats(index);
  }

  updateEditCache(): void {
    this.dpsService.dataSet.forEach(item => {
      this.editCache[item.id] = {
        edit: false,
        data: { ...item }
      };
    });
  }

}
