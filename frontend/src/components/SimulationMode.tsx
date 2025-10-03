'use client';

import { useState } from 'react';
import ScenarioHub from './ScenarioHub';
import ConsequenceReport from './ConsequenceReport';
import EnhancedCesiumViewer from './EnhancedCesiumViewer';
import MasterControls from './MasterControls';

export default function SimulationMode() {
  const [leftSidebarCollapsed, setLeftSidebarCollapsed] = useState(false);
  const [rightSidebarCollapsed, setRightSidebarCollapsed] = useState(true);
  const [selectedAsteroid, setSelectedAsteroid] = useState<any>(null);
  const [impactData, setImpactData] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const handleAsteroidSelect = (asteroid: any) => {
    setSelectedAsteroid(asteroid);
    setRightSidebarCollapsed(false);
  };

  const handleSimulationComplete = (data: any) => {
    setImpactData(data);
    setRightSidebarCollapsed(false);
  };

  return (
    <div className="relative w-full" style={{ height: 'calc(100vh - 73px)' }}>
      {/* Left Sidebar - Scenario Hub */}
      <div className={`absolute top-0 left-0 h-full transition-all duration-300 ${
        leftSidebarCollapsed ? 'w-12 bg-gray-900' : 'w-80 bg-gray-900 bg-opacity-80 backdrop-blur-sm'
      } border-r border-gray-700 flex flex-col z-20`}>
        {leftSidebarCollapsed ? (
          <button
            onClick={() => setLeftSidebarCollapsed(false)}
            className="p-3 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
            title="Expand Scenario Hub"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        ) : (
          <>
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Scenario Hub</h2>
              <button
                onClick={() => setLeftSidebarCollapsed(true)}
                className="p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors"
                title="Collapse"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
            </div>
            <ScenarioHub 
              onAsteroidSelect={handleAsteroidSelect}
              selectedAsteroid={selectedAsteroid}
            />
          </>
        )}
      </div>

      {/* Main 3D Viewport - Full Screen */}
      <div 
        className="absolute inset-0 z-0"
        style={{
          width: '100%',
          height: '100%',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0
        }}
      >
        <EnhancedCesiumViewer
          selectedAsteroid={selectedAsteroid}
          impactData={impactData}
          isSimulating={isSimulating}
          mode="simulation"
        />
      </div>

      {/* Bottom Controls - Floating */}
      <div className="absolute bottom-0 left-0 right-0 z-30">
        <MasterControls 
          onSimulationStart={() => setIsSimulating(true)}
          onSimulationComplete={handleSimulationComplete}
          selectedAsteroid={selectedAsteroid}
        />
      </div>

      {/* Right Sidebar - Consequence Report */}
      <div className={`absolute top-0 right-0 h-full transition-all duration-300 ${
        rightSidebarCollapsed ? 'w-12 bg-gray-900' : 'w-96 bg-gray-900 bg-opacity-80 backdrop-blur-sm'
      } border-l border-gray-700 flex flex-col z-20`}>
        {rightSidebarCollapsed ? (
          <button
            onClick={() => setRightSidebarCollapsed(false)}
            className="p-3 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
            title="Expand Consequence Report"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        ) : (
          <>
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Consequence Report</h2>
              <button
                onClick={() => setRightSidebarCollapsed(true)}
                className="p-1 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors"
                title="Collapse"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
            <ConsequenceReport 
              impactData={impactData}
              selectedAsteroid={selectedAsteroid}
            />
          </>
        )}
      </div>
    </div>
  );
}
