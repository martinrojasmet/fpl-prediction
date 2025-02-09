export interface Player {
  id: number;
  name: string;
  imageUrl: string;
  opponent: string;
  expectedPoints: number;
  previousPoints: number[];
}

export interface Team {
  name: string;
  logoUrl: string;
  primaryColor: string;
  winProbability: number;
}

export interface Game {
  homeName: string;
  awayName: string;
  result: number;
}