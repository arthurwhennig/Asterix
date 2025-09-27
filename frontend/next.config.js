/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Handle Cesium
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        os: false,
      };
    }

    // Copy Cesium assets
    config.module.rules.push({
      test: /\.(js|mjs)$/,
      include: /node_modules\/cesium/,
      use: {
        loader: 'file-loader',
        options: {
          outputPath: 'static/cesium/',
          publicPath: '/_next/static/cesium/',
        },
      },
    });

    return config;
  },
  // Enable static file serving for Cesium
  async rewrites() {
    return [
      {
        source: '/cesium/:path*',
        destination: '/cesium/:path*',
      },
    ];
  },
  // Disable image optimization for Cesium assets
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
