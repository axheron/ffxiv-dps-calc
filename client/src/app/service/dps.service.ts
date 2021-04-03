import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GearSet } from '../data/gearset';

@Injectable({
  providedIn: 'root'
})
export class DpsService {

  constructor(private http: HttpClient) { }

  calculateDps(gearSet: GearSet): Observable<number> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Accept': 'text/plain',
        'Content-Type': 'text/plain'
      }),
      /* No I don't understand why this needed to be typecast. */
      'responseType': 'text' as 'text'
    };
    return this.http.get('/calc_damage', httpOptions).pipe(
      map((result) => {
        console.log(result);
        const numbers = result.match(/\d+/);
        const dpsValue = numbers ? parseInt(numbers[0]) : 0;
        return dpsValue;
      }));
  }
}
