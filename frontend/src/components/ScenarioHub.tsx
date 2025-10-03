'use client';

import { useState } from 'react';

interface Asteroid {
  id: string;
  name: string;
  diameter: number;
  isHazardous: boolean;
  velocity?: number;
  mass?: number;
  composition?: string;
}

interface ScenarioHubProps {
  onAsteroidSelect: (asteroid: Asteroid) => void;
  selectedAsteroid: Asteroid | null;
}

export default function ScenarioHub({ onAsteroidSelect, selectedAsteroid }: ScenarioHubProps) {
  const [selectedMode, setSelectedMode] = useState<'real-time' | 'historical'>('real-time');
  const [searchTerm, setSearchTerm] = useState('');

  // Mock data for real-time NEOs
  const realTimeAsteroids: Asteroid[] = [
    { id: '1', name: 'Apophis', diameter: 0.37, isHazardous: true, velocity: 17.0, mass: 6.1e10, composition: 'Stony' },
    { id: '2', name: 'Bennu', diameter: 0.49, isHazardous: true, velocity: 15.0, mass: 7.3e10, composition: 'Carbonaceous' },
    { id: '3', name: 'Didymos', diameter: 0.78, isHazardous: false, velocity: 13.4, mass: 5.2e11, composition: 'Stony' },
    { id: '4', name: '2023 DW', diameter: 0.05, isHazardous: true, velocity: 25.0, mass: 4.8e8, composition: 'Metallic' },
    { id: '5', name: 'Ryugu', diameter: 0.87, isHazardous: false, velocity: 12.0, mass: 4.5e11, composition: 'Carbonaceous' },
  ];

  // Mock data for historical impacts
  const historicalAsteroids: Asteroid[] = [
    { id: 'h1', name: 'Tunguska Event', diameter: 0.06, isHazardous: true, velocity: 15.0, mass: 1.0e8, composition: 'Stony' },
    { id: 'h2', name: 'Chelyabinsk', diameter: 0.02, isHazardous: true, velocity: 19.0, mass: 1.3e7, composition: 'Stony' },
    { id: 'h3', name: 'Chicxulub Impact', diameter: 10.0, isHazardous: true, velocity: 20.0, mass: 4.6e15, composition: 'Carbonaceous' },
  ];

  const asteroids = selectedMode === 'real-time' ? realTimeAsteroids : historicalAsteroids;
  
  const filteredAsteroids = asteroids.filter(asteroid =>
    asteroid.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6">
      {/* Section 1: Select Impactor */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Select Impactor</h3>
        
        {/* Mode Selection */}
        <div className="flex bg-gray-700 rounded-lg p-1 mb-4">
          <button
            onClick={() => setSelectedMode('real-time')}
            className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedMode === 'real-time'
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:text-white'
            }`}
          >
            Real-Time NEO
          </button>
          <button
            onClick={() => setSelectedMode('historical')}
            className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedMode === 'historical'
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:text-white'
            }`}
          >
            Historical
          </button>
        </div>

        {/* Search */}
        <div className="relative mb-4">
          <input
            type="text"
            placeholder="Search asteroids..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <svg className="absolute right-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Asteroid List */}
        <div className="space-y-2">
          {filteredAsteroids.map((asteroid) => (
            <div
              key={asteroid.id}
              onClick={() => onAsteroidSelect(asteroid)}
              className={`p-3 rounded-lg border cursor-pointer transition-all ${
                selectedAsteroid?.id === asteroid.id
                  ? 'border-blue-500 bg-blue-900/20'
                  : 'border-gray-600 bg-gray-700 hover:border-gray-500 hover:bg-gray-600'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-white">{asteroid.name}</h4>
                  <p className="text-sm text-gray-400">
                    Diameter: {asteroid.diameter} km
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  {asteroid.isHazardous && (
                    <span className="px-2 py-1 bg-red-600 text-white text-xs rounded-full">
                      Hazardous
                    </span>
                  )}
                  {asteroid.composition && (
                    <span className="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded-full">
                      {asteroid.composition}
                    </span>
                  )}
                </div>
              </div>
              {asteroid.velocity && (
                <p className="text-xs text-gray-500 mt-1">
                  Velocity: {asteroid.velocity} km/s
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Section 2: Impact Location (placeholder for future implementation) */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Impact Location</h3>
        <div className="p-4 bg-gray-700 rounded-lg">
          <p className="text-gray-400 text-sm">
            Click on the 3D Earth to select impact location
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Selected: {selectedAsteroid ? 'Click on Earth to select' : 'No asteroid selected'}
          </p>
        </div>
      </div>

      {/* Section 3: Simulation Parameters (placeholder) */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Parameters</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-sm text-gray-300 mb-1">Impact Angle</label>
            <input
              type="range"
              min="0"
              max="90"
              defaultValue="45"
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0°</span>
              <span>45°</span>
              <span>90°</span>
            </div>
          </div>
          
          <div>
            <label className="block text-sm text-gray-300 mb-1">Target Density</label>
            <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="rock">Rock (2.7 g/cm³)</option>
              <option value="water">Water (1.0 g/cm³)</option>
              <option value="ice">Ice (0.9 g/cm³)</option>
              <option value="sand">Sand (1.6 g/cm³)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
