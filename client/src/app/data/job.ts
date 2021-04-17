export interface Job {
  id: string;
  name: string;
  path: string;
  buffs: string[];
}

const ASTROLOGIAN: Job = {
  id: 'AST',
  name: 'Astrologian',
  path: './assets/astrologian.png',
  buffs: ['DIVINATION'],
};

const BARD: Job = {
  id: 'BRD',
  name: 'Bard',
  path: './assets/bard.png',
  buffs: ['BATTLE_VOICE'],
};

const BLACK_MAGE: Job = {
  id: 'BLM',
  name: 'Black mage',
  path: './assets/blackmage.png',
  buffs: [],
};

const DANCER: Job = {
  id: 'DNC',
  name: 'Dancer',
  path: './assets/dancer.png',
  buffs: ['TECHNICAL_FINISH'],
};

const DARK_KNIGHT: Job = {
  id: 'DRK',
  name: 'Dark knight',
  path: './assets/darkknight.png',
  buffs: [],
};

const DRAGOON: Job = {
  id: 'DRG',
  name: 'Dragonn',
  path: './assets/dragoon.png',
  buffs: ['BATTLE_LITANY'],
};

const GUNBREAKER: Job = {
  id: 'GNB',
  name: 'Gunbreaker',
  path: './assets/gunbreaker.png',
  buffs: [],
};

const MACHINIST: Job = {
  id: 'MCH',
  name: 'Machinist',
  path: './assets/machinist.png',
  buffs: [],
};

const MONK: Job = {
  id: 'MNK',
  name: 'Monk',
  path: './assets/monk.png',
  buffs: ['BROTHERHOOD'],
};

const NINJA: Job = {
  id: 'NIN',
  name: 'Ninja',
  path: './assets/ninja.png',
  buffs: ['TRICK_ATTACK'],
};

const PALADIN: Job = {
  id: 'PLD',
  name: 'Paladin',
  path: './assets/paladin.png',
  buffs: [],
};

const RED_MAGE: Job = {
  id: 'RDM',
  name: 'Red mage',
  path: './assets/redmage.png',
  buffs: ['EMBOLDEN'],
};

const SAMURAI: Job = {
  id: 'SAM',
  name: 'Samurai',
  path: './assets/samurai.png',
  buffs: [],
};

const SCHOLAR: Job = {
  id: 'SCH',
  name: 'Scholar',
  path: './assets/scholar.png',
  buffs: ['CHAIN_STRATAGEM'],
};

const SUMMONER: Job = {
  id: 'SMN',
  name: 'Summoner',
  path: './assets/summoner.png',
  buffs: ['DEVOTION'],
};

const WARRIOR: Job = {
  id: 'WAR',
  name: 'Warrior',
  path: './assets/warrior.png',
  buffs: [],
};

const WHITE_MAGE: Job = {
  id: 'WHM',
  name: 'White mage',
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
