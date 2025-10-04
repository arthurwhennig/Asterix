'use client';

import { useEffect, useRef } from 'react';
import * as Cesium from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';

// Set Cesium base path and access token
if (typeof window !== 'undefined') {
  (window as { CESIUM_BASE_URL?: string }).CESIUM_BASE_URL = "/cesium/";
  // Set the Cesium Ion access token
  Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhOGE4ZTU1My00MWZhLTRhY2YtOWY0Zi02ZmJiMzlmMTA0NTQiLCJpZCI6MzQ2OTQ2LCJpYXQiOjE3NTk1MTg4NTN9.P1FImMkJczHJVSERLAWrrFPJOLEE9J4_8rh7qCJP-l4';
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
  damageZones: Record<string, unknown>;
}

interface DeployedAsset {
  id: string;
  type: string;
  name: string;
  cost: number;
  position: { longitude: number; latitude: number };
  deployedAt: string;
}

interface EnhancedCesiumViewerProps {
  selectedAsteroid: Asteroid | null;
  impactData: ImpactData | null;
  isSimulating: boolean;
  mode: "simulation" | "defense";
  deployedAssets?: DeployedAsset[];
  _onAssetRemove?: (assetId: string) => void;
}

export default function EnhancedCesiumViewer({
  selectedAsteroid,
  impactData,
  isSimulating,
  mode,
  deployedAssets = [],
  _onAssetRemove,
}: EnhancedCesiumViewerProps) {
  const cesiumContainer = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);
  const entitiesRef = useRef<Cesium.Entity[]>([]);

  // Centralized cleanup function to clear all simulation entities
  const clearAllEntities = () => {
    if (viewerRef.current) {
      entitiesRef.current.forEach((entity) => {
        viewerRef.current!.entities.remove(entity);
      });
      entitiesRef.current = [];
    }
  };

  useEffect(() => {
    // This effect hook will now handle the viewer's lifecycle
    // based on the container div's actual size.

    const container = cesiumContainer.current;
    if (!container) return; // Exit if the ref isn't attached yet

    const resizeObserver = new ResizeObserver(() => {
      // This callback runs when the container is first painted or resized.
      // We only want to run the initialization logic ONCE.
      if (container && container.clientHeight > 0 && !viewerRef.current) {
        try {
          console.log("Container has size, initializing Cesium viewer...");
          console.log("Container dimensions:", {
            width: container.clientWidth,
            height: container.clientHeight,
          });

          // Set the Cesium Ion access token
          Cesium.Ion.defaultAccessToken =
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhOGE4ZTU1My00MWZhLTRhY2YtOWY0Zi02ZmJiMzlmMTA0NTQiLCJpZCI6MzQ2OTQ2LCJpYXQiOjE3NTk1MTg4NTN9.P1FImMkJczHJVSERLAWrrFPJOLEE9J4_8rh7qCJP-l4";

          const viewer = new Cesium.Viewer(container, {
            // Your existing options
            homeButton: false,
            sceneModePicker: false,
            baseLayerPicker: false,
            navigationHelpButton: false,
            animation: false,
            timeline: false,
            fullscreenButton: false,
            vrButton: false,
            geocoder: false,
            infoBox: false,
            selectionIndicator: false,
            // This is still very important for crisp visuals
            useBrowserRecommendedResolution: true,
          });

          viewer.scene.globe.enableLighting = true;
          if (viewer.scene.skyAtmosphere) {
            viewer.scene.skyAtmosphere.show = true;
          }

          // Add error handling for imagery loading
          viewer.scene.globe.imageryLayers.layerAdded.addEventListener(
            (layer) => {
              layer.errorEvent.addEventListener((error) => {
                console.warn("Imagery layer error:", error);
              });
            }
          );

          // Set initial view based on mode
          if (mode === "simulation") {
            viewer.camera.setView({
              destination: Cesium.Cartesian3.fromDegrees(
                -75.59777,
                40.03883,
                10000000
              ),
            });
          } else {
            // Defense mode - solar system view
            viewer.camera.setView({
              destination: Cesium.Cartesian3.fromDegrees(0, 0, 50000000),
            });
          }

          // Add some sample asteroids for demonstration
          const asteroidPositions = [
            { longitude: -75.59777, latitude: 40.03883, height: 1000000 },
            { longitude: -100.0, latitude: 30.0, height: 2000000 },
            { longitude: 0.0, latitude: 0.0, height: 1500000 },
            { longitude: 120.0, latitude: -30.0, height: 3000000 },
          ];

          asteroidPositions.forEach((pos, index) => {
            const entity = viewer.entities.add({
              position: Cesium.Cartesian3.fromDegrees(
                pos.longitude,
                pos.latitude,
                pos.height
              ),
              billboard: {
                image: "/asteroid-icon.svg",
                scale: 0.5,
                verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
              },
              label: {
                text: `Asteroid ${index + 1}`,
                font: "12pt sans-serif",
                pixelOffset: new Cesium.Cartesian2(0, -50),
                fillColor: Cesium.Color.YELLOW,
                outlineColor: Cesium.Color.BLACK,
                outlineWidth: 2,
                style: Cesium.LabelStyle.FILL_AND_OUTLINE,
              },
            });
            entitiesRef.current.push(entity);
          });

          viewerRef.current = viewer; // Save the viewer instance

          // Once the viewer is created, we don't need the observer anymore
          resizeObserver.disconnect();
          console.log("Cesium viewer initialized and observer disconnected.");
        } catch (error) {
          console.error("Error initializing Cesium:", error);
          console.error("Error details:", {
            message: error.message,
            stack: error.stack,
            container: container,
            cesiumAvailable: typeof Cesium !== "undefined",
          });
        }
      }
    });

    // Start observing the container element
    resizeObserver.observe(container);

    // Cleanup function: This is crucial for React
    return () => {
      resizeObserver.disconnect();
      if (viewerRef.current && !viewerRef.current.isDestroyed()) {
        viewerRef.current.destroy();
        viewerRef.current = null;
      }
    };

    // We remove all dependencies from the array. This hook should run
    // only once when the component mounts.
  }, [mode]); // Include mode dependency

  // Update visualization when asteroid is selected
  useEffect(() => {
    // Clear ALL previous entities before adding new ones
    clearAllEntities();

    if (viewerRef.current && selectedAsteroid) {
      // Add selected asteroid visualization
      const asteroidEntity = viewerRef.current.entities.add({
        position: Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883, 1000000),
        billboard: {
          image: "/asteroid-icon.svg",
          scale: Math.max(0.3, Math.min(2.0, selectedAsteroid.diameter * 0.5)),
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          color: selectedAsteroid.isHazardous
            ? Cesium.Color.RED
            : Cesium.Color.YELLOW,
        },
        label: {
          text: selectedAsteroid.name,
          font: "14pt sans-serif",
          pixelOffset: new Cesium.Cartesian2(0, -60),
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 2,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        },
      });
      entitiesRef.current.push(asteroidEntity);

      // Add trajectory
      const trajectoryEntity = viewerRef.current.entities.add({
        polyline: {
          positions: [
            Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883, 1000000),
            Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883, 0),
          ],
          width: 3,
          material: Cesium.Color.ORANGE,
          clampToGround: true,
        },
      });
      entitiesRef.current.push(trajectoryEntity);
    }
  }, [selectedAsteroid]);

  // Update visualization when impact data is available
  useEffect(() => {
    // NOTE: Do NOT clear all entities here. Just add the new ones.
    // The selection hook has already cleared the board.

    if (viewerRef.current && impactData) {
      const impactPosition = Cesium.Cartesian3.fromDegrees(
        -75.59777,
        40.03883,
        0
      );

      // Add crater
      const craterEntity = viewerRef.current.entities.add({
        position: impactPosition,
        ellipse: {
          semiMajorAxis: (impactData.crater.diameterKm * 1000) / 2,
          semiMinorAxis: (impactData.crater.diameterKm * 1000) / 2,
          material: Cesium.Color.GRAY.withAlpha(0.7),
          height: 0,
          extrudedHeight: -impactData.crater.depthKm * 1000,
        },
      });
      entitiesRef.current.push(craterEntity);

      // Add airblast rings
      Object.entries(impactData.airblast.blastRadiiKm).forEach(
        ([psi, radiusKm], index) => {
          const colors = [
            Cesium.Color.YELLOW.withAlpha(0.3),
            Cesium.Color.ORANGE.withAlpha(0.3),
            Cesium.Color.RED.withAlpha(0.3),
            Cesium.Color.PURPLE.withAlpha(0.3),
          ];

          const ringEntity = viewerRef.current!.entities.add({
            position: impactPosition,
            ellipse: {
              semiMajorAxis: radiusKm * 1000,
              semiMinorAxis: radiusKm * 1000,
              material: colors[index % colors.length],
              height: 0,
              outline: true,
              outlineColor: colors[index % colors.length],
            },
            label: {
              text: `${psi} PSI`,
              font: "10pt sans-serif",
              pixelOffset: new Cesium.Cartesian2(0, -30),
              fillColor: Cesium.Color.WHITE,
              outlineColor: Cesium.Color.BLACK,
              outlineWidth: 1,
              style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            },
          });
          entitiesRef.current.push(ringEntity);
        }
      );

      // Add fireball
      const fireballEntity = viewerRef.current.entities.add({
        position: impactPosition,
        billboard: {
          image: "/fireball-icon.svg",
          scale: impactData.airblast.fireballRadiusKm * 100,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          color: Cesium.Color.ORANGE.withAlpha(0.8),
        },
      });
      entitiesRef.current.push(fireballEntity);

      // Add thermal radiation zone
      const thermalEntity = viewerRef.current.entities.add({
        position: impactPosition,
        ellipse: {
          semiMajorAxis: impactData.thermal.thermalRadiusKm * 1000,
          semiMinorAxis: impactData.thermal.thermalRadiusKm * 1000,
          material: Cesium.Color.RED.withAlpha(0.2),
          height: 0,
          outline: true,
          outlineColor: Cesium.Color.RED,
        },
        label: {
          text: `Thermal Radiation`,
          font: "10pt sans-serif",
          pixelOffset: new Cesium.Cartesian2(0, -30),
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 1,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        },
      });
      entitiesRef.current.push(thermalEntity);
    }
  }, [impactData]);

  // Handle mode changes - only update camera if mode actually changed
  useEffect(() => {
    if (viewerRef.current) {
      if (mode === "defense") {
        // Switch to solar system view for defense mode
        viewerRef.current.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(0, 0, 50000000),
        });
      } else {
        // Switch back to Earth view for simulation mode
        viewerRef.current.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(
            -75.59777,
            40.03883,
            10000000
          ),
        });
      }
    }
  }, [mode]);

  // Handle deployed assets visualization
  useEffect(() => {
    if (viewerRef.current && mode === "defense") {
      // Clear existing asset entities
      entitiesRef.current.forEach((entity) => {
        if (entity.name && entity.name.startsWith("asset_")) {
          viewerRef.current!.entities.remove(entity);
        }
      });

      // Add deployed assets
      deployedAssets.forEach((asset) => {
        const position = Cesium.Cartesian3.fromDegrees(
          asset.position.longitude,
          asset.position.latitude,
          0
        );

        const assetEntity = viewerRef.current!.entities.add({
          position: position,
          billboard: {
            image: getAssetIcon(asset.type),
            scale: 0.8,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            color: Cesium.Color.CYAN,
          },
          label: {
            text: asset.name,
            font: "12pt sans-serif",
            pixelOffset: new Cesium.Cartesian2(0, -50),
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          },
          name: `asset_${asset.id}`,
        });
        entitiesRef.current.push(assetEntity);
      });
    }
  }, [deployedAssets, mode]);

  const getAssetIcon = (assetType: string) => {
    // Return appropriate icon based on asset type
    switch (assetType) {
      case "kinetic_impactor":
        return "/kinetic-impactor-icon.svg";
      case "laser_ablation":
        return "/laser-icon.svg";
      case "gravity_tractor":
        return "/gravity-tractor-icon.svg";
      case "nuclear_device":
        return "/nuclear-icon.svg";
      case "solar_sail":
        return "/solar-sail-icon.svg";
      case "mass_driver":
        return "/mass-driver-icon.svg";
      default:
        return "/asteroid-icon.svg";
    }
  };

  return (
    <div className="w-full h-full relative">
      <div
        id="cesiumContainer"
        ref={cesiumContainer}
        className="absolute inset-0 w-full h-full"
        style={{
          width: "100%",
          height: "100%",
          minWidth: "100%",
          minHeight: "100%",
        }}
      />

      {/* Overlay for mode-specific UI elements */}
      {mode === "defense" && (
        <div className="absolute top-4 left-4 bg-gray-800 bg-opacity-90 rounded-lg p-3 z-10">
          <h3 className="text-white font-semibold mb-2">Defense Mode</h3>
          <p className="text-gray-300 text-sm">
            Strategic view for asset deployment
          </p>
        </div>
      )}

      {mode === "simulation" && isSimulating && (
        <div className="absolute top-4 right-4 bg-red-800 bg-opacity-90 rounded-lg p-3 z-10">
          <h3 className="text-white font-semibold mb-2">Simulation Running</h3>
          <p className="text-gray-300 text-sm">Impact sequence in progress</p>
        </div>
      )}
    </div>
  );
}
