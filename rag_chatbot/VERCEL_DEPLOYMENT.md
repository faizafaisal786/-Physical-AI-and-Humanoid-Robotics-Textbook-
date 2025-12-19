# Vercel Deployment Guide

This guide explains how to deploy the RAG Chatbot to Vercel.

## Architecture

The deployment consists of two main components:

1. **Frontend**: Docusaurus static site with integrated ChatWidget
2. **Backend**: Python serverless functions for RAG API endpoints

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI (optional but recommended):
   ```bash
   npm install -g vercel
   ```
3. Required API keys:
   - Cohere API key (get from https://cohere.com)
   - Qdrant database URL and API key (get from https://qdrant.tech)

## Project Structure

```
rag_chatbot/
├── api/                      # Vercel serverless functions
│   ├── ask.py               # Main RAG query endpoint
│   ├── health.py            # Health check endpoint
│   └── requirements.txt     # Python dependencies for API
├── backend/                  # Shared backend code
│   ├── agent.py             # RAG agent implementation
│   ├── retrieving.py        # Retrieval logic
│   └── requirements.txt     # Backend dependencies
├── docusaurus_textbook/      # Docusaurus frontend
│   ├── src/
│   │   └── components/
│   │       └── ChatWidget.js # Chat interface
│   └── package.json
├── vercel.json              # Vercel configuration
├── .vercelignore            # Files to exclude from deployment
└── VERCEL_DEPLOYMENT.md     # This file
```

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended for first-time)

1. **Connect to Vercel**:
   - Go to https://vercel.com/new
   - Import your Git repository (GitHub, GitLab, or Bitbucket)
   - Vercel will automatically detect the configuration from `vercel.json`

2. **Configure Environment Variables**:
   In your Vercel project settings, add these environment variables:

   | Variable Name     | Description                        | Example                              |
   |-------------------|------------------------------------|--------------------------------------|
   | `COHERE_API_KEY`  | Your Cohere API key                | `your-cohere-api-key-here`          |
   | `QDRANT_URL`      | Your Qdrant database URL           | `https://your-cluster.qdrant.io`    |
   | `QDRANT_API_KEY`  | Your Qdrant API key                | `your-qdrant-api-key-here`          |

   To add environment variables:
   - Go to your project in Vercel Dashboard
   - Navigate to **Settings** > **Environment Variables**
   - Add each variable with its value
   - Make sure to add them for all environments (Production, Preview, Development)

3. **Deploy**:
   - Click **Deploy**
   - Vercel will build and deploy your project
   - The first deployment may take 2-3 minutes

4. **Verify Deployment**:
   - Once deployed, visit your Vercel URL (e.g., `https://your-project.vercel.app`)
   - Test the health endpoint: `https://your-project.vercel.app/api/health`
   - Try the chat widget on the homepage

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd rag_chatbot
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy: Yes
   - Which scope: Select your account
   - Link to existing project: No (for first deployment)
   - Project name: Enter your desired name
   - Directory: `./` (current directory)

5. **Set Environment Variables**:
   ```bash
   vercel env add COHERE_API_KEY
   vercel env add QDRANT_URL
   vercel env add QDRANT_API_KEY
   ```
   Enter the values when prompted.

6. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

## API Endpoints

After deployment, your API will be available at:

### POST /api/ask
Query the RAG agent with a question.

**Request:**
```json
{
  "query": "What is ROS2?"
}
```

**Response:**
```json
{
  "answer": "ROS2 is...",
  "sources": ["https://docs.ros.org/..."],
  "matched_chunks": [
    {
      "content": "...",
      "url": "https://...",
      "position": 0,
      "similarity_score": 0.95
    }
  ],
  "status": "success",
  "query_time_ms": 1234.5
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "RAG Agent API is running on Vercel"
}
```

## Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Navigate to **Settings** > **Domains**
3. Add your custom domain
4. Update DNS records as instructed by Vercel

## Troubleshooting

### Build Fails

**Issue**: Build fails with module not found errors

**Solution**:
- Check that `docusaurus_textbook/package.json` has all required dependencies
- Verify the build command in `vercel.json` is correct
- Check build logs in Vercel dashboard for specific errors

### API Functions Timeout

**Issue**: API requests timeout or fail

**Possible causes**:
1. **Missing environment variables**: Verify all required env vars are set
2. **Cold start**: First request may be slower (30s timeout for free tier)
3. **Dependencies too large**: Vercel has a 50MB limit for serverless functions

**Solutions**:
- Use Vercel Pro for longer timeouts (300s)
- Optimize dependencies in `api/requirements.txt`
- Consider using edge functions for faster cold starts

### CORS Errors

**Issue**: Browser shows CORS errors when calling API

**Solution**:
- The API endpoints already include CORS headers (`Access-Control-Allow-Origin: *`)
- If issues persist, check browser console for specific CORS errors
- Verify the API URL in ChatWidget.js is correct

### Qdrant Connection Issues

**Issue**: API returns errors about Qdrant connection

**Solutions**:
1. Verify Qdrant URL and API key are correct
2. Check that your Qdrant cluster is running and accessible
3. Ensure Qdrant collection is created and populated with embeddings
4. Check Qdrant dashboard for connection logs

### Environment Variables Not Working

**Issue**: API can't access environment variables

**Solutions**:
1. Verify env vars are added in Vercel Dashboard
2. Redeploy after adding environment variables:
   ```bash
   vercel --prod
   ```
3. Check that variable names match exactly (case-sensitive)
4. Ensure variables are added for the correct environment (Production/Preview/Development)

## Performance Considerations

### Cold Starts
- Serverless functions may have cold starts (2-5 seconds)
- First request after inactivity will be slower
- Consider Vercel Pro for faster cold starts

### Function Size
- Keep `api/requirements.txt` minimal
- Vercel has a 50MB limit for serverless functions
- Large ML libraries may exceed this limit

### Caching
- Vercel automatically caches static assets
- API responses are not cached by default
- Consider implementing response caching if needed

## Cost Estimation

### Vercel Free Tier
- 100GB bandwidth per month
- Unlimited static hosting
- 100 hours serverless function execution
- Typically sufficient for moderate usage

### Vercel Pro ($20/month)
- 1TB bandwidth
- Unlimited serverless function execution
- Better cold start performance
- Team collaboration features

### External Services
- **Cohere**: Pay-per-use for embeddings and generation
- **Qdrant**: Free tier or cloud pricing based on usage

## Monitoring

1. **Vercel Analytics**:
   - Go to your project > **Analytics**
   - View deployment stats, traffic, and performance

2. **Function Logs**:
   - Go to your project > **Deployments** > Select deployment
   - Click **Functions** to view logs
   - Filter by function name and time range

3. **Error Tracking**:
   - Monitor error rates in Analytics
   - Check function logs for detailed error messages
   - Set up Vercel Notifications for deployment failures

## Updating Deployment

### Automatic Deployments (Recommended)
- Push changes to your Git repository
- Vercel automatically builds and deploys
- Preview deployments for pull requests
- Production deployment on merge to main branch

### Manual Deployments
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

## Rollback

If a deployment has issues:

1. Go to Vercel Dashboard > **Deployments**
2. Find a previous working deployment
3. Click **⋯** > **Promote to Production**

Or via CLI:
```bash
vercel rollback
```

## Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Monitor API usage** to detect unusual activity
5. **Set up rate limiting** if needed (Vercel Pro feature)

## Support

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Community**: https://github.com/vercel/vercel/discussions
- **Cohere Documentation**: https://docs.cohere.com
- **Qdrant Documentation**: https://qdrant.tech/documentation

## Next Steps

After successful deployment:

1. Test all functionality:
   - Health check: `/api/health`
   - Chat widget on homepage
   - Different types of queries

2. Set up custom domain (optional)

3. Configure analytics and monitoring

4. Set up automatic deployments from Git

5. Share your deployed URL: `https://your-project.vercel.app`
