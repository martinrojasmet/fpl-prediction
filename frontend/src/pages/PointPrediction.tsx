import React, { useState, useEffect } from 'react';
import { PlayerRow } from '../components/PlayerRow';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Player } from '../types';
import { fetchGWs, fetchPlayers } from '../data/Data';
import { gameweekContext } from '../context';

type SortField = 'name' | 'opponent' | 'expectedPoints';
type SortDirection = 'asc' | 'desc';

export const PointPrediction: React.FC = () => {
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [gameweek, setGameweek] = useState<number>(23);
  const [sortField, setSortField] = useState<SortField>('expectedPoints');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');
  const [players, setPlayers] = useState<Player[]>([]);
  const [gameweeks, setGameweeks] = useState<number[]>([]); // Store the list of gameweeks
  const [currentIndex, setCurrentIndex] = useState<number>(0); // Track the current gameweek index

  useEffect(() => {
    const getGWs = async () => {
      try {
        const gameweeks = await fetchGWs();
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
    const getPlayers = async () => {
      try {
        const data = await fetchPlayers(gameweek);
        setPlayers(data);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };

    getPlayers();
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

  const sortPlayers = (players: Player[]): Player[] => {
    return [...players].sort((a, b) => {
      const aValue = a[sortField];
      const bValue = b[sortField];

      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
      }

      return sortDirection === 'asc'
        ? String(aValue).localeCompare(String(bValue))
        : String(bValue).localeCompare(String(aValue));
    });
  };

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const getSortIcon = (field: SortField) => {
    if (sortField !== field) return null;
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-[#38003c]">Points</h1>
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
      <div className="bg-white rounded-lg shadow-[0_0_10px_rgba(0,0,0,0.1)] overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="p-4 text-left">Player</th>
              <th
                className="p-4 text-left cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => handleSort('name')}
              >
                Name {getSortIcon('name')}
              </th>
              <th
                className="p-4 text-left cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => handleSort('opponent')}
              >
                Opponent {getSortIcon('opponent')}
              </th>
              <th
                className="p-4 text-left cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => handleSort('expectedPoints')}
              >
                Expected Points {getSortIcon('expectedPoints')}
              </th>
              <th className="p-4"></th>
            </tr>
          </thead>
          <tbody>
            <gameweekContext.Provider  value={gameweek}>
              {sortPlayers(players).map(player => (
                <PlayerRow
                  key={player.id}
                  player={player}
                  isExpanded={expandedId === player.id}
                  onToggle={() => setExpandedId(expandedId === player.id ? null : player.id)}
                />
              ))}
            </gameweekContext.Provider>
          </tbody>
        </table>
      </div>
    </div>
  );
};