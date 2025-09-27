'use client';

import { useEffect, useRef } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import Cesium to avoid SSR issues
const CesiumViewer = dynamic(() => import('../components/CesiumViewer'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-screen">Loading 3D Earth...</div>
});

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            Asterix - Asteroid Visualization Tool
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            Explore asteroids, simulate impacts, and protect Earth from cosmic threats
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 3D Earth Viewer */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg p-4">
              <h2 className="text-2xl font-semibold text-white mb-4">3D Earth Visualization</h2>
              <div className="relative h-96 rounded-lg overflow-hidden">
                <CesiumViewer />
              </div>
            </div>
          </div>

          {/* Features Panel */}
          <div className="space-y-6">
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Features</h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Real-time asteroid tracking
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                  Impact simulation
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full mr-3"></span>
                  Game mode
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3"></span>
                  Historical data
                </li>
              </ul>
            </div>

            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                  View Asteroids
                </button>
                <button className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                  Start Simulation
                </button>
                <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                  Play Game
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gray-800 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-blue-400 mb-2">1,000+</div>
            <div className="text-gray-300">Tracked Asteroids</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-green-400 mb-2">50+</div>
            <div className="text-gray-300">Simulations Created</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 text-center">
            <div className="text-3xl font-bold text-yellow-400 mb-2">100+</div>
            <div className="text-gray-300">Players Protected Earth</div>
          </div>
        </div>
      </div>
    </main>
  );
}