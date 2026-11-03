# CivicLens Deployment Guide

CivicLens is production-ready for Docker Compose containerization or standalone host deployment.

## Option A: Docker Compose (Production / All-in-One)

1. Clone repository and navigate to root directory:
   ```bash
   cd CivicLens
   ```
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
3. Build and launch all container services:
   ```bash
   docker compose up --build -d
   ```
4. Verify running services:
   ```bash
   docker compose ps
   ```
   Containers initialized:
   - `civiclens_frontend` (Port 80)
   - `civiclens_backend` (Port 8000)
   - `civiclens_db` (Port 5432)
   - `civiclens_redis` (Port 6379)
   - `civiclens_celery` (Worker process)

5. Open application:
   - Frontend: `http://localhost/`
   - Backend APIs: `http://localhost:8000/api/v1/`
   - Interactive Swagger Docs: `http://localhost:8000/api/docs/`

---

## Option B: Local Standalone Development

### Backend Setup
1. Create and activate Python virtual environment:
   ```bash
   py -3.13 -m venv backend/venv
   backend\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run migrations and populate demo seed data:
   ```bash
   python backend/manage.py migrate
   python backend/manage.py seed_demo_data
   ```
4. Start backend server:
   ```bash
   python backend/manage.py runserver 8000
   ```

### Frontend Setup
1. Navigate to `frontend`:
   ```bash
   cd frontend
   npm install
   ```
2. Run development server:
   ```bash
   npm run dev
   ```
3. Access UI at `http://localhost:3000/`

