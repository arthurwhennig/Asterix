'use client';

import { useState } from 'react';

interface Asset {
  type: string;
  name: string;
  cost: number;
  description: string;
  icon: string;
}

interface DeployedAsset {
  id: string;
  type: string;
  name: string;
  cost: number;
  position: any;
  deployedAt: string;
}

interface AssetDeploymentProps {
  onAssetDeploy: (asset: Asset, position: any) => void;
  deployedAssets: DeployedAsset[];
  budget: number;
  usedBudget: number;
  onExecuteDefense: () => void;
  isExecuting: boolean;
  selectedThreat: any;
}

export default function AssetDeployment({
  onAssetDeploy,
  deployedAssets,
  budget,
  usedBudget,
  onExecuteDefense,
  isExecuting,
  selectedThreat
}: AssetDeploymentProps) {
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [isDeploying, setIsDeploying] = useState(false);

  const availableAssets: Asset[] = [
    {
      type: 'kinetic_impactor',
      name: 'Kinetic Impactor',
      cost: 50000000000, // $50B
      description: 'High-speed spacecraft that impacts the asteroid to change its trajectory',
      icon: '🚀'
    },
    {
      type: 'laser_ablation',
      name: 'Laser Ablation',
      cost: 100000000000, // $100B
      description: 'High-power laser system that vaporizes asteroid material to create thrust',
      icon: '🔦'
    },
    {
      type: 'gravity_tractor',
      name: 'Gravity Tractor',
      cost: 75000000000, // $75B
      description: 'Large spacecraft that uses gravitational force to gradually pull the asteroid',
      icon: '🛰️'
    },
    {
      type: 'nuclear_device',
      name: 'Nuclear Device',
      cost: 20000000000, // $20B
      description: 'Nuclear explosive device to fragment or deflect the asteroid',
      icon: '💥'
    },
    {
      type: 'solar_sail',
      name: 'Solar Sail',
      cost: 30000000000, // $30B
      description: 'Large reflective sail that uses solar radiation pressure for propulsion',
      icon: '⛵'
    },
    {
      type: 'mass_driver',
      name: 'Mass Driver',
      cost: 80000000000, // $80B
      description: 'Electromagnetic launcher that ejects asteroid material to create thrust',
      icon: '⚡'
    }
  ];

  const handleAssetSelect = (asset: Asset) => {
    setSelectedAsset(asset);
    setIsDeploying(true);
  };

  const handleEarthClick = (event: React.MouseEvent) => {
    if (selectedAsset && isDeploying) {
      // Mock position calculation based on click coordinates
      const rect = event.currentTarget.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      
      const position = {
        x: x / rect.width,
        y: y / rect.height,
        longitude: (x / rect.width) * 360 - 180,
        latitude: 90 - (y / rect.height) * 180
      };
      
      onAssetDeploy(selectedAsset, position);
      setSelectedAsset(null);
      setIsDeploying(false);
    }
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

  const budgetPercentage = (usedBudget / budget) * 100;

  return (
    <div className="bg-gray-800 bg-opacity-95 border-t border-gray-700 p-4 backdrop-blur-sm">
      {/* Budget Display */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-white">Defense Budget</h3>
          <span className="text-sm text-gray-300">
            {formatCurrency(usedBudget)} / {formatCurrency(budget)}
          </span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3">
          <div 
            className={`h-3 rounded-full transition-all duration-300 ${
              budgetPercentage > 90 ? 'bg-red-500' : 
              budgetPercentage > 70 ? 'bg-yellow-500' : 'bg-green-500'
            }`}
            style={{ width: `${Math.min(budgetPercentage, 100)}%` }}
          />
        </div>
        <p className="text-xs text-gray-400 mt-1">
          {budgetPercentage.toFixed(1)}% of budget used
        </p>
      </div>

      {/* Asset Arsenal */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white mb-3">Asset Arsenal</h3>
        <div className="grid grid-cols-3 gap-3">
          {availableAssets.map((asset) => {
            const canAfford = (budget - usedBudget) >= asset.cost;
            const isSelected = selectedAsset?.type === asset.type;
            
            return (
              <button
                key={asset.type}
                onClick={() => handleAssetSelect(asset)}
                disabled={!canAfford || isExecuting}
                className={`p-3 rounded-lg border transition-all ${
                  isSelected
                    ? 'border-green-500 bg-green-900/20 ring-2 ring-green-500'
                    : canAfford
                    ? 'border-gray-600 bg-gray-700 hover:border-gray-500 hover:bg-gray-600'
                    : 'border-gray-700 bg-gray-800 opacity-50 cursor-not-allowed'
                }`}
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">{asset.icon}</div>
                  <h4 className="font-medium text-white text-sm">{asset.name}</h4>
                  <p className="text-xs text-gray-400 mt-1">{formatCurrency(asset.cost)}</p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Deployment Instructions */}
      {isDeploying && selectedAsset && (
        <div className="mb-4 p-3 bg-blue-900/20 border border-blue-500 rounded-lg">
          <p className="text-blue-300 text-sm">
            <strong>Deploying {selectedAsset.name}</strong><br/>
            Click on the Earth to place this asset. Press ESC to cancel.
          </p>
        </div>
      )}

      {/* Deployed Assets Summary */}
      {deployedAssets.length > 0 && (
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-white mb-3">Deployed Assets ({deployedAssets.length})</h3>
          <div className="grid grid-cols-2 gap-2">
            {deployedAssets.map((asset) => (
              <div key={asset.id} className="p-2 bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-white">{asset.name}</p>
                    <p className="text-xs text-gray-400">{formatCurrency(asset.cost)}</p>
                  </div>
                  <button
                    onClick={() => {
                      // Handle asset removal
                      const index = deployedAssets.findIndex(a => a.id === asset.id);
                      if (index > -1) {
                        const updatedAssets = [...deployedAssets];
                        updatedAssets.splice(index, 1);
                        // Update deployed assets
                      }
                    }}
                    className="text-red-400 hover:text-red-300 text-sm"
                    disabled={isExecuting}
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Execute Button */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-400">
          {selectedThreat ? (
            <span>Ready to defend against {selectedThreat.name}</span>
          ) : (
            <span>Select a threat to begin defense planning</span>
          )}
        </div>
        
        <button
          onClick={onExecuteDefense}
          disabled={!selectedThreat || deployedAssets.length === 0 || isExecuting}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${
            isExecuting
              ? 'bg-yellow-600 text-white'
              : selectedThreat && deployedAssets.length > 0
              ? 'bg-red-600 hover:bg-red-700 text-white'
              : 'bg-gray-600 text-gray-400 cursor-not-allowed'
          }`}
        >
          {isExecuting ? 'Executing Defense Plan...' : 'EXECUTE DEFENSE PLAN'}
        </button>
      </div>

      {/* Click handler for Earth */}
      {isDeploying && (
        <div 
          className="fixed inset-0 z-50 cursor-crosshair"
          onClick={handleEarthClick}
          onKeyDown={(e) => {
            if (e.key === 'Escape') {
              setSelectedAsset(null);
              setIsDeploying(false);
            }
          }}
          tabIndex={0}
        />
      )}
    </div>
  );
}
