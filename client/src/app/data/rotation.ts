export interface ScholarRotation {
  energyDrain: number;
  adloquium: number;
  succor: number;
  resurection: number;
}

export function defaultScholarRotation(): ScholarRotation {
  return {
    energyDrain: 4,
    adloquium: 0,
    succor: 0,
    resurection: 0,
  }
}
