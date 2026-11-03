<div align="center">

# 🏛️ CivicLens
### Full-Stack Political, Electoral & Demographic Intelligence Platform

[![Build Status](https://img.shields.io/badge/CI-Passing-emerald?style=for-the-badge&logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-darkgreen?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-cyan?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](docker-compose.yml)
[![Coverage](https://img.shields.io/badge/Tests-100%25_Passing-success?style=for-the-badge)](docs/TESTING.md)

<p align="center">
  <b>A modern, production-grade intelligence suite transforming fragmented open government election gazettes and census records into an interactive, multi-dimensional analytical environment.</b>
</p>

[✨ Live Features](#-key-features) •
[🏛️ System Architecture](#️-system-architecture) •
[⚡ Quickstart](#-quickstart-guide) •
[📊 API Documentation](#-api-endpoints--swagger) •
[🐳 Docker Setup](#-docker-compose-deployment) •
[🛡️ Ethical Boundaries](#-ethical-data-mandate)

---

</div>

## 📌 Executive Overview

**CivicLens** is an open-access intelligence platform for researchers, public administrators, policy think tanks, and investigative journalists. Focusing initially on **Haryana, India** (with extensible multi-state architecture), the platform aggregates verified constituency records, historical Vidhan Sabha assembly returns, socioeconomic indices, and public interest issues.

> [!IMPORTANT]
> **Ethical Research Guarantee:** CivicLens strictly processes aggregate, publicly released election commission returns and statistical surveys. The platform **does not collect, track, profile, or predict individual voter behavior or private voter identities.**

---

## ✨ Key Features

<table>
  <tr>
    <td width="50%">
      <h3>🗺️ Constituency Explorer & Geo-Intelligence</h3>
      <ul>
        <li>Interactive OpenStreetMap interface powered by <b>React Leaflet</b>.</li>
        <li>Pinpoint assembly constituencies with live GPS coordinates.</li>
        <li>Filter by district, reservation category (<code>GEN</code>/<code>SC</code>/<code>ST</code>), and constituency code.</li>
        <li>Detailed constituency profile view with boundary references.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🗳️ Historical Election Analytics</h3>
      <ul>
        <li>Candidate vote shares, runner-up margins, and ranking positions.</li>
        <li>Turnout trend analysis ($Turnout = \frac{Polled}{Electors} \times 100$).</li>
        <li>Statewide seat shares and vote distribution charts via <b>Recharts</b>.</li>
        <li>Longitudinal analysis comparing multiple assembly cycles.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>👥 Demographic & Socioeconomic Analytics</h3>
      <ul>
        <li>Indicator catalog across Literacy, Population, Healthcare, Workforce, and Infrastructure.</li>
        <li>Explicit data traceability: source citation, reference year, and measurement unit.</li>
        <li>Time-series trend calculation and regional standard deviation analytics.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>⚖️ Side-by-Side Constituency Comparison</h3>
      <ul>
        <li>Multi-constituency comparative dossier builder.</li>
        <li>Side-by-side electoral performance and victory margin divergences.</li>
        <li>Comparative bar graphs for quick civic indicator benchmarking.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>📰 Public Issue & Civic Intelligence</h3>
      <ul>
        <li>Public interest tracking across 8 key sectors: Healthcare, Education, Infrastructure, Agriculture, etc.</li>
        <li>Descriptive text sentiment tone classification (<code>Positive</code>, <code>Neutral</code>, <code>Concern</code>).</li>
        <li>District keyword extraction and geographic issue heatmaps.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>📁 Dataset Pipelines & Report Exports</h3>
      <ul>
        <li>Dynamic downloadable PDF dossiers formatted with <b>ReportLab</b>.</li>
        <li>Multi-sheet Excel exports (<code>.xlsx</code>) using <b>openpyxl</b> and filtered CSVs.</li>
        <li>Transactional CSV/Excel/JSON upload parser with preview inspector.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🏛️ System Architecture

```mermaid
graph TD
    Client([Analyst / Researcher / Admin]) -->|HTTPS / JWT| ReactApp[React 18 + Vite + Tailwind CSS]
    ReactApp -->|REST API v1| DRF[Django REST Framework]

    subgraph Django Core Services
        DRF --> AuthModule[apps.accounts: RBAC & JWT]
        DRF --> GeoModule[apps.constituencies: ACs, Dist & GeoJSON]
        DRF --> ElectionModule[apps.elections: Results & Margins]
        DRF --> DemoModule[apps.demographics: Indicators & Census]
        DRF --> AnalyticsModule[apps.analytics: Aggregations & Matrices]
        DRF --> IntelligenceModule[apps.intelligence: Public Issues & NLP]
        DRF --> DatasetsModule[apps.datasets: Ingestion & Validation]
        DRF --> ReportsModule[apps.reports: ReportLab & Excel]
        DRF --> AuditModule[apps.audit: Immutable Activity Logs]
    end

    Django Core Services --> PostgreSQL[(PostgreSQL Database)]
    Django Core Services --> Redis[(Redis Queue & Cache)]
    Redis --> CeleryWorker[Celery Asynchronous Workers]
```

---

## 🔑 Pre-Seeded Demonstration Accounts

The platform comes pre-configured with realistic, aggregate demonstration records for immediate hands-on exploration:

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **👑 Chief Administrator** | `admin` | `Admin@12345` | Full system control, user management, audit trails, dataset approval |
| **🔬 Research Analyst** | `analyst` | `Analyst@12345` | Dataset uploads, custom report generation, advanced comparative analytics |

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- **Python 3.12+** or **Python 3.13**
- **Node.js 18+** or **Node.js 22**
- **npm** or **pnpm**

---

### 2. Backend Setup
```bash
# 1. Create and activate virtual environment
py -3.13 -m venv backend/venv
# Windows:
backend\venv\Scripts\activate
# Linux/macOS:
source backend/venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Apply database migrations
python backend/manage.py migrate

# 4. Seed demonstration dataset (24 ACs, 48 Elections, 384 Indicators)
python backend/manage.py seed_demo_data

# 5. Start development API server
python backend/manage.py runserver 8000
```
> Backend API will be active at: `http://localhost:8000/api/v1/`  
> Interactive Swagger API Docs: `http://localhost:8000/api/docs/`

---

### 3. Frontend Setup
```bash
# In a new terminal:
cd frontend

# 1. Install frontend packages
npm install

# 2. Start Vite development server
npm run dev
```
> Open your browser and navigate to: **`http://localhost:3000/`**  
> Sign in using: `admin` / `Admin@12345`

---

## 🐳 Docker Compose Deployment

Launch the complete stack in isolated containers (PostgreSQL + Redis + Django Backend + Celery Worker + Nginx Frontend):

```bash
# 1. Clone repository
git clone https://github.com/Radioactive009/CivicLens.git
cd CivicLens

# 2. Build and start containers in detached mode
docker compose up --build -d

# 3. Check health and service status
docker compose ps
```

| Service | Port | Endpoint URL | Description |
| :--- | :--- | :--- | :--- |
| **Frontend** | `80` | `http://localhost/` | Nginx-served optimized React dashboard |
| **Backend REST API** | `8000` | `http://localhost:8000/api/v1/` | Django REST Framework API layer |
| **Swagger UI** | `8000` | `http://localhost:8000/api/docs/` | Interactive OpenAPI documentation |
| **PostgreSQL** | `5432` | `localhost:5432` | Primary relational database |
| **Redis** | `6379` | `localhost:6379` | Message broker & cache |

---

## 📊 API Endpoints & Swagger

CivicLens provides complete, self-documenting REST APIs versioned under `/api/v1/`:

<details>
<summary><b>🔍 Click to view primary API endpoints</b></summary>

<br>

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login/` | Obtain JWT token pair (access + refresh) |
| `POST` | `/api/v1/auth/register/` | Register new researcher/analyst profile |
| `GET` | `/api/v1/constituencies/` | Paginated constituency list with search & district filter |
| `GET` | `/api/v1/constituencies/{id}/` | Detailed constituency view with boundaries |
| `GET` | `/api/v1/elections/` | Historical election results, turnout & winners |
| `GET` | `/api/v1/elections/turnout/` | Longitudinal voter participation metrics |
| `GET` | `/api/v1/elections/winning-margins/` | Ranked victory margins between winner and runner-up |
| `GET` | `/api/v1/demographics/` | Filterable socioeconomic and demographic indicators |
| `GET` | `/api/v1/analytics/dashboard/` | Dynamic KPI summary and statewide metrics |
| `POST` | `/api/v1/analytics/compare/` | Multi-constituency comparative analytical payload |
| `GET` | `/api/v1/intelligence/articles/` | Monitored public issues tagged with sentiment |
| `GET` | `/api/v1/intelligence/trends/` | Sector topic volumes and editorial tone breakdown |
| `POST` | `/api/v1/datasets/upload/` | Multipart file upload and automatic transactional parser |
| `POST` | `/api/v1/reports/generate/` | Compile downloadable PDF, XLSX, or CSV analytical reports |
| `GET` | `/api/v1/reports/{id}/download/` | Download generated file attachment |

</details>

---

## 🧪 Automated Testing Suite

CivicLens enforces high automated test standards across both frontend and backend layers:

```bash
# Run all backend unit, integration, and API tests
backend\venv\Scripts\python.exe -m pytest -v
```
```
backend/tests/test_api.py::test_user_login PASSED
backend/tests/test_api.py::test_user_registration PASSED
backend/tests/test_api.py::test_constituencies_api PASSED
backend/tests/test_api.py::test_dashboard_analytics_api PASSED
backend/tests/test_api.py::test_constituency_comparison_api PASSED
backend/tests/test_api.py::test_demographics_api PASSED
backend/tests/test_api.py::test_elections_turnout_api PASSED
backend/tests/test_api.py::test_news_intelligence_api PASSED
backend/tests/test_api.py::test_news_trends_api PASSED

============================== 9 passed in 41.35s ==============================
```

```bash
# Run frontend Vitest component tests
cd frontend
npx vitest run
```

---

## 📁 Repository Structure

```
CivicLens/
├── .github/workflows/       # GitHub Actions automated CI/CD pipeline
├── backend/
│   ├── apps/
│   │   ├── accounts/        # User authentication, RBAC, SimpleJWT
│   │   ├── constituencies/  # Assembly & Parliamentary geographical models
│   │   ├── elections/       # Results, candidates, parties, turnout
│   │   ├── demographics/    # Census & Directorate indicators
│   │   ├── analytics/       # Comparative matrices, aggregations
│   │   ├── datasets/        # File ingestion pipeline (CSV/XLSX/JSON)
│   │   ├── intelligence/    # Civic issue tracking, NLP tone analysis
│   │   ├── reports/         # ReportLab PDF & openpyxl Excel generators
│   │   └── audit/           # Immutable administrative audit logging
│   ├── config/              # Django settings, Celery, URLs
│   ├── tests/               # Pytest automated API suite
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # UI widgets and navigation cards
│   │   ├── pages/           # 10 comprehensive dashboard views
│   │   ├── layouts/         # Responsive SaaS dashboard sidebar layout
│   │   ├── services/        # Axios interceptors & API client
│   │   ├── store/           # Zustand state management
│   │   └── test/            # Vitest suite
│   ├── package.json
│   └── vite.config.js
├── docker/                  # Dockerfiles and Nginx reverse proxy configuration
├── docs/                    # In-depth architectural & operational guides
├── docker-compose.yml       # Complete multi-container orchestration
├── .env.example             # Documented environment variables
└── README.md
```

---

## 🛡️ Ethical Data Mandate

CivicLens was created under the fundamental principle that data science should empower civic transparency and research, not undermine privacy:

- **Strictly Aggregate Records:** Every indicator is normalized to regional boundaries (constituency, district, state).
- **Zero Voter Tracking:** No individual voter registers, electoral roll identities, or personal profiles are collected.
- **Descriptive Tone Only:** Article tone categorizations depict journalistic editorial voice, not public opinion polling.

---

## 📜 Documentation Links

- [System Architecture Specification](docs/ARCHITECTURE.md)
- [Database Entity-Relationship Schema](docs/DATABASE_SCHEMA.md)
- [REST API Reference](docs/API_DOCUMENTATION.md)
- [Data Ingestion Pipeline Documentation](docs/DATA_INGESTION.md)
- [Data Sources & Open Government Licensing](docs/DATA_SOURCES.md)
- [Production Deployment Guide](docs/DEPLOYMENT.md)
- [Quality Assurance & Testing Manual](docs/TESTING.md)
- [Security & Governance Policy](docs/SECURITY.md)

---

<div align="center">
  <b>Built for Public-Interest Research, Civic Policy Insights & Demographic Transparency.</b>
</div>
