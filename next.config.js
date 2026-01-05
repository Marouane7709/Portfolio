/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com'], // Add any other image domains you need
  },
  reactStrictMode: true,
  swcMinify: true,
};

module.exports = nextConfig; 