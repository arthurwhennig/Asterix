'use client';

import { useState } from 'react';

interface MissionResults {
  success: boolean;
  score: number; // 1-3 stars
  totalCost: number;
  consequencesMitigated: number;
  details: {
    asteroidDeflected: boolean;
    impactPrevented: boolean;
    costEfficiency: number;
  };
}

interface DeployedAsset {
  id: string;
  type: string;
  name: string;
  cost: number;
  position: any;
  deployedAt: string;
}

interface MissionReportProps {
  missionResults: MissionResults | null;
  missionCompleted: boolean;
  isExecuting: boolean;
  deployedAssets: DeployedAsset[];
  selectedThreat: any;
}

export default function MissionReport({ 
  missionResults, 
  missionCompleted, 
  isExecuting, 
  deployedAssets, 
  selectedThreat 
}: MissionReportProps) {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const handleSectionToggle = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const formatCurrency = (amount: number) => {
    if (amount >= 1e12) {
      return `$${(amount / 1e12).toFixed(1)}T`;
    } else if (amount >= 1e9) {
      return `$${(amount / 1e9).toFixed(1)}B`;
    } else if (amount >= 1e6) {
      return `$${(amount / 1e6).toFixed(1)}M`;
    } else {
      return `$${amount.toLocaleString()}`;
    }
  };

  const renderStars = (score: number) => {
    return Array.from({ length: 3 }, (_, i) => (
      <span
        key={i}
        className={`text-2xl ${
          i < score ? 'text-yellow-400' : 'text-gray-600'
        }`}
      >
        ⭐
      </span>
    ));
  };

  const getSuccessMessage = (results: MissionResults) => {
    if (results.success) {
      if (results.score === 3) {
        return "★★★ Perfect Score! Threat neutralized under budget.";
      } else if (results.score === 2) {
        return "★★ Good job! Threat successfully deflected with minor issues.";
      } else {
        return "★ Mission accomplished, but with significant challenges.";
      }
    } else {
      return "❌ Mission failed. The asteroid impact could not be prevented.";
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {/* Mission Status */}
      <div className="bg-gray-700 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-white mb-3">Mission Status</h3>
        
        {isExecuting ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-blue-400 font-medium">Executing Defense Plan...</p>
            <p className="text-gray-400 text-sm mt-2">
              Simulating asteroid deflection sequence
            </p>
          </div>
        ) : missionCompleted && missionResults ? (
          <div className="space-y-4">
            {/* Mission Summary */}
            <div className="text-center">
              <div className="flex justify-center mb-2">
                {renderStars(missionResults.score)}
              </div>
              <h4 className={`text-xl font-bold mb-2 ${
                missionResults.success ? 'text-green-400' : 'text-red-400'
              }`}>
                {missionResults.success ? 'MISSION SUCCESS' : 'MISSION FAILED'}
              </h4>
              <p className="text-gray-300 text-sm">
                {getSuccessMessage(missionResults)}
              </p>
            </div>

            {/* Performance Metrics */}
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-white">
                  {formatCurrency(missionResults.totalCost)}
                </p>
                <p className="text-gray-400 text-sm">Total Cost</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-white">
                  {missionResults.consequencesMitigated.toFixed(1)}%
                </p>
                <p className="text-gray-400 text-sm">Consequences Mitigated</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-400">
              {selectedThreat ? 'Ready to execute defense plan' : 'Select a threat to begin'}
            </p>
          </div>
        )}
      </div>

      {/* Detailed Analysis (only show if mission completed) */}
      {missionCompleted && missionResults && (
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
                    {missionResults.details.asteroidDeflected 
                      ? 'No significant seismic activity' 
                      : 'Magnitude 4.2 - Moderate shaking'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Shaking Intensity</h4>
                  <p className="text-white">
                    {missionResults.details.asteroidDeflected 
                      ? 'No impact-related shaking' 
                      : 'Light to moderate shaking within 100km radius'
                    }
                  </p>
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
                    {missionResults.details.impactPrevented 
                      ? 'Zero casualties - Impact prevented' 
                      : 'Estimated 0-50 fatalities, 100-500 injuries'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Population Displaced</h4>
                  <p className="text-white">
                    {missionResults.details.impactPrevented 
                      ? 'No evacuation required' 
                      : '1,000-5,000 people evacuated'
                    }
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
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Property Damage</h4>
                  <p className="text-white">
                    {missionResults.details.impactPrevented 
                      ? 'No property damage - Impact prevented' 
                      : 'Estimated $50M - $200M in property damage'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Economic Disruption</h4>
                  <p className="text-white">
                    {missionResults.details.impactPrevented 
                      ? 'No economic disruption' 
                      : 'Regional economic impact: Moderate'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Cost Efficiency</h4>
                  <p className="text-white">
                    Defense cost: {formatCurrency(missionResults.totalCost)}
                  </p>
                  <p className="text-gray-400 text-sm">
                    Efficiency rating: {missionResults.details.costEfficiency.toFixed(1)}%
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
                    {missionResults.details.impactPrevented 
                      ? 'No atmospheric contamination' 
                      : 'Minimal dust ejection, negligible cooling effects'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Ecosystem Impact</h4>
                  <p className="text-white">
                    {missionResults.details.impactPrevented 
                      ? 'No ecosystem damage' 
                      : 'Local wildlife impact: Moderate'
                    }
                  </p>
                </div>
                
                <div>
                  <h4 className="text-sm font-medium text-gray-300 mb-2">Wildfire Risk</h4>
                  <p className="text-white">
                    {missionResults.details.impactPrevented 
                      ? 'No wildfire risk' 
                      : 'Thermal radiation radius: 2.1 km'
                    }
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Deployed Assets Summary */}
      {deployedAssets.length > 0 && (
        <div className="bg-gray-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-white mb-3">
            Deployed Assets ({deployedAssets.length})
          </h3>
          <div className="space-y-2">
            {deployedAssets.map((asset) => (
              <div key={asset.id} className="flex items-center justify-between p-2 bg-gray-600 rounded">
                <div>
                  <p className="text-sm text-white">{asset.name}</p>
                  <p className="text-xs text-gray-400">
                    Deployed at {new Date(asset.deployedAt).toLocaleTimeString()}
                  </p>
                </div>
                <p className="text-sm text-gray-300">{formatCurrency(asset.cost)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
