import { Component, OnInit } from '@angular/core';
import { take } from 'rxjs/operators';

import { GearSet, GearSetResponse } from '../data/gearset';
import { DpsService } from '../service/dps.service';

import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from "@angular/common/http";

@Component({
  selector: 'app-gearset-list',
  templateUrl: './gearset-list.component.html',
  styleUrls: ['./gearset-list.component.css']
})
export class GearsetListComponent implements OnInit {
	dataSet = [
	{
		id: '1',
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
	editCache: { [key: string]: { edit: boolean; data: GearSet } } = {};

  constructor(private dpsService: DpsService, private httpClient: HttpClient) { }

  ngOnInit(): void {
    this.getAllDamage();
  	this.updateEditCache();
  }

  startEdit(id: string): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: string): void {
    const index = this.dataSet.findIndex(item => item.id === id);
    this.editCache[id] = {
      data: { ...this.dataSet[index] },
      edit: false
    };
  }

  saveEdit(id: string): void {
    const index = this.dataSet.findIndex(item => item.id === id);
    Object.assign(this.dataSet[index], this.editCache[id].data);
    this.editCache[id].edit = false;
    this.getDamage(index);
  }

  updateEditCache(): void {
    this.dataSet.forEach(item => {
      this.editCache[item.id] = {
        edit: false,
        data: { ...item }
      };
    });
  }

  private calculateDps(index: number): void {
    this.dpsService.calculateDps(this.dataSet[index]).pipe(take(1)).subscribe((dps: number) => {
      this.dataSet[index].dps = dps;
    })

  private getAllDamage(): void {
  	for (let index : number = 0; index < this.dataSet.length; index++) {
  	  this.getDamage(index);
  	}
  }

  private getDamage(index: number): void {
  	const damageUrl = 'https://ffxiv-dps-calc-backend.uc.r.appspot.com/calc_damage';
  	const headers = new HttpHeaders({
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
            })
  	const player = this.dataSet[index];
  	/* TODO: stop hardcoding comp */
  	const comp = ['SCH', 'PLD', 'GNB', 'AST', 'MCH', 'DRG', 'MNK', 'BLM'];
  	const response = this.httpClient.post<GearSetResponse>(damageUrl, JSON.stringify({player: player, comp: comp, job: 'SCH'}), {headers: headers}).subscribe(res => this.dataSet[index].dps = res.dps);
  }

}
