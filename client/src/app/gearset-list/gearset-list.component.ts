import { Component, OnInit } from '@angular/core';

interface GearSet {
	name: string;
	weaponDamage: number;
	mainStat: number;
	dh: number;
	crit: number;
	det: number;
	sps: number;
	pie: number;
	gcd: number;
	mp: number;
	dps: number;
}


@Component({
  selector: 'app-gearset-list',
  templateUrl: './gearset-list.component.html',
  styleUrls: ['./gearset-list.component.css']
})
export class GearsetListComponent implements OnInit {
	dataSet = [
	{
		name: '5.4 Preliminary SCH BiS',
		weaponDamage: 180,
		mainStat: 5577,
		dh: 1100,
		crit: 3802,
		det: 2272,
		sps: 2139,
		pie: 682,
		gcd: 2.32,
		mp: -1191.90,
		dps: 13535.61,
	}, {
		name: '5.4 Super Safe Set',
		weaponDamage: 180,
		mainStat: 5577,
		dh: 1460,
		crit: 4033,
		det: 1995,
		sps: 1223,
		pie: 1284,
		gcd: 2.41,
		mp: -291.03,
		dps: 13240.73,
	}, {
		name: '5.45 BiS Tome Earrings',
		weaponDamage: 180,
		mainStat: 5510,
		dh: 1400,
		crit: 3781,
		det: 2478,
		sps: 2141,
		pie: 340,
		gcd: 2.32,
		mp: -1491.90,
		dps: 13621.75,
	}];

  constructor() { }

  ngOnInit(): void {
  }

}
