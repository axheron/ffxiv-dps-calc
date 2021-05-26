import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GearSet, UpdateStatsResponse } from '../data/gearset';
import { defaultScholarRotation, ScholarRotation } from '../data/rotation';

@Injectable({
  providedIn: 'root'
})
export class DpsService {
  selfJob = 'SCH';
  party = ['PLD', 'GNB', 'AST', 'MCH', 'DRG', 'MNK', 'BLM'];
  rotation = defaultScholarRotation();
  dataSet = [
    {
      id: '1',
      etroId: '4f21e0e3-d02e-4c58-a11d-a5cb062efcf8',
      name: 'Non-Relic 2.41 Hi Pi',
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
      id: '2',
      etroId: '1652ae0d-deea-4d86-9b4e-f5959f5232d4',
      name: 'Non-Relic 2.32 Mid Pi',
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
      id: '3',
      etroId: '198b6d3f-899e-4103-ae06-329c116ecd67',
      name: 'Non-Relic 2.33 Lo Pi',
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
      id: '4',
      etroId: '3b894bb4-3dd6-4fcd-adfd-0d4d43c37fea',
      name: 'Relic 2.41 Hi Pi',
      weaponDamage: 180,
      mainStat: 5581,
      dh: 1520,
      crit: 4178,
      det: 2041,
      speed: 1218,
      ten: 380,
      pie: 1141,
      gcd: 2.41,
      mp: 0,
      dps: 0,
    }, {
      id: '5',
      etroId: '653b1158-f440-4036-84d4-7af2a9f7aa32',
      name: 'Relic 2.32 Mid Pi',
      weaponDamage: 180,
      mainStat: 5608,
      dh: 1280,
      crit: 3846,
      det: 1787,
      speed: 2132,
      ten: 380,
      pie: 1066,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '6',
      etroId: 'fd9ea1b9-8390-4ccc-9d36-36476fd6bfc8',
      name: 'Relic 2.32 Lo Pi',
      weaponDamage: 180,
      mainStat: 5592,
      dh: 1220,
      crit: 3846,
      det: 2223,
      speed: 2132,
      ten: 380,
      pie: 682,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '7',
      etroId: '88f8f236-df05-44a5-8251-31f0da3f060b',
      name: 'Relic 2.32 Min Pi (AT YOUR OWN RISK)',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 1520,
      crit: 3682,
      det: 2574,
      speed: 2132,
      ten: 380,
      pie: 340,
      gcd: 2.32,
      mp: 0,
      dps: 0,
    }, {
      id: '8',
      etroId: '5cb4d69e-30f5-41d6-8a88-4b586a04cc3a',
      name: 'Relic 2.31 Min Pi (AT YOUR OWN RISK)',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 1460,
      crit: 3817,
      det: 2397,
      speed: 2234,
      ten: 380,
      pie: 340,
      gcd: 2.31,
      mp: 0,
      dps: 0,
    }, {
      id: '9',
      etroId: '022eef13-5e11-448d-9805-d03c9da56621',
      name: 'Relic 2.22 BiS (DONT USE THIS IF YOURE NOT SPEEDRUNNING (NOT HIGH PING FRIENDLY EITHER))',
      weaponDamage: 180,
      mainStat: 5525,
      dh: 1160,
      crit: 3763,
      det: 1838,
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
    const statsUrl = 'https://dpscalc.xivresources.com/api/update_stats';
    const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    });
    const request = JSON.stringify({
        player: this.dataSet[index],
        comp: this.party,
        job: this.selfJob,
        rotation: this.rotation,
    });
    this.http.post<UpdateStatsResponse>(statsUrl, request, {headers: headers}).subscribe((res: UpdateStatsResponse) => {
      this.dataSet[index].dps = res.dps;
      this.dataSet[index].gcd = res.gcd;
      this.dataSet[index].mp = res.mp;
    });
  }
}
