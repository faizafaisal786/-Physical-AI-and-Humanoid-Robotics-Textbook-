const express = require('express');
const path = require('path');
const { betterAuth } = require('better-auth');
const { cors } = require('better-auth/plugins');

// Initialize BetterAuth
const auth = betterAuth({
  secret: process.env.AUTH_SECRET || 'fallback-secret-change-this',
  baseURL: process.env.BASE_URL || 'http://localhost:3000',
  app: {
    name: 'Physical AI & Humanoid Robotics Textbook',
  },
  database: {
    provider: 'sqlite',
    url: process.env.DATABASE_URL || './db.sqlite',
  },
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    },
  },
  plugins: [
    cors({
      allowedOrigins: [
        'http://localhost:3000',
        'http://localhost:3001', 
        'http://localhost:8000', // Python backend
        process.env.FRONTEND_URL || 'https://physical-ai-textbook.vercel.app'
      ],
    }),
  ],
});

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use('/api/auth', auth);

// Serve static files from build directory in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'build')));

  // Handle React Router by serving index.html for any non-API routes
  app.get(/^(?!\/api\/auth\/?).*/, (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
  });
} else {
  // In development, proxy requests to Docusaurus dev server
  const { createProxyMiddleware } = require('http-proxy-middleware');

  // Proxy everything except /api/auth to Docusaurus dev server
  app.use(
    (req, res, next) => {
      // If it's an auth API request, handle normally
      if (req.path.startsWith('/api/auth')) {
        next();
      } else {
        // Otherwise, proxy to Docusaurus dev server
        createProxyMiddleware({
          target: 'http://localhost:3000',
          changeOrigin: true,
          logLevel: 'silent',
        })(req, res, next);
      }
    }
  );
}

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Authentication endpoints available at /api/auth`);
});