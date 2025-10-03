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

interface MasterControlsProps {
  onSimulationStart: () => void;
  onSimulationComplete: (data: any) => void;
  selectedAsteroid: Asteroid | null;
}

export default function MasterControls({ 
  onSimulationStart, 
  onSimulationComplete, 
  selectedAsteroid 
}: MasterControlsProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(60); // 60 seconds simulation
  const [isSimulating, setIsSimulating] = useState(false);

  const handlePlayPause = () => {
    if (isSimulating) return;
    
    if (!isPlaying) {
      setIsPlaying(true);
      onSimulationStart();
      // Simulate the simulation running
      const interval = setInterval(() => {
        setCurrentTime(prev => {
          if (prev >= duration) {
            clearInterval(interval);
            setIsPlaying(false);
            setIsSimulating(false);
            // Mock simulation completion
            onSimulationComplete({
              impactEnergy: { joules: 1.5e15, megatonsTnt: 0.36 },
              crater: { diameterKm: 0.8, depthKm: 0.2 },
              airblast: { blastRadiiKm: { "1.0_psi": 15.2 } },
              earthquake: { richterMagnitude: 4.0 },
              thermal: { thermalRadiusKm: 2.1 }
            });
            return duration;
          }
          return prev + 0.1;
        });
      }, 100);
    } else {
      setIsPlaying(false);
    }
  };

  const handleReset = () => {
    setIsPlaying(false);
    setCurrentTime(0);
    setIsSimulating(false);
  };

  const handleTimeChange = (newTime: number) => {
    if (!isSimulating) {
      setCurrentTime(newTime);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const getPrimaryButtonText = () => {
    if (!selectedAsteroid) return 'Select Asteroid';
    if (isSimulating) return 'Simulating...';
    if (isPlaying) return 'Pause Simulation';
    return 'Start Simulation';
  };

  const getPrimaryButtonColor = () => {
    if (!selectedAsteroid) return 'bg-gray-600';
    if (isSimulating) return 'bg-yellow-600';
    if (isPlaying) return 'bg-red-600';
    return 'bg-green-600';
  };

  return (
    <div className="bg-gray-900 bg-opacity-80 border-t border-gray-700 p-4 backdrop-blur-sm">
      <div className="flex items-center justify-between">
        {/* Timeline */}
        <div className="flex-1 mr-6">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-400 w-16">
              {formatTime(currentTime)}
            </span>
            
            <div className="flex-1 relative">
              <input
                type="range"
                min="0"
                max={duration}
                value={currentTime}
                onChange={(e) => handleTimeChange(parseFloat(e.target.value))}
                disabled={isSimulating}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                style={{
                  background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(currentTime / duration) * 100}%, #374151 ${(currentTime / duration) * 100}%, #374151 100%)`
                }}
              />
            </div>
            
            <span className="text-sm text-gray-400 w-16">
              {formatTime(duration)}
            </span>
          </div>
        </div>

        {/* Control Buttons */}
        <div className="flex items-center space-x-3">
          <button
            onClick={handlePlayPause}
            disabled={!selectedAsteroid}
            className={`px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${getPrimaryButtonColor()} hover:opacity-90`}
          >
            {getPrimaryButtonText()}
          </button>
          
          <button
            onClick={handleReset}
            disabled={isSimulating}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Status Bar */}
      <div className="mt-3 flex items-center justify-between text-sm text-gray-400">
        <div className="flex items-center space-x-4">
          <span>
            Status: {isSimulating ? 'Simulating' : isPlaying ? 'Playing' : 'Ready'}
          </span>
          {selectedAsteroid && (
            <span>
              Asteroid: {selectedAsteroid.name}
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-4">
          <span>
            Progress: {Math.round((currentTime / duration) * 100)}%
          </span>
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #1f2937;
        }
        
        .slider::-moz-range-thumb {
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #1f2937;
        }
      `}</style>
    </div>
  );
}
