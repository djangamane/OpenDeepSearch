# OpenDeepSearch PRD Generator Integration Guide

This guide explains how to integrate the OpenDeepSearch PRD Generator into your existing web application.

## Architecture Overview

The integration follows a microservice architecture with the following components:

1. **OpenDeepSearch PRD API** - A FastAPI-based service that exposes PRD generation functionality
2. **Proxy Backend** - A Node.js Express server that forwards requests from your website to the OpenDeepSearch API
3. **Web Frontend** - Your existing website with modifications to the deep-research-tool.html page

This architecture allows for:
- Separation of concerns between your main website and the PRD generation functionality
- Independent scaling of the OpenDeepSearch service based on demand
- Easy maintenance and updates of the PRD generation functionality

## Prerequisites

- Docker and Docker Compose installed on your server
- API keys for the required services:
  - A search provider (Serper.dev or SearXNG)
  - An LLM provider via LiteLLM (OpenAI, Anthropic, Google, etc.)
  - A reranker (Jina AI recommended for simplicity)

## Setup Instructions

### 1. Clone and Prepare the Repository

```bash
# Clone OpenDeepSearch
git clone https://github.com/djangamane/OpenDeepSearch.git
cd OpenDeepSearch

# Copy our integration files to the main directory
cp -r integration/* .

# Make sure integration files are executable
chmod +x setup.sh
```

### 2. Configure Environment Variables

Create environment files for both services:

```bash
# For OpenDeepSearch API
cp .env.example.microservice .env

# For Proxy Backend
cp .env.example.proxy .env.proxy
```

Edit these files to include your API keys and configuration.

### 3. Build and Start the Services

```bash
# Build and start all services
docker-compose up -d

# Check that services are running
docker-compose ps
```

### 4. Test the Integration

Test the proxy backend:

```bash
# Make a test request to the proxy backend
curl -X POST -H "Content-Type: application/json" -d '{"query":"A social media app for pet owners"}' http://localhost:3000/api/deep-research
```

### 5. Integrate with Your Website

There are two options for integrating with your website:

#### Option A: Update Your Existing Backend

If you already have a backend proxy at `/api/deep-research`:

1. Modify your existing backend code to forward requests to the OpenDeepSearch proxy:

```javascript
// Example in Node.js/Express
app.post('/api/deep-research', async (req, res) => {
  try {
    const { query } = req.body;
    
    // Forward to the OpenDeepSearch proxy
    const response = await axios.post('http://localhost:3000/api/deep-research', {
      query
    });
    
    return res.json(response.data);
  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: 'Failed to generate PRD' });
  }
});
```

#### Option B: Direct Integration

If you don't have an existing backend or prefer to connect directly:

1. Update your frontend to point to the new proxy endpoint:

```javascript
// In your deep-research-tool.html JavaScript
// Change the fetch URL to point to the proxy backend
const response = await fetch('http://localhost:3000/api/deep-research', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: query
  })
});
```

2. Make sure CORS is properly configured if your frontend is on a different domain.

## Frontend Integration Example

We've provided an example HTML file (`deep-research-tool-example.html`) that demonstrates how to integrate with the OpenDeepSearch PRD Generator. Key features:

- Chat-like interface for PRD generation
- Example project ideas to help users get started
- Copy button for easy PRD sharing
- Loading indicators during processing

You can use this as a reference or starting point for updating your existing `deep-research-tool.html` page.

## Deployment to Render.com (Recommended)

For deploying to Render.com:

1. Create a Render account if you don't have one
2. Create a new Web Service, pointing to your GitHub repository
3. Choose the "Docker" runtime
4. Configure environment variables from `.env.example.microservice`
5. Deploy the service

## Production Deployment Considerations

For production deployment, consider the following:

1. **Security**:
   - Set up proper API authentication between services
   - Restrict CORS to only your domain in the proxy backend
   - Use HTTPS for all communications

2. **Scaling**:
   - Deploy the OpenDeepSearch API on machines with good CPU/RAM for ML workloads
   - Consider using Kubernetes for better scaling and management

3. **Monitoring**:
   - Add logging and monitoring to track usage and detect issues
   - Set up alerts for service failures

4. **Cost Management**:
   - Monitor API usage to control costs from external services
   - Consider caching common queries to reduce API calls

## Self-hosting Options

For more control and potentially lower costs, consider self-hosting:

1. **SearXNG** instead of Serper.dev for web search
2. **Infinity Embeddings** with open-source models instead of Jina AI for reranking
3. **Local LLMs** via LiteLLM, which supports local model deployment

See the OpenDeepSearch documentation for details on setting up these self-hosted options.

## Troubleshooting

Common issues and solutions:

- **Connection refused errors**: Check that the services are running and ports are correctly exposed
- **API key errors**: Verify your environment variables are set correctly
- **Slow responses**: Adjust max_sources and pro_mode parameters for better performance
- **Memory issues**: Increase the container memory limits in docker-compose.yml

## Additional Resources

- [OpenDeepSearch Documentation](https://github.com/sentient-agi/OpenDeepSearch)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LiteLLM Documentation](https://docs.litellm.ai/docs/) 