'use client';

import dynamic from 'next/dynamic';

// Dynamically import MainLayout to avoid SSR issues
const MainLayout = dynamic(() => import('../components/MainLayout'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-screen bg-gray-900 text-white">Loading Asterix...</div>
});

export default function Home() {
  return <MainLayout />;
}