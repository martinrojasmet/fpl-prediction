import { Player, Team } from '../types';

export const mockPlayers: Player[] = [];

export const mockTeams: Team[] = [
  {
    name: "Liverpool",
    logoUrl: "https://resources.premierleague.com/premierleague/badges/t14.svg",
    primaryColor: "#C8102E",
    winProbability: 0.45
  },
  {
    name: "Manchester City",
    logoUrl: "https://resources.premierleague.com/premierleague/badges/t43.svg",
    primaryColor: "#6CABDD",
    winProbability: 0.55
  }
];


export async function fetchPlayers(gw: number): Promise<Player[]> {
    try {
        const response = await fetch(`http://localhost:5000/api/predictions/points/gws/?gw=${gw}`); // Fixed query param
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const contentType = response.headers.get('content-type');
        if (!contentType?.includes('application/json')) {
            throw new TypeError("Received non-JSON response");
        }

        const data = await response.json();
        return data.players;
    } catch (error) {
        console.error('Error fetching players:', error);
        throw error;
    }
}

export async function fetchCombinedData(gw: number): Promise<Player[]> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 10 seconds timeout

    try {
        const response = await fetch(`/api/combined-data?gw=${gw}`, { signal: controller.signal });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
    
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    } finally {
        clearTimeout(timeoutId);
    }
}

export async function fetchGWs(): Promise<number[]> {
    try {
        const response = await fetch('http://localhost:5000/api/predictions/points/gws/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const contentType = response.headers.get('content-type');
        if (!contentType?.includes('application/json')) {
            throw new TypeError("Received non-JSON response");
        }

        const data = await response.json();
        return data.gw_predictions;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

console.log(await fetchPlayers(23))