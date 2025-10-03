'use client';

import { useState } from 'react';
import SimulationMode from './SimulationMode';
import DefenseMode from './DefenseMode';

export type AppMode = 'simulation' | 'defense';

export default function MainLayout() {
  const [currentMode, setCurrentMode] = useState<AppMode>('simulation');

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-white">Asterix</h1>
            <span className="text-gray-400">|</span>
            <span className="text-sm text-gray-300">Planetary Defense Simulation</span>
          </div>
          
          {/* Mode Selector */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentMode('simulation')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                currentMode === 'simulation'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Impact Simulation
            </button>
            <button
              onClick={() => setCurrentMode('defense')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                currentMode === 'defense'
                  ? 'bg-amber-600 text-white shadow-lg'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              Defense Mode
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {currentMode === 'simulation' ? (
          <SimulationMode />
        ) : (
          <DefenseMode />
        )}
      </main>
    </div>
  );
}
