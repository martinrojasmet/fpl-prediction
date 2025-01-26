import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Dot } from 'recharts';
import { Player } from '../types';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useGameweekContext } from '../context';

interface PlayerRowProps {
  player: Player;
  isExpanded: boolean;
  onToggle: () => void;
}

export const PlayerRow: React.FC<PlayerRowProps> = ({ player, isExpanded, onToggle }) => {

  const gameweek = useGameweekContext()

  const chartData = [...player.previousPoints.map((points, index) => ({
    gameweek: `GW${gameweek + index - 5}`,
    points,
    isPrediction: false,
    key: `gw-${gameweek + index - 5}`
  })), {
    gameweek: 'Predicted',
    points: player.expectedPoints,
    isPrediction: true,
    key: 'prediction'
  }];

  const CustomDot = (props: any) => {
    const { cx, cy, payload } = props;
    return (
      <Dot
        key={payload.key}
        cx={cx}
        cy={cy}
        r={4}
        fill="#fff"
        stroke={payload.isPrediction ? '#e90052' : '#38003c'}
        strokeWidth={2}
      />
    );
  };

  return (
    <>
      <tr 
        className="hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-200"
        onClick={onToggle}
      >
        <td className="p-4">
          <img 
            src={player.imageUrl} 
            alt={player.name} 
            className="w-12 h-15 object-cover transition-transform duration-200 hover:scale-105"
          />
        </td>
        <td className="p-4">{player.name}</td>
        <td className="p-4">{player.opponent}</td>
        <td className="p-4">{player.expectedPoints.toFixed(1)}</td>
        <td className="p-4">
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </td>
      </tr>
      {isExpanded && (
        <tr className="border-b border-gray-200">
          <td colSpan={5} className="p-4">
            <div 
              className="h-64 transform transition-all duration-500 ease-out"
              style={{
                animation: 'expandGraph 0.5s ease-out'
              }}
            >
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <XAxis dataKey="gameweek" />
                  <YAxis />
                  <Tooltip />
                  <defs>
                    <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                      <stop offset="80%" stopColor="#38003c" />
                      <stop offset="80%" stopColor="#e90052" />
                    </linearGradient>
                  </defs>
                  <Line 
                    type="monotone"
                    dataKey="points"
                    stroke="url(#lineGradient)"
                    strokeWidth={2}
                    dot={CustomDot}
                    connectNulls
                    isAnimationActive={true}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </td>
        </tr>
      )}
    </>
  );
};