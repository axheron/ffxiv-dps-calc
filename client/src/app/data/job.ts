export interface Job {
  name: string;
  path: string;
  buffs: string[];
}

export const jobs = new Map<string, Job>([
	['AST', {
		name: 'AST',
		path: './assets/astrologian.png',
		buffs: ['DIVINATION'],
	}],
	['BRD', {
		name: 'BRD',
		path: './assets/bard.png',
		buffs: ['BATTLE_VOICE'],
    }],
    ['BLM', {
	    name: 'BLM',
	    path: './assets/blackmage.png',
	    buffs: [],
	}],
	['DNC', {
	    name: 'DNC',
	    path: './assets/dancer.png',
	    buffs: ['TECHNICAL_FINISH'],
  	}],
  	['DRK', {
	    name: 'DRK',
	    path: './assets/darkknight.png',
	    buffs: [],
	}],
    ['DRG', {
    	name: 'DRG',
   	    path: './assets/dragoon.png',
   	    buffs: ['BATTLE_LITANY'],
    }],
    ['GNB', {
	    name: 'GNB',
	    path: './assets/gunbreaker.png',
	    buffs: [],
    }],
    ['MCH', {
	    name: 'MCH',
	    path: './assets/machinist.png',
	    buffs: [],
    }],
    ['MNK', {
	    name: 'MNK',
	    path: './assets/monk.png',
	    buffs: ['BROTHERHOOD'],
    }],
    ['NIN', {
	    name: 'NIN',
	    path: './assets/ninja.png',
	    buffs: ['TRICK_ATTACK'],
    }],
    ['PLD', {
	    name: 'PLD',
	    path: './assets/paladin.png',
	    buffs: [],
    }],
    ['RDM', {
	    name: 'RDM',
	    path: './assets/redmage.png',
	    buffs: ['EMBOLDEN'],
    }],
    ['SAM', {
	    name: 'SAM',
	    path: './assets/samurai.png',
	    buffs: [],
    }],
    ['SCH', {
	    name: 'SCH',
	    path: './assets/scholar.png',
	    buffs: ['CHAIN_STRATAGEM'],
    }],
    ['SMN', {
	    name: 'SMN',
	    path: './assets/summoner.png',
	    buffs: ['DEVOTION'],
    }],
    ['WAR', {
	    name: 'WAR',
	    path: './assets/warrior.png',
	    buffs: [],
    }],
    ['WHM', {
	    name: 'WHM',
	    path: './assets/whitemage.png',
	    buffs: [],
    }],
]);
