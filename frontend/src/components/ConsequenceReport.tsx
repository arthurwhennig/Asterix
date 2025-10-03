'use client';

import { useState } from 'react';

interface ImpactData {
  impactEnergy: {
    joules: number;
    megatonsTnt: number;
    kilotonsTnt: number;
  };
  crater: {
    diameterKm: number;
    depthKm: number;
  };
  airblast: {
    blastRadiiKm: Record<string, number>;
    fireballRadiusKm: number;
  };
  earthquake: {
    momentMagnitude: number;
    richterMagnitude: number;
    shakingIntensities: Record<string, number>;
  };
  thermal: {
    thermalRadiusKm: number;
    fireballTemperatureC: number;
  };
  tsunami?: {
    initialWaveHeightM: number;
    waveHeights: Record<string, number>;
  };
  damageZones: Record<string, any>;
}

interface Asteroid {
  id: string;
  name: string;
  diameter: number;
  isHazardous: boolean;
  velocity?: number;
  mass?: number;
  composition?: string;
}

interface ConsequenceReportProps {
  impactData: ImpactData | null;
  selectedAsteroid: Asteroid | null;
}

interface TooltipData {
  term: string;
  definition: string;
}

export default function ConsequenceReport({ impactData, selectedAsteroid }: ConsequenceReportProps) {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<TooltipData | null>(null);

  const handleSectionToggle = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const handleTermHover = (term: string, definition: string) => {
    setTooltip({ term, definition });
  };

  const handleTermLeave = () => {
    setTooltip(null);
  };

  // Mock data for demonstration
  const mockImpactData: ImpactData = {
    impactEnergy: {
      joules: 1.5e15,
      megatonsTnt: 0.36,
      kilotonsTnt: 360
    },
    crater: {
      diameterKm: 0.8,
      depthKm: 0.2
    },
    airblast: {
      blastRadiiKm: {
        "1.0_psi": 15.2,
        "2.5_psi": 8.7,
        "5.0_psi": 4.3,
        "15.0_psi": 1.8
      },
      fireballRadiusKm: 0.5
    },
    earthquake: {
      momentMagnitude: 4.2,
      richterMagnitude: 4.0,
      shakingIntensities: {
        "10_km": 8.5,
        "50_km": 6.2,
        "100_km": 4.8,
        "500_km": 2.1,
        "1000_km": 1.0
      }
    },
    thermal: {
      thermalRadiusKm: 2.1,
      fireballTemperatureC: 3200
    },
    tsunami: {
      initialWaveHeightM: 0,
      waveHeights: {}
    },
    damageZones: {
      window_shatter: { radius_km: 15.2, description: "Most windows shatter" },
      residential_damage: { radius_km: 8.7, description: "Most residential buildings severely damaged" },
      building_destruction: { radius_km: 4.3, description: "Most buildings destroyed" }
    }
  };

  const data = impactData || mockImpactData;

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {/* Brief Overview - Always Visible */}
      <div className="bg-gray-700 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-white mb-3">Brief Overview</h3>
        
        <div className="space-y-3">
          <div>
            <h4 className="text-sm font-medium text-gray-300">Impactor Profile</h4>
            <p className="text-white">
              {selectedAsteroid?.name || 'No asteroid selected'} 
              ({selectedAsteroid?.diameter || 0} km diameter)
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-medium text-gray-300">Energy Release</h4>
            <p className="text-white">
              {data.impactEnergy.megatonsTnt.toFixed(2)} megatons TNT
              <span className="text-gray-400 ml-2">
                ({data.impactEnergy.joules.toExponential(2)} J)
              </span>
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-medium text-gray-300">Crater Size</h4>
            <p className="text-white">
              {data.crater.diameterKm.toFixed(1)} km diameter × {data.crater.depthKm.toFixed(1)} km deep
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-medium text-gray-300">Location</h4>
            <p className="text-white">Impact site coordinates</p>
          </div>
        </div>
      </div>

      {/* Expandable Sections */}
      <div className="space-y-2">
        {/* Seismic Analysis */}
        <div className="bg-gray-700 rounded-lg">
          <button
            onClick={() => handleSectionToggle('seismic')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-600 transition-colors"
          >
            <h3 className="text-lg font-semibold text-white">Seismic Analysis</h3>
            <svg 
              className={`w-5 h-5 text-gray-400 transition-transform ${
                expandedSection === 'seismic' ? 'rotate-180' : ''
              }`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          {expandedSection === 'seismic' && (
            <div className="px-4 pb-4 space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Earthquake Magnitude</h4>
                <p className="text-white">
                  <span 
                    className="italic cursor-help"
                    onMouseEnter={() => handleTermHover('Richter Scale', 'A logarithmic scale measuring earthquake magnitude')}
                    onMouseLeave={handleTermLeave}
                  >
                    Richter Scale
                  </span>: {data.earthquake.richterMagnitude.toFixed(1)}
                </p>
                <p className="text-gray-400 text-sm">
                  Moment Magnitude: {data.earthquake.momentMagnitude.toFixed(1)}
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Shaking Intensity Zones</h4>
                <div className="space-y-1">
                  {Object.entries(data.earthquake.shakingIntensities).map(([distance, intensity]) => (
                    <div key={distance} className="flex justify-between text-sm">
                      <span className="text-gray-300">{distance.replace('_', ' ')}</span>
                      <span className="text-white">Intensity {intensity.toFixed(1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Social Analysis */}
        <div className="bg-gray-700 rounded-lg">
          <button
            onClick={() => handleSectionToggle('social')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-600 transition-colors"
          >
            <h3 className="text-lg font-semibold text-white">Social Analysis</h3>
            <svg 
              className={`w-5 h-5 text-gray-400 transition-transform ${
                expandedSection === 'social' ? 'rotate-180' : ''
              }`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          {expandedSection === 'social' && (
            <div className="px-4 pb-4 space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Human Casualties</h4>
                <p className="text-white">
                  Estimated fatalities: 0-50
                  <span className="text-gray-400 ml-2">(Low population density)</span>
                </p>
                <p className="text-white">
                  Estimated injuries: 100-500
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Population Displaced</h4>
                <p className="text-white">
                  Estimated evacuees: 1,000-5,000
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Economic Analysis */}
        <div className="bg-gray-700 rounded-lg">
          <button
            onClick={() => handleSectionToggle('economic')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-600 transition-colors"
          >
            <h3 className="text-lg font-semibold text-white">Economic Analysis</h3>
            <svg 
              className={`w-5 h-5 text-gray-400 transition-transform ${
                expandedSection === 'economic' ? 'rotate-180' : ''
              }`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          {expandedSection === 'economic' && (
            <div className="px-4 pb-4 space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Destroyed Property</h4>
                <p className="text-white">
                  Estimated damage: $50M - $200M
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Economic Disruption</h4>
                <p className="text-white">
                  Regional impact: Moderate
                </p>
                <p className="text-gray-400 text-sm">
                  Global impact: Minimal
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Critical Infrastructure</h4>
                <p className="text-white">
                  Power grids: Minor disruption
                </p>
                <p className="text-white">
                  Transportation: Local delays
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Environmental Analysis */}
        <div className="bg-gray-700 rounded-lg">
          <button
            onClick={() => handleSectionToggle('environmental')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-600 transition-colors"
          >
            <h3 className="text-lg font-semibold text-white">Environmental Analysis</h3>
            <svg 
              className={`w-5 h-5 text-gray-400 transition-transform ${
                expandedSection === 'environmental' ? 'rotate-180' : ''
              }`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          {expandedSection === 'environmental' && (
            <div className="px-4 pb-4 space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Atmospheric Effects</h4>
                <p className="text-white">
                  <span 
                    className="italic cursor-help"
                    onMouseEnter={() => handleTermHover('Dust Ejection', 'Material ejected into the atmosphere by the impact')}
                    onMouseLeave={handleTermLeave}
                  >
                    Dust ejection
                  </span>: Minimal
                </p>
                <p className="text-gray-400 text-sm">
                  Cooling effects: Negligible
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Wildfire Radius</h4>
                <p className="text-white">
                  Thermal radiation radius: {data.thermal.thermalRadiusKm.toFixed(1)} km
                </p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Ecosystem Impact</h4>
                <p className="text-white">
                  Local wildlife: Moderate impact
                </p>
                <p className="text-gray-400 text-sm">
                  Forest damage: {data.thermal.thermalRadiusKm.toFixed(1)} km radius
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Tooltip */}
      {tooltip && (
        <div className="fixed left-4 bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg z-50 max-w-xs">
          <h4 className="font-medium text-white mb-1">{tooltip.term}</h4>
          <p className="text-sm text-gray-300">{tooltip.definition}</p>
        </div>
      )}
    </div>
  );
}
