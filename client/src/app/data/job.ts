export interface Job {
  id: string;
  name: string;
  path: string;
  buffs: string[];
}

export const ASTROLOGIAN: Job = {
  id: 'AST',
  name: 'Astrologian',
  path: './assets/astrologian.png',
  buffs: ['DIVINATION'],
};

export const BARD: Job = {
  id: 'BRD',
  name: 'Bard',
  path: './assets/bard.png',
  buffs: ['BATTLE_VOICE'],
};

export const BLACK_MAGE: Job = {
  id: 'BLM',
  name: 'Black mage',
  path: './assets/blackmage.png',
  buffs: [],
};

export const DANCER: Job = {
  id: 'DNC',
  name: 'Dancer',
  path: './assets/dancer.png',
  buffs: ['TECHNICAL_FINISH'],
};

export const DARK_KNIGHT: Job = {
  id: 'DRK',
  name: 'Dark knight',
  path: './assets/darkknight.png',
  buffs: [],
};

export const DRAGOON: Job = {
  id: 'DRG',
  name: 'Dragonn',
  path: './assets/dragoon.png',
  buffs: ['BATTLE_LITANY'],
};

export const GUNBREAKER: Job = {
  id: 'GNB',
  name: 'Gunbreaker',
  path: './assets/gunbreaker.png',
  buffs: [],
};

export const MACHINIST: Job = {
  id: 'MCH',
  name: 'Machinist',
  path: './assets/machinist.png',
  buffs: [],
};

export const MONK: Job = {
  id: 'MNK',
  name: 'Monk',
  path: './assets/monk.png',
  buffs: ['BROTHERHOOD'],
};

export const NINJA: Job = {
  id: 'NIN',
  name: 'Ninja',
  path: './assets/ninja.png',
  buffs: ['TRICK_ATTACK'],
};

export const PALADIN: Job = {
  id: 'PLD',
  name: 'Paladin',
  path: './assets/paladin.png',
  buffs: [],
};

export const RED_MAGE: Job = {
  id: 'RDM',
  name: 'Red mage',
  path: './assets/redmage.png',
  buffs: ['EMBOLDEN'],
};

export const SAMURAI: Job = {
  id: 'SAM',
  name: 'Samurai',
  path: './assets/samurai.png',
  buffs: [],
};

export const SCHOLAR: Job = {
  id: 'SCH',
  name: 'Scholar',
  path: './assets/scholar.png',
  buffs: ['CHAIN_STRATAGEM'],
};

export const SUMMONER: Job = {
  id: 'SMN',
  name: 'Summoner',
  path: './assets/summoner.png',
  buffs: ['DEVOTION'],
};

export const WARRIOR: Job = {
  id: 'WAR',
  name: 'Warrior',
  path: './assets/warrior.png',
  buffs: [],
};

export const WHITE_MAGE: Job = {
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

export const IMPLEMENTED_JOBS = [SCHOLAR];

export interface Role {
  name: string;
  jobs: Job[];
};

export const TANK: Role = {
  name: 'Tank',
  jobs: [DARK_KNIGHT, GUNBREAKER, PALADIN, WARRIOR],
};

export const HEALER: Role = {
  name: 'Healer',
  jobs: [ASTROLOGIAN, SCHOLAR, WHITE_MAGE],
};

export const MELEE: Role = {
  name: 'Melee',
  jobs:  [DRAGOON, MONK, NINJA, SAMURAI],
}

export const RANGED: Role = {
  name: 'Ranged',
  jobs: [BARD, DANCER, MACHINIST],
};

export const CASTER: Role = {
  name: 'Caster',
  jobs: [BLACK_MAGE, RED_MAGE, SUMMONER],
};

export const DPS: Role = {
  name: 'DPS',
  jobs: [...MELEE.jobs, ...RANGED.jobs, ...CASTER.jobs],
}

export const ROLES = [TANK, HEALER, MELEE, RANGED, CASTER];