import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { PointPrediction } from './pages/PointPrediction';
import { WinnerPrediction } from './pages/WinnerPrediction';
import { TrendingUp, Trophy } from 'lucide-react';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-[#38003c] text-white p-4">
          <div className="container mx-auto flex items-center justify-between">
            <h1 className="text-2xl font-bold">FPL Predictions</h1>
            <div className="space-x-6">
              <Link 
                to="/" 
                className="inline-flex items-center space-x-2 hover:text-[#00ff85] transition-colors"
              >
                {/* <TrendingUp size={20} /> */}
                <span>Points</span>
              </Link>
              <Link 
                to="/games" 
                className="inline-flex items-center space-x-2 hover:text-[#00ff85] transition-colors"
              >
                <span>Games</span>
              </Link>
            </div>
          </div>
        </nav>

        <main className="container mx-auto py-8">
          <Routes>
            <Route path="/" element={<PointPrediction />} />
            <Route path="/games" element={<WinnerPrediction />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;