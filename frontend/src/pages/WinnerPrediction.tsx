import React, { useState } from 'react';
import { MatchPrediction } from '../components/MatchPrediction';
import { mockTeams } from '../data/Data';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export const WinnerPrediction: React.FC = () => {
  const [gameweek, setGameweek] = useState(1);

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-[#38003c]">Winner Prediction</h1>
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => setGameweek(gw => Math.max(1, gw - 1))}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            disabled={gameweek === 1}
          >
            <ChevronLeft size={24} className={gameweek === 1 ? 'text-gray-400' : 'text-[#38003c]'} />
          </button>
          <span className="font-semibold text-lg">Gameweek {gameweek}</span>
          <button 
            onClick={() => setGameweek(gw => Math.min(38, gw + 1))}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            disabled={gameweek === 38}
          >
            <ChevronRight size={24} className={gameweek === 38 ? 'text-gray-400' : 'text-[#38003c]'} />
          </button>
        </div>
      </div>
      <MatchPrediction 
        homeTeam={mockTeams[0]} 
        awayTeam={mockTeams[1]} 
      />
    </div>
  );
};