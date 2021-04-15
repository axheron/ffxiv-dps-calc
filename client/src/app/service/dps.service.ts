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
      etroId: 'b3c0a4b6-e6a1-4ff6-9f2b-c7b82a8a2f02',
      name: '5.4 Preliminary SCH BiS',
      weaponDamage: 180,
      mainStat: 5577,
      dh: 1100,
      crit: 3802,
      det: 2272,
      speed: 2139,
      ten: 380,
      pie: 682,
      gcd: 2.32,
      mp: -1191.90,
      dps: 13535.61,
    }, {
      id: '2',
      etroId: '5bd09e65-4349-4b22-9322-850cae3bc6ef',
      name: '5.4 Super Safe Set',
      weaponDamage: 180,
      mainStat: 5577,
      dh: 1460,
      crit: 4033,
      det: 1995,
      speed: 1223,
      ten: 380,
      pie: 1284,
      gcd: 2.41,
      mp: -291.03,
      dps: 13240.73,
    }, {
      id: '3',
      name: '5.45 BiS Tome Earrings',
      weaponDamage: 180,
      mainStat: 5510,
      dh: 1400,
      crit: 3781,
      det: 2478,
      speed: 2141,
      ten: 380,
      pie: 340,
      gcd: 2.32,
      mp: -1491.90,
      dps: 13621.75,
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
