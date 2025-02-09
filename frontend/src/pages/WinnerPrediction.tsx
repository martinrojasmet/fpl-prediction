import React, { useState, useEffect } from 'react';
import { MatchPrediction } from '../components/MatchPrediction';
import { fetchGames, mockTeams } from '../data/Data';
import { Game } from '../types';
import { fetchGWs } from '../data/Data';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export const WinnerPrediction: React.FC = () => {
  const [gameweek, setGameweek] = useState<number>(23);
  const [games, setGames] = useState<Game[]>([]);
  const [gameweeks, setGameweeks] = useState<number[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  useEffect(() => {
    const getGWs = async () => {
      try {
        const gameweeks = await fetchGWs("points");
        setGameweeks(gameweeks);

        if (gameweeks.length > 0) {
          // Set the initial gameweek to the last available gameweek
          const lastGameweek = gameweeks[gameweeks.length - 1];
          setGameweek(lastGameweek);
          setCurrentIndex(gameweeks.length - 1);
        }
      } catch (error) {
        console.error('Error fetching gameweeks:', error);
      }
    };

    getGWs();
  }, []);

  useEffect(() => {
    const getGames = async () => {
      try {
        const data = await fetchGames(gameweek);
        setGames(data);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };

    getGames();
  }, [gameweek]);

  const handleGameweekChange = (direction: 'prev' | 'next') => {
    let newIndex = currentIndex;

    if (direction === 'prev' && currentIndex > 0) {
      newIndex = currentIndex - 1;
    } else if (direction === 'next' && currentIndex < gameweeks.length - 1) {
      newIndex = currentIndex + 1;
    }

    if (newIndex !== currentIndex) {
      setCurrentIndex(newIndex);
      setGameweek(gameweeks[newIndex]);
    }
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-[#38003c]">Games</h1>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => handleGameweekChange('prev')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            disabled={currentIndex === 0}
          >
            <ChevronLeft size={24} className={currentIndex === 0 ? 'text-gray-400' : 'text-[#38003c]'} />
          </button>
          <span className="font-semibold text-lg">Gameweek {gameweek}</span>
          <button
            onClick={() => handleGameweekChange('next')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            disabled={currentIndex === gameweeks.length - 1}
          >
            <ChevronRight size={24} className={currentIndex === gameweeks.length - 1 ? 'text-gray-400' : 'text-[#38003c]'} />
          </button>
        </div>
      </div>
      <div>
        {games.map((game) => (
            <MatchPrediction key={`${game.homeName}-${game.awayName}-${gameweek}`} game={game} />
          ))}
      </div>
    </div>
  );
};