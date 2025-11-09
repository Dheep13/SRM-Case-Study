import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8080;

// Get API URL from environment or use default
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

// Serve static files from dist directory
app.use(express.static(join(__dirname, 'dist')));

// Inject environment variables into index.html
app.get('*', (req, res) => {
  try {
    const indexPath = join(__dirname, 'dist', 'index.html');
    let html = readFileSync(indexPath, 'utf8');
    
    // Inject environment variables by adding a script tag before </head>
    const envScript = `
    <script>
      window.ENV = window.ENV || {};
      window.ENV.API_BASE_URL = '${API_BASE_URL}';
      console.log('API_BASE_URL injected:', window.ENV.API_BASE_URL);
    </script>
    `;
    
    html = html.replace('</head>', `${envScript}</head>`);
    
    res.send(html);
  } catch (error) {
    console.error('Error loading application:', error);
    res.status(500).send('Error loading application');
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API Base URL: ${API_BASE_URL}`);
});

