export interface GearSet {
	id: string;
	name: string;
	weaponDamage: number;
	mainStat: number;
	dh: number;
	crit: number;
	det: number;
	speed: number;
	ten: number;
	pie: number;
	gcd: number;
	mp: number;
	dps: number;
}

export interface GearSetResponse {
	dps: number;
}
