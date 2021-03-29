export interface Job {
  name: string;
  path: string;
  buffs: string[];
}

const ASTROLOGIAN: Job = {
  name: 'AST',
  path: './assets/astrologian.png',
  buffs: ['DIVINATION'],
};

const BARD: Job = {
  name: 'BRD',
  path: './assets/bard.png',
  buffs: ['BATTLE_VOICE'],
};

const BLACK_MAGE: Job = {
  name: 'BLM',
  path: './assets/blackmage.png',
  buffs: [],
};

const DANCER: Job = {
  name: 'DNC',
  path: './assets/dancer.png',
  buffs: ['TECHNICAL_FINISH'],
};

const DARK_KNIGHT: Job = {
  name: 'DRK',
  path: './assets/darkknight.png',
  buffs: [],
};

const DRAGOON: Job = {
  name: 'DRG',
  path: './assets/dragoon.png',
  buffs: ['BATTLE_LITANY'],
};

const GUNBREAKER: Job = {
  name: 'GNB',
  path: './assets/gunbreaker.png',
  buffs: [],
};

const MACHINIST: Job = {
  name: 'MCH',
  path: './assets/machinist.png',
  buffs: [],
};

const MONK: Job = {
  name: 'MNK',
  path: './assets/monk.png',
  buffs: ['BROTHERHOOD'],
};

const NINJA: Job = {
  name: 'NIN',
  path: './assets/ninja.png',
  buffs: ['TRICK_ATTACK'],
};

const PALADIN: Job = {
  name: 'PLD',
  path: './assets/paladin.png',
  buffs: [],
};

const RED_MAGE: Job = {
  name: 'RDM',
  path: './assets/redmage.png',
  buffs: ['EMBOLDEN'],
};

const SAMURAI: Job = {
  name: 'SAM',
  path: './assets/samurai.png',
  buffs: [],
};

const SCHOLAR: Job = {
  name: 'SCH',
  path: './assets/scholar.png',
  buffs: ['CHAIN_STRATAGEM'],
};

const SUMMONER: Job = {
  name: 'SMN',
  path: './assets/summoner.png',
  buffs: ['DEVOTION'],
};

const WARRIOR: Job = {
  name: 'WAR',
  path: './assets/warrior.png',
  buffs: [],
};

const WHITE_MAGE: Job = {
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
