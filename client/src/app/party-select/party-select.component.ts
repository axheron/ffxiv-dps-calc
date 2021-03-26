import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';

import {jobs} from '../data/job';


@Component({
  selector: 'app-party-select',
  templateUrl: './party-select.component.html',
  styleUrls: ['./party-select.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PartySelectComponent implements OnInit {
  jobs = jobs;

  selfJob = 'SCH';
  party = ['PLD', 'GNB', 'AST', 'MCH', 'DRG', 'MNK', 'BLM'];

  constructor() { }

  ngOnInit(): void {
  }

  changeSelf(): void {
  	console.log("Hello");
  }

  changeParty(index: number): void {
    console.log("Hi");
  }
}
