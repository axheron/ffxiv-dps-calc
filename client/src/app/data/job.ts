export interface Job {
  name: string;
  path: string;
}

export const jobs = new Map<string, Job>([
	['AST', {
		name: 'AST',
		path: './assets/astrologian.png',
	}],
	['BRD', {
		name: 'BRD',
		path: './assets/bard.png',
    }],
    ['BLM', {
	    name: 'BLM',
	    path: './assets/blackmage.png',
	}],
	['DNC', {
	    name: 'DNC',
	    path: './assets/dancer.png',
  	}],
  	['DRK', {
	    name: 'DRK',
	    path: './assets/darkknight.png',
	}],
    ['DRG', {
    	name: 'DRG',
   	    path: './assets/dragoon.png',
    }],
    ['GNB', {
	    name: 'GNB',
	    path: './assets/gunbreaker.png',
    }],
    ['MCH', {
	    name: 'MCH',
	    path: './assets/machinist.png',
    }],
    ['MNK', {
	    name: 'MNK',
	    path: './assets/monk.png',
    }],
    ['NIN', {
	    name: 'NIN',
	    path: './assets/ninja.png',
    }],
    ['PLD', {
	    name: 'PLD',
	    path: './assets/paladin.png',
    }],
    ['RDM', {
	    name: 'RDM',
	    path: './assets/redmage.png',
    }],
    ['SAM', {
	    name: 'SAM',
	    path: './assets/samurai.png',
    }],
    ['SCH', {
	    name: 'SCH',
	    path: './assets/scholar.png',
    }],
    ['SMN', {
	    name: 'SMN',
	    path: './assets/summoner.png',
    }],
    ['WAR', {
	    name: 'WAR',
	    path: './assets/warrior.png',
    }],
    ['WHM', {
	    name: 'WHM',
	    path: './assets/whitemage.png',
    }],
]);
