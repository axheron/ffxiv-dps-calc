import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-party-select',
  templateUrl: './party-select.component.html',
  styleUrls: ['./party-select.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PartySelectComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  changeSelf(): void {
  	console.log("Hello");
  }
}
