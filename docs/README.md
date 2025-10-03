# Asterix - Asteroid Visualization Tool

Asterix is a web application that allows you to simulate real or fictional asteroids and their impacts on Earth. It also includes a game mode to protect Earth from asteroids.

## Features

- Interactive 3D visualization of Earth using Cesium.js, Three.js, D3.js
- Historical asteroid data from NASA APIs
- Real-time asteroid path tracking
- Simulation mode with build-it-yourself asteroid creation
- Impact visualization (craters, secondary impacts (tsunamis, ...))
- Data and time sliders
- Single-player game mode to protect Earth from asteroids
- Visual effects
- Gravity tractors, shields, and kinetic impactors
- Score system with difficulty levels (cost for each defending mechanism and 1 to  3 star system based on the used costs)
- User accounts for saving game progress and saved built-it-yourself games
- public leaderboard for the game mode (ranked by min cost)
- Error tracking and logging

## Technologies

- **Frontend**: Next.js with TypeScript, Tailwind CSS, Cesium.js
- **Backend**: FastAPI (Python)
- **Database**: Firebase 
- **Cache**: Redis 
- **Deployment**: Docker and Docker Compose
- **Version Control**: GitHub

## Project Structure

```
/Users/ahennig/Desktop/Asterix/
├── frontend/          # frontend setuo
├── backend/           # backend setup
├── database/          # Database schema and migrations
├── deployment/        # Docker and deployment configurations
├── docs/             # Documentation files
└── documentation.txt # Project overview
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.11+ (for local development)

### Environment Setup

1. Copy the environment example file:

   ```bash
   cp env.example .env
   ```

2. Update the `.env` file with your configuration:
   - Set your NASA API key (get one from https://api.nasa.gov/)
   - Update database credentials if needed
   - Set a secure secret key for JWT tokens

### Running with Docker

1. Start all services:

   ```bash
   cd deployment
   docker-compose up -d
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

#### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## API Documentation

The API documentation is available at http://localhost:8000/docs when the backend is running.

### Main Endpoints

- `GET /` - API health check
- `GET /health` - Health check endpoint
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/asteroids/` - Get asteroid data
- `POST /api/asteroids/sync-nasa` - Sync with NASA data
- `GET /api/game/leaderboard` - Get game leaderboard
- `POST /api/simulations/` - Create simulation

## Database Schema

The application uses Firebase with the following main tables:

- `users` - User accounts and authentication
- `asteroids` - Asteroid data (real and fictional)
- `games` - Game scores and statistics
- `simulations` - User-created simulations

## License

This project is licensed under the MIT License.
