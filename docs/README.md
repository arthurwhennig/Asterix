# Asterix - Asteroid Defense Simulation Platform

Asterix is a comprehensive web application that simulates asteroid impacts on Earth and provides defense mechanisms. The platform combines real NASA asteroid data with user-created scenarios for educational and entertainment purposes.

## Core Features

### 3D Visualization Engine
- **Technology Stack**: Cesium.js for Earth rendering, Three.js for 3D objects, D3.js for data visualization
- **Capabilities**: Interactive Earth model with real-time asteroid trajectory tracking
- **Performance**: 60fps rendering with LOD (Level of Detail) optimization

### Data Integration
- **NASA API Integration**: Real-time asteroid data from NASA's Near Earth Object Web Service
- **Data Sources**: Historical impact data, current asteroid tracking, orbital mechanics
- **Update Frequency**: Daily synchronization with NASA databases

### Simulation Modes
- **Defense Mode**: Strategic placement of defense mechanisms (gravity tractors, shields, kinetic impactors)
- **Simulation Mode**: Real-time visualization of asteroid deflection attempts
- **Impact Analysis**: Comprehensive damage assessment including craters, tsunamis, earthquakes

### Game Mechanics
- **Scoring System**: 1-3 star rating based on cost efficiency and impact prevention
- **Cost Management**: Real-world pricing for defense mechanisms
- **Difficulty Levels**: Progressive challenge scaling based on asteroid size and velocity

### User Management
- **Account System**: JWT-based authentication with Firebase backend
- **Progress Tracking**: Save defense configurations and simulation results
- **Leaderboards**: Global rankings based on cost efficiency and success rate

## Technology Architecture

### Frontend Stack
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript with strict type checking
- **Styling**: Tailwind CSS with custom design system
- **3D Engine**: Cesium.js for Earth visualization
- **State Management**: React Context API with useReducer
- **Build Tool**: Vite for optimized bundling

### Backend Stack
- **Framework**: FastAPI with async/await support
- **Language**: Python 3.11+ with type hints
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with refresh mechanism
- **API Documentation**: OpenAPI 3.0 with Swagger UI
- **Testing**: Pytest with coverage reporting

### Infrastructure
- **Database**: PostgreSQL 15+ with connection pooling
- **Cache**: Redis 7+ for session storage and API caching
- **Message Queue**: Redis for background task processing
- **File Storage**: Local filesystem with planned S3 migration
- **Monitoring**: Structured logging with JSON format

## Project Structure

```
Asterix/
├── frontend/                    # Next.js frontend application
│   ├── src/
│   │   ├── app/                # App Router pages and layouts
│   │   ├── components/         # Reusable React components
│   │   ├── lib/                # Utility functions and configurations
│   │   └── types/              # TypeScript type definitions
│   ├── public/                 # Static assets
│   └── package.json           # Frontend dependencies
├── backend/                    # FastAPI backend application
│   ├── api/                   # API route handlers
│   │   └── routes/            # Endpoint implementations
│   ├── database/              # Database models and connections
│   ├── alembic/               # Database migrations
│   ├── main.py               # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
├── deployment/                # Infrastructure configuration
│   ├── docker-compose.yml    # Multi-container orchestration
│   └── init.sql              # Database initialization
├── docs/                     # Project documentation
│   ├── README.md            # Main project documentation
│   ├── api.md               # API endpoint documentation
│   └── deployment.md        # Deployment instructions
└── .env.example             # Environment variables template
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.11+ (for local development)

### Environment Configuration

1. Copy the environment template:
   ```bash
   cp env.example .env
   ```

2. Configure required environment variables in `.env`:
   ```bash
   # NASA API Configuration
   NASA_API_KEY=your_nasa_api_key_here
   NASA_API_BASE_URL=https://api.nasa.gov/neo/rest/v1
   
   # Database Configuration
   DATABASE_URL=postgresql://user:password@localhost:5432/asterix_db
   REDIS_URL=redis://localhost:6379
   
   # Security Configuration
   JWT_SECRET_KEY=your_super_secret_jwt_key_here
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
   
   # Application Configuration
   DEBUG=true
   LOG_LEVEL=INFO
   CORS_ORIGINS=http://localhost:3000
   ```

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

## API Reference

The complete API documentation is available at `http://localhost:8000/docs` when the backend is running.

### Authentication Endpoints
```http
POST /api/auth/register
Content-Type: application/json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}

POST /api/auth/login
Content-Type: application/json
{
  "username": "string",
  "password": "string"
}

POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

### Asteroid Data Endpoints
```http
GET /api/asteroids/
Query Parameters:
  - limit: integer (default: 100)
  - offset: integer (default: 0)
  - min_diameter: float (optional)
  - max_diameter: float (optional)
  - is_hazardous: boolean (optional)

POST /api/asteroids/sync-nasa
Authorization: Bearer <access_token>
Synchronizes local database with NASA asteroid data

GET /api/asteroids/{asteroid_id}
Returns detailed information for a specific asteroid
```

### Game and Simulation Endpoints
```http
GET /api/game/leaderboard
Query Parameters:
  - challenge_id: string (optional)
  - limit: integer (default: 10)

POST /api/simulations/
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "asteroid_id": "string",
  "defense_config": {
    "gravity_tractors": [...],
    "shields": [...],
    "kinetic_impactors": [...]
  }
}

GET /api/simulations/{simulation_id}
Returns simulation results and impact analysis
```

## Database Schema

The application uses PostgreSQL with the following core tables:

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Asteroids Table
```sql
CREATE TABLE asteroids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nasa_id VARCHAR(50) UNIQUE,
    name VARCHAR(255) NOT NULL,
    diameter_km DECIMAL(10,3),
    velocity_km_s DECIMAL(10,3),
    mass_kg DECIMAL(20,3),
    composition VARCHAR(100),
    is_hazardous BOOLEAN DEFAULT FALSE,
    orbital_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Simulations Table
```sql
CREATE TABLE simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    asteroid_id UUID REFERENCES asteroids(id),
    defense_config JSONB NOT NULL,
    total_cost DECIMAL(15,2),
    success BOOLEAN,
    impact_location JSONB,
    damage_assessment JSONB,
    star_rating INTEGER CHECK (star_rating >= 1 AND star_rating <= 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Game Scores Table
```sql
CREATE TABLE game_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    challenge_id VARCHAR(100),
    score INTEGER,
    cost_efficiency DECIMAL(10,2),
    completion_time_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## License

This project is licensed under the MIT License.
