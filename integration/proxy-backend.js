const express = require('express');
const cors = require('cors');
const axios = require('axios');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// OpenDeepSearch API URL
const ODS_API_URL = process.env.ODS_API_URL || 'http://localhost:8000';

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', service: 'prd-generator-proxy' });
});

// Deep research proxy endpoint - now exclusively for PRD generation
app.post('/api/deep-research', async (req, res) => {
  try {
    const { query } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }
    
    // Call the PRD generation endpoint
    const response = await axios.post(`${ODS_API_URL}/api/deep-research`, {
      query,
      max_sources: 3,
      pro_mode: true
    });
    
    // Return the result from OpenDeepSearch
    return res.json({
      result: response.data.result,
      sources: response.data.sources || []
    });
  } catch (error) {
    console.error('Error calling OpenDeepSearch PRD Generator:', error);
    
    // Check if it's an API error with a response
    if (error.response) {
      return res.status(error.response.status).json({
        error: `Error from PRD Generator: ${error.response.data.detail || 'Unknown error'}`
      });
    }
    
    // Generic error
    return res.status(500).json({
      error: 'Failed to generate PRD'
    });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`PRD Generator proxy listening on port ${PORT}`);
}); 