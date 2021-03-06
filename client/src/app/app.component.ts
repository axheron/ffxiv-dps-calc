import { Component } from '@angular/core';
import { NzIconService } from 'ng-zorro-antd/icon';

const schIconLiteral = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="16 24 480 480">
  <path d="M430 227q-4-6-8-10-18-5-25 9-3 7-3.5 16.5t.5 13.5q7 15 7 24 0 17-12.5 29.5T359 322t-29-12.5-12-29.5q0-26 16-44 10-11 
      36-27l18-12-2-1q-19-16-39-22-33-11-91-11t-91 11q-20 7-39 22l-2 1 18 12q26 16 36 27 16 18 16 44 0 11-5.5 20.5t-15 15.5-20.5 
      6-21-6-15.5-15.5T111 281t7-25q1-4 .5-13.5T115 226q-7-14-25-9-4 4-8 10-7 11-12 24-6 16-6 29 0 31 19.5 55.5t50 31.5 58.5-7 41.5-42.5 
      6-58.5-32.5-49q12-5 25-7 8-2 24-2t24 2q13 2 25 7-25 19-32.5 49t6 58.5T320 360t58.5 7 50-31.5T448 280q0-13-6-29-5-13-12-24z"/>
</svg>
`;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'client';
  constructor(private iconService: NzIconService) {
this.iconService.addIconLiteral('app:SCH', schIconLiteral);

  }
}
