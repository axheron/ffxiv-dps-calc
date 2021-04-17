export interface Buff {
	id: string;
	name: string;
	path: string;
}

export const buffs = new Map<string, Buff>([
	['BATTLE_LITANY', {
		id: 'BATTLE_LITANY',
		name: 'Battle litany',
		path: './assets/battle_litany.png',
	}],
	['BATTLE_VOICE', {
		id: 'BATTLE_VOICE',
		name: 'Battle voice',
		path: './assets/battle_voice.png',
	}],
	['BROTHERHOOD', {
		id: 'BROTHERHOOD',
		name: 'Brotherhood',
		path: './assets/brotherhood.png',
	}],
	['CHAIN_STRATAGEM', {
		id: 'CHAIN_STRATAGEM',
		name: 'Chain stratagem',
		path: './assets/chain_stratagem.png',
	}],
	['DEVOTION', {
		id: 'DEVOTION',
		name: 'Devotion',
		path: './assets/devotion.png',
	}],
	['DIVINATION', {
		id: 'DIVINATION',
		name: 'Divination',
		path: './assets/divination.png',
	}],
	['EMBOLDEN', {
		id: 'EMBOLDEN',
		name: 'Embolden',
		path: './assets/embolden.png',
	}],
	['TECHNICAL_FINISH', {
		id: 'TECHNICAL_FINISH',
		name: 'Technical finish',
		path: './assets/technical_finish.png',
	}],
	['TRICK_ATTACK', {
		id: 'TRICK_ATTACK',
		name: 'Trick attack',
		path: './assets/trick_attack.png',
	}],
]);
