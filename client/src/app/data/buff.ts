export interface Buff {
	name: string;
	path: string;
}

export const buffs = new Map<string, Buff>([
	['BATTLE_LITANY', {
		name: 'BATTLE_LITANY',
		path: './assets/battle_litany.png',
	}],
	['BATTLE_VOICE', {
		name: 'BATTLE_VOICE',
		path: './assets/battle_voice.png',
	}],
	['BROTHERHOOD', {
		name: 'BROTHERHOOD',
		path: './assets/brotherhood.png',
	}],
	['CHAIN_STRATAGEM', {
		name: 'CHAIN_STRATAGEM',
		path: './assets/chain_stratagem.png',
	}],
	['BROTHERHOOD', {
		name: 'BROTHERHOOD',
		path: './assets/brotherhood.png',
	}],
	['DEVOTION', {
		name: 'DEVOTION',
		path: './assets/devotion.png',
	}],
	['DIVINATION', {
		name: 'DIVINATION',
		path: './assets/divination.png',
	}],
	['EMBOLDEN', {
		name: 'EMBOLDEN',
		path: './assets/embolden.png',
	}],
	['TECHNICAL_FINISH', {
		name: 'TECHNICAL_FINISH',
		path: './assets/technical_finish.png',
	}],
	['TRICK_ATTACK', {
		name: 'TRICK_ATTACK',
		path: './assets/trick_attack.png',
	}],
]);