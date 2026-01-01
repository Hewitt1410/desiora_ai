const createNextIntlPlugin = require('next-intl/plugin');

const withNextIntl = createNextIntlPlugin('./i18n.ts');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  images: {
    domains: ['localhost'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  // Disable static optimization for pages that use dynamic features
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
  webpack: (config, { isServer }) => {
    // Fix for axios vendor chunks issue
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
      
      // Optimize axios bundling
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          ...config.optimization.splitChunks,
          cacheGroups: {
            ...config.optimization.splitChunks.cacheGroups,
            default: false,
            vendors: false,
            // Create a separate chunk for axios
            axios: {
              name: 'axios',
              test: /[\\/]node_modules[\\/]axios[\\/]/,
              priority: 20,
              reuseExistingChunk: true,
            },
          },
        },
      };
    }
    
    return config;
  },
}

module.exports = withNextIntl(nextConfig);
