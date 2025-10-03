'use client';

import { useState } from 'react';
import MissionBriefing from './MissionBriefing';
import MissionReport from './MissionReport';
import EnhancedCesiumViewer from './EnhancedCesiumViewer';
import AssetDeployment from './AssetDeployment';

export default function DefenseMode() {
  const [leftSidebarCollapsed, setLeftSidebarCollapsed] = useState(false);
  const [rightSidebarCollapsed, setRightSidebarCollapsed] = useState(true);
  const [selectedThreat, setSelectedThreat] = useState<any>(null);
  const [deployedAssets, setDeployedAssets] = useState<any[]>([]);
  const [budget, setBudget] = useState(1000000000000); // $1T budget
  const [usedBudget, setUsedBudget] = useState(0);
  const [missionCompleted, setMissionCompleted] = useState(false);
  const [missionResults, setMissionResults] = useState<any>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const handleThreatSelect = (threat: any) => {
    setSelectedThreat(threat);
    setRightSidebarCollapsed(false);
  };

  const handleAssetDeploy = (asset: any, position: any) => {
    const newAsset = {
      id: Date.now().toString(),
      type: asset.type,
      name: asset.name,
      cost: asset.cost,
      position: position,
      deployedAt: new Date().toISOString(),
    };
    
    setDeployedAssets(prev => [...prev, newAsset]);
    setUsedBudget(prev => prev + asset.cost);
  };

  const handleAssetRemove = (assetId: string) => {
    const asset = deployedAssets.find(a => a.id === assetId);
    if (asset) {
      setDeployedAssets(prev => prev.filter(a => a.id !== assetId));
      setUsedBudget(prev => prev - asset.cost);
    }
  };

  const handleExecuteDefense = async () => {
    setIsExecuting(true);
    
    // Simulate mission execution
    setTimeout(() => {
      // Mock mission results
      const results = {
        success: Math.random() > 0.3, // 70% success rate
        score: Math.floor(Math.random() * 3) + 1, // 1-3 stars
        totalCost: usedBudget,
        consequencesMitigated: Math.random() * 100,
        details: {
          asteroidDeflected: Math.random() > 0.3,
          impactPrevented: Math.random() > 0.5,
          costEfficiency: Math.random() * 100,
        }
      };
      
      setMissionResults(results);
      setMissionCompleted(true);
      setIsExecuting(false);
      setRightSidebarCollapsed(false);
    }, 3000);
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Left Sidebar - Mission Briefing & Asset Deployment */}
      <div className={`transition-all duration-300 ${
        leftSidebarCollapsed ? 'w-12' : 'w-80'
      } bg-gray-800 border-r border-gray-700 flex flex-col`}>
        {leftSidebarCollapsed ? (
          <button
            onClick={() => setLeftSidebarCollapsed(false)}
            className="p-3 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
            title="Expand Mission Briefing"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        ) : (
          <>
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Mission Briefing</h2>
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
            <MissionBriefing 
              onThreatSelect={handleThreatSelect}
              selectedThreat={selectedThreat}
            />
          </>
        )}
      </div>

      {/* Main 3D Viewport */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 relative">
          <EnhancedCesiumViewer
            selectedAsteroid={selectedThreat}
            impactData={null}
            isSimulating={isExecuting}
            mode="defense"
            deployedAssets={deployedAssets}
            onAssetRemove={handleAssetRemove}
          />
        </div>
        
        {/* Asset Deployment Bar */}
        <AssetDeployment
          onAssetDeploy={handleAssetDeploy}
          deployedAssets={deployedAssets}
          budget={budget}
          usedBudget={usedBudget}
          onExecuteDefense={handleExecuteDefense}
          isExecuting={isExecuting}
          selectedThreat={selectedThreat}
        />
      </div>

      {/* Right Sidebar - Mission Report */}
      <div className={`transition-all duration-300 ${
        rightSidebarCollapsed ? 'w-12' : 'w-96'
      } bg-gray-800 border-l border-gray-700 flex flex-col`}>
        {rightSidebarCollapsed ? (
          <button
            onClick={() => setRightSidebarCollapsed(false)}
            className="p-3 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
            title="Expand Mission Report"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        ) : (
          <>
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Mission Report</h2>
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
            <MissionReport 
              missionResults={missionResults}
              missionCompleted={missionCompleted}
              isExecuting={isExecuting}
              deployedAssets={deployedAssets}
              selectedThreat={selectedThreat}
            />
          </>
        )}
      </div>
    </div>
  );
}
