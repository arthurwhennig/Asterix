'use client';

import { useEffect, useRef } from 'react';
import * as Cesium from 'cesium';

// Set Cesium base path
if (typeof window !== 'undefined') {
  (window as any).CESIUM_BASE_URL = '/cesium/';
}

export default function CesiumViewer() {
  const cesiumContainer = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);

  useEffect(() => {
    if (cesiumContainer.current && !viewerRef.current) {
      try {
        // Initialize Cesium viewer
        const viewer = new Cesium.Viewer(cesiumContainer.current, {
          terrainProvider: new Cesium.EllipsoidTerrainProvider(),
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
        });

        // Set initial view
        viewer.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(-75.59777, 40.03883, 10000000),
        });

        // Add some sample asteroids as billboards
        const asteroidPositions = [
          { longitude: -75.59777, latitude: 40.03883, height: 1000000 },
          { longitude: -100.0, latitude: 30.0, height: 2000000 },
          { longitude: 0.0, latitude: 0.0, height: 1500000 },
          { longitude: 120.0, latitude: -30.0, height: 3000000 },
        ];

        asteroidPositions.forEach((pos, index) => {
          viewer.entities.add({
            position: Cesium.Cartesian3.fromDegrees(pos.longitude, pos.latitude, pos.height),
            billboard: {
              image: '/asteroid-icon.svg',
              scale: 0.5,
              verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            },
            label: {
              text: `Asteroid ${index + 1}`,
              font: '12pt sans-serif',
              pixelOffset: new Cesium.Cartesian2(0, -50),
              fillColor: Cesium.Color.YELLOW,
              outlineColor: Cesium.Color.BLACK,
              outlineWidth: 2,
              style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            },
          });
        });

        // Add Earth's atmosphere
        viewer.scene.skyAtmosphere.show = true;
        viewer.scene.globe.enableLighting = true;

        viewerRef.current = viewer;

        // Cleanup function
        return () => {
          if (viewerRef.current) {
            viewerRef.current.destroy();
            viewerRef.current = null;
          }
        };
      } catch (error) {
        console.error('Error initializing Cesium:', error);
      }
    }
  }, []);

  return (
    <div className="w-full h-full">
      <div
        ref={cesiumContainer}
        className="w-full h-full rounded-lg"
        style={{ minHeight: '400px' }}
      />
    </div>
  );
}
