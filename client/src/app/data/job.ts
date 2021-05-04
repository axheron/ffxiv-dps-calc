export interface Job {
  name: string;
  path: string;
  buffs: string[];
}

export const ASTROLOGIAN: Job = {
  name: 'AST',
  path: './assets/astrologian.png',
  buffs: ['DIVINATION'],
};

export const BARD: Job = {
  name: 'BRD',
  path: './assets/bard.png',
  buffs: ['BATTLE_VOICE'],
};

export const BLACK_MAGE: Job = {
  name: 'BLM',
  path: './assets/blackmage.png',
  buffs: [],
};

export const DANCER: Job = {
  name: 'DNC',
  path: './assets/dancer.png',
  buffs: ['TECHNICAL_FINISH'],
};

export const DARK_KNIGHT: Job = {
  name: 'DRK',
  path: './assets/darkknight.png',
  buffs: [],
};

export const DRAGOON: Job = {
  name: 'DRG',
  path: './assets/dragoon.png',
  buffs: ['BATTLE_LITANY'],
};

export const GUNBREAKER: Job = {
  name: 'GNB',
  path: './assets/gunbreaker.png',
  buffs: [],
};

export const MACHINIST: Job = {
  name: 'MCH',
  path: './assets/machinist.png',
  buffs: [],
};

export const MONK: Job = {
  name: 'MNK',
  path: './assets/monk.png',
  buffs: ['BROTHERHOOD'],
};

export const NINJA: Job = {
  name: 'NIN',
  path: './assets/ninja.png',
  buffs: ['TRICK_ATTACK'],
};

export const PALADIN: Job = {
  name: 'PLD',
  path: './assets/paladin.png',
  buffs: [],
};

export const RED_MAGE: Job = {
  name: 'RDM',
  path: './assets/redmage.png',
  buffs: ['EMBOLDEN'],
};

export const SAMURAI: Job = {
  name: 'SAM',
  path: './assets/samurai.png',
  buffs: [],
};

export const SCHOLAR: Job = {
  name: 'SCH',
  path: './assets/scholar.png',
  buffs: ['CHAIN_STRATAGEM'],
};

export const SUMMONER: Job = {
  name: 'SMN',
  path: './assets/summoner.png',
  buffs: ['DEVOTION'],
};

export const WARRIOR: Job = {
  name: 'WAR',
  path: './assets/warrior.png',
  buffs: [],
};

export const WHITE_MAGE: Job = {
  name: 'WHM',
  path: './assets/whitemage.png',
  buffs: [],
};

export const JOBS = new Map<string, Job>([
	['AST', ASTROLOGIAN],
	['BRD', BARD],
  ['BLM', BLACK_MAGE],
	['DNC', DANCER],
  ['DRK', DARK_KNIGHT],
  ['DRG', DRAGOON],
  ['GNB', GUNBREAKER],
  ['MCH', MACHINIST],
  ['MNK', MONK],
  ['NIN', NINJA],
  ['PLD', PALADIN],
  ['RDM', RED_MAGE],
  ['SAM', SAMURAI],
  ['SCH', SCHOLAR],
  ['SMN', SUMMONER],
  ['WAR', WARRIOR],
  ['WHM', WHITE_MAGE],
]);

export const TANK_JOBS = [DARK_KNIGHT, GUNBREAKER, PALADIN, WARRIOR];

export const HEALER_JOBS = [ASTROLOGIAN, SCHOLAR, WHITE_MAGE];

export const MELEE_JOBS = [DRAGOON, MONK, NINJA, SAMURAI];

export const RANGED_JOBS = [BARD, DANCER, MACHINIST];

export const CASTER_JOBS = [BLACK_MAGE, RED_MAGE, SUMMONER];

export const DPS_JOBS = [
  ...MELEE_JOBS,
  ...RANGED_JOBS,
  ...CASTER_JOBS
];
