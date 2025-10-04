'use client';

import { useState } from 'react';

interface Threat {
  id: string;
  name: string;
  description: string;
  diameter: number;
  velocity: number;
  impactProbability: number;
  impactDate: string;
  category: 'historical' | 'future';
}

interface MissionBriefingProps {
  onThreatSelect: (threat: Threat) => void;
  selectedThreat: Threat | null;
}

export default function MissionBriefing({ onThreatSelect, selectedThreat }: MissionBriefingProps) {
  const [selectedCategory, setSelectedCategory] = useState<'historical' | 'future'>('future');

  // Mock threat data
  const historicalThreats: Threat[] = [
    {
      id: 'h1',
      name: 'Tunguska Event',
      description: 'Re-imagined as a future threat - similar to the 1908 Tunguska impact',
      diameter: 0.06,
      velocity: 15.0,
      impactProbability: 1.0,
      impactDate: '2024-06-30',
      category: 'historical'
    },
    {
      id: 'h2',
      name: 'Chelyabinsk',
      description: 'Re-imagined as a future threat - similar to the 2013 Chelyabinsk meteor',
      diameter: 0.02,
      velocity: 19.0,
      impactProbability: 1.0,
      impactDate: '2024-02-15',
      category: 'historical'
    }
  ];

  const futureThreats: Threat[] = [
    {
      id: 'f1',
      name: 'Apophis (2029 Flyby)',
      description: 'Potentially hazardous asteroid with close approach in 2029',
      diameter: 0.37,
      velocity: 17.0,
      impactProbability: 0.0001,
      impactDate: '2029-04-13',
      category: 'future'
    },
    {
      id: 'f2',
      name: 'Bennu (Future Risk)',
      description: 'Carbonaceous asteroid with potential impact risk in the 22nd century',
      diameter: 0.49,
      velocity: 15.0,
      impactProbability: 0.0001,
      impactDate: '2135-09-25',
      category: 'future'
    },
    {
      id: 'f3',
      name: '2023 DW',
      description: 'Recently discovered asteroid with high impact probability',
      diameter: 0.05,
      velocity: 25.0,
      impactProbability: 0.001,
      impactDate: '2046-02-14',
      category: 'future'
    }
  ];

  const threats = selectedCategory === 'historical' ? historicalThreats : futureThreats;

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6">
      {/* Section 1: Threat Assessment */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">
          Threat Assessment
        </h3>

        {/* Category Selection */}
        <div className="flex bg-gray-700 rounded-lg p-1 mb-4">
          <button
            onClick={() => setSelectedCategory("historical")}
            className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedCategory === "historical"
                ? "bg-amber-600 text-white"
                : "text-gray-300 hover:text-white"
            }`}
          >
            Historical Threats
          </button>
          <button
            onClick={() => setSelectedCategory("future")}
            className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedCategory === "future"
                ? "bg-amber-600 text-white"
                : "text-gray-300 hover:text-white"
            }`}
          >
            Future PHOs
          </button>
        </div>

        {/* Threat List */}
        <div className="space-y-2">
          {threats.map((threat) => (
            <div
              key={threat.id}
              onClick={() => onThreatSelect(threat)}
              className={`p-3 rounded-lg border cursor-pointer transition-all ${
                selectedThreat?.id === threat.id
                  ? "border-amber-500 bg-amber-900/20"
                  : "border-gray-600 bg-gray-700 hover:border-gray-500 hover:bg-gray-600"
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-white">{threat.name}</h4>
                  <p className="text-sm text-gray-400">{threat.description}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-500">{threat.diameter} km</p>
                  <p className="text-xs text-gray-500">
                    {threat.velocity} km/s
                  </p>
                </div>
              </div>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-500">
                  Impact Date: {threat.impactDate}
                </span>
                <span
                  className={`px-2 py-1 text-xs rounded-full ${
                    threat.impactProbability > 0.01
                      ? "bg-red-600 text-white"
                      : threat.impactProbability > 0.001
                      ? "bg-yellow-600 text-white"
                      : "bg-green-600 text-white"
                  }`}
                >
                  {threat.impactProbability.toFixed(4)}% risk
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Section 2: Impact Corridor Adjustment */}
      {selectedThreat && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">
            Targeting Control
          </h3>
          <div className="p-4 bg-gray-700 rounded-lg">
            <label className="block text-sm text-gray-300 mb-2">
              Adjust Impact Corridor
            </label>
            <input
              type="range"
              min="-180"
              max="180"
              defaultValue="0"
              className="w-full mb-2"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>-180°</span>
              <span>0°</span>
              <span>180°</span>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              Modify the asteroid&apos;s trajectory to target different regions
              on Earth
            </p>
          </div>
        </div>
      )}

      {/* Section 3: Mission Objectives */}
      <div>
        <h3 className="text-lg font-semibold text-white mb-4">
          Mission Objectives
        </h3>
        <div className="space-y-3">
          <div className="p-3 bg-gray-700 rounded-lg">
            <h4 className="text-sm font-medium text-white mb-2">
              Primary Objective
            </h4>
            <p className="text-sm text-gray-300">
              Deflect or destroy the incoming asteroid to prevent Earth impact
            </p>
          </div>

          <div className="p-3 bg-gray-700 rounded-lg">
            <h4 className="text-sm font-medium text-white mb-2">
              Secondary Objectives
            </h4>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Minimize collateral damage</li>
              <li>• Optimize cost efficiency</li>
              <li>• Ensure mission success</li>
            </ul>
          </div>

          <div className="p-3 bg-gray-700 rounded-lg">
            <h4 className="text-sm font-medium text-white mb-2">Constraints</h4>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Budget limit: $1 Trillion</li>
              <li>• Time constraint: Limited window</li>
              <li>• Asset availability: Limited inventory</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Section 4: Current Status */}
      {selectedThreat && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4">
            Current Status
          </h3>
          <div className="p-4 bg-gray-700 rounded-lg space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-300">Threat Selected:</span>
              <span className="text-sm text-white">{selectedThreat.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-300">Time to Impact:</span>
              <span className="text-sm text-white">Calculating...</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-300">
                Deflection Required:
              </span>
              <span className="text-sm text-white">Calculating...</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-300">Mission Status:</span>
              <span className="text-sm text-yellow-400">Planning Phase</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
