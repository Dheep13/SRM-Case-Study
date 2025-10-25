# GenAI Learning Assistant - React Frontend

Professional React frontend for the GenAI Learning Assistant.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Start Backend API
In the parent directory:
```bash
python api.py
```

API will be available at `http://localhost:8000`

## Features

- 🏠 **Home Dashboard** - Overview and quick stats
- 💬 **Chat Interface** - Agentic RAG-powered chatbot
- 🔍 **Resource Discovery** - AI agents find learning materials
- 📊 **Analytics** - Skill trends and recommendations
- 📈 **Visualizations** - Interactive charts and graphs

## Tech Stack

- React 18+ with Vite
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Recharts for data visualization
- React Icons for UI icons

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API service layer
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── public/              # Static assets
└── package.json         # Dependencies
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`

Endpoints:
- `POST /api/chat` - Chat with AI
- `POST /api/discover` - Discover resources
- `GET /api/skills` - Get skills
- `GET /api/analytics` - Get analytics
- `POST /api/charts/generate` - Generate charts

## Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## Environment

Create `.env` file:
```
VITE_API_URL=http://localhost:8000
```

Default is already set to localhost:8000 in the code.



