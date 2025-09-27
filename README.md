# 🚀 Asterix - An Asteroid Visualisation Tool

Asterix is a comprehensive web application that allows you to simulate real or fictional asteroids and their impacts on Earth. It features an interactive 3D visualization, real-time asteroid tracking, and an engaging game mode to protect Earth from cosmic threats.

## ✨ Features

### 🌍 3D Visualization

- Interactive 3D Earth
- Real-time asteroid tracking and positioning
- Historical asteroid data from NASA APIs
- Real-world asteroid case studies

### 🎮 Simulation Mode

- Create fictional asteroids with custom parameters
- Impact visualization (craters, fires, effects)
- Data and time sliders for simulation control
- Save and share simulations

### 🛡️ Game Mode

- Single-player defense game
- Multiple difficulty levels
- Various defense mechanisms:
  - Gravity tractors
  - Energy shields
  - Kinetic impactors
- Score system and leaderboards
- Sound effects and visual effects

### 👤 User Features

- User accounts and authentication
- Save simulations and game progress
- Global leaderboards
- Personal statistics

## 🛠️ Technologies

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Cesium.js
- **Backend**: FastAPI (Python), SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **Cache**: Redis
- **Deployment**: Docker & Docker Compose
- **APIs**: NASA NEO Data

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone and Setup

```bash
git clone https://github.com/arthurwhennig/Asterix.git
cd Asterix
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment

```bash
cp env.example .env
# Edit .env with your NASA API key and other settings
```

### 3. Run with Docker

```bash
cd deployment
docker-compose up -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
Asterix/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   └── components/      # React components
│   ├── public/              # Static assets
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── api/                 # API routes
│   ├── database/            # Database models
│   ├── alembic/             # Database migrations
│   └── main.py
├── database/                # Database scripts
├── deployment/              # Docker configurations
│   ├── docker-compose.yml
│   └── init.sql
├── docs/                    # Documentation
└── setup.sh                # Setup script
```

## 🔧 Development

### Backend Development

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 📊 API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Asteroids

- `GET /api/asteroids/` - Get asteroid data
- `GET /api/asteroids/{id}` - Get specific asteroid
- `POST /api/asteroids/sync-nasa` - Sync with NASA data
- `POST /api/asteroids/` - Create fictional asteroid

### Game

- `POST /api/game/score` - Submit game score
- `GET /api/game/scores` - Get user scores
- `GET /api/game/leaderboard` - Get leaderboard
- `GET /api/game/stats` - Get user statistics

### Simulations

- `POST /api/simulations/` - Create simulation
- `GET /api/simulations/` - Get simulations
- `GET /api/simulations/{id}` - Get specific simulation
- `PUT /api/simulations/{id}` - Update simulation
- `DELETE /api/simulations/{id}` - Delete simulation

## 🗄️ Database Schema

- **users** - User accounts and authentication
- **asteroids** - Asteroid data (real and fictional)
- **game_scores** - Game scores and statistics
- **simulations** - User-created simulations

## 🐳 Docker Services

- **postgres** - PostgreSQL database (port 5432)
- **redis** - Redis cache (port 6379)
- **backend** - FastAPI application (port 8000)
- **frontend** - Next.js application (port 3000)

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Project Documentation](docs/README.md) - Detailed project docs
- [NASA API](https://api.nasa.gov/) - NASA asteroid data API

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NASA for providing asteroid data APIs
- Cesium.js for 3D Earth visualization
- The open-source community for amazing tools and libraries

---

**Ready to explore the cosmos?** 🚀 Start the application and begin your journey into asteroid visualization and Earth defense!
