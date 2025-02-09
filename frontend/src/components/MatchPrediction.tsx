import { Game } from '../types';

interface MatchPredictionProps {
  game: Game;
}

export const MatchPrediction: React.FC<MatchPredictionProps> = ({ game }) => {

  return (
  <div className="md:w-[70%] w-[100%] mx-auto p-6 bg-white rounded-lg shadow-md mb-5">
    <div className="flex items-center justify-center gap-4 mb-2 relative">
      <div className="flex-1 text-center break-words">
        <img src={`http://localhost:5000/api/assets/teams/${game.homeName}.png`}  alt={game.homeName} className="w-16 h-16 mx-auto md:w-20 md:h-20 max-w-full object-contain" />
        <h3 className={`mt-2 font-semibold text-sm md:text-base p-1 px-3 rounded-lg inline-block ${game.result === 1 ? 'bg-green-500 text-white' : ''}`}>
          {game.homeName}
        </h3>
      </div>
      <div className="text-center">
        <div className="text-xl font-bold whitespace-nowrap">vs</div>
        {game.result === 0 && (
          <div className="mt-1 text-sm font-semibold bg-gray-300 text-gray-700 p-1 px-3 rounded-lg">
            Tie
          </div>
        )}
      </div>
      <div className="flex-1 text-center break-words">
        <img src={`http://localhost:5000/api/assets/teams/${game.awayName}.png`} alt={game.awayName} className="w-16 h-16 mx-auto md:w-20 md:h-20 max-w-full object-contain" />
        <h3 className={`mt-2 font-semibold text-sm md:text-base p-1 px-3 rounded-lg inline-block ${game.result === 2 ? 'bg-green-500 text-white' : ''}`}>
          {game.awayName}
        </h3>
      </div>
    </div>
  </div>
  );
};