import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GearSet, UpdateStatsResponse } from '../data/gearset';

@Injectable({
  providedIn: 'root'
})
export class DpsService {
  selfJob = 'SCH';
  party = ['PLD', 'GNB', 'AST', 'MCH', 'DRG', 'MNK', 'BLM'];
  dataSet = [
    {
      id: '1',
      etroId: '198b6d3f-899e-4103-ae06-329c116ecd67',
      name: '5.5 Relicless Lo Pi 2.33',
      weaponDamage: 180,
      mainStat: 5592,
      dh: 1280,
      crit: 3747,
      det: 2196,
      speed: 2039,
      ten: 380,
      pie: 682,
      gcd: 2.33,
      mp: 0,
      dps: 0,
    }, {
      id: '2',
      etroId: 'fd9ea1b9-8390-4ccc-9d36-36476fd6bfc8',
      name: '5.5 Relicless Lo Pi 2.32',
      weaponDamage: 180,
      mainStat: 5592,
      dh: 1160,
      crit: 3747,
      det: 2196,
      speed: 2159,
      ten: 380,
      pie: 682,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '3',
      etroId: '1652ae0d-deea-4d86-9b4e-f5959f5232d4',
      name: '5.4 2.32 Mid Piety',
      weaponDamage: 180,
      mainStat: 5608,
      dh: 920,
      crit: 3681,
      det: 2152,
      speed: 2133,
      ten: 380,
      pie: 1066,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '4',
      etroId: '4f21e0e3-d02e-4c58-a11d-a5cb062efcf8',
      name: '5.4 2.39 High Piety',
      weaponDamage: 180,
      mainStat: 5608,
      dh: 1220,
      crit: 3786,
      det: 2303,
      speed: 1434,
      ten: 380,
      pie: 1209,
      gcd: 2.39,
      mp: 0,
      dps: 0,
    }, {
      id: '5',
      etroId: '278615be-aac7-490b-9900-e4beee960778',
      name: '5.5 2.32 BiS (AT YOUR OWN RISK)',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 1400,
      crit: 3786,
      det: 2422,
      speed: 2141,
      ten: 380,
      pie: 340,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '6',
      etroId: '4bc70744-55bb-4862-ab95-1e7d3289462a',
      name: '5.5 Raid Earring Set (AT YOUR OWN RISK)',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 1400,
      crit: 3715,
      det: 2375,
      speed: 2259,
      ten: 380,
      pie: 340,
      gcd: 2.31,
      mp: 0,
      dps: 0,
    }, {
      id: '7',
      etroId: '856447fa-b9ba-4bad-a6f8-3ceeb098749f',
      name: '2.22 BiS (SPEEDKILL ONLY -- YOU HAVE BEEN WARNED)',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 860,
      crit: 3546,
      det: 2196,
      speed: 3147,
      ten: 380,
      pie: 340,
      gcd: 2.22,
      mp: 0,
      dps: 0,
    }];

  constructor(private http: HttpClient) { }

  updateAllStats(): void {
    for (let index : number = 0; index < this.dataSet.length; index++) {
      this.updateStats(index);
    }
  }

  updateStats(index: number): void {
    const statsUrl = 'https://ffxiv-dps-calc-backend.uc.r.appspot.com/update_stats';
    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    });
    const request = JSON.stringify({
        player: this.dataSet[index],
        comp: this.party,
        job: this.selfJob
    });
    this.http.post<UpdateStatsResponse>(statsUrl, request, {headers: headers}).subscribe((res: UpdateStatsResponse) => {
      this.dataSet[index].dps = res.dps;
      this.dataSet[index].gcd = res.gcd;
      this.dataSet[index].mp = res.mp;
    });
  }
}
