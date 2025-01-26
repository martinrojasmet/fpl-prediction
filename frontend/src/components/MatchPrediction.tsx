import React, { useState } from 'react';
import { Team } from '../types';

interface MatchPredictionProps {
  homeTeam: Team;
  awayTeam: Team;
}

export const MatchPrediction: React.FC<MatchPredictionProps> = ({ homeTeam, awayTeam }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div className="w-[70%] mx-auto p-6 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <div className="text-center">
          <img src={homeTeam.logoUrl} alt={homeTeam.name} className="w-16 h-16 mx-auto" />
          <h3 className="mt-2 font-semibold">{homeTeam.name}</h3>
        </div>
        <div className="text-xl font-bold">vs</div>
        <div className="text-center">
          <img src={awayTeam.logoUrl} alt={awayTeam.name} className="w-16 h-16 mx-auto" />
          <h3 className="mt-2 font-semibold">{awayTeam.name}</h3>
        </div>
      </div>

      <div className="relative">
        <div 
          className="relative h-2 bg-gray-200 rounded-full overflow-hidden cursor-pointer transition-all duration-300"
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          style={{ height: isHovered ? '2rem' : '0.5rem' }}
        >
          <div
            className="absolute left-0 h-full transition-all duration-300 flex items-center justify-start pl-2"
            style={{
              width: `${homeTeam.winProbability * 100}%`,
              backgroundColor: homeTeam.primaryColor
            }}
          >
            {isHovered && (
              <span className="text-white font-semibold text-sm whitespace-nowrap">
                {(homeTeam.winProbability * 100).toFixed(1)}%
              </span>
            )}
          </div>
          <div
            className="absolute right-0 h-full transition-all duration-300 flex items-center justify-end pr-2"
            style={{
              width: `${awayTeam.winProbability * 100}%`,
              backgroundColor: awayTeam.primaryColor
            }}
          >
            {isHovered && (
              <span className="text-white font-semibold text-sm whitespace-nowrap">
                {(awayTeam.winProbability * 100).toFixed(1)}%
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};