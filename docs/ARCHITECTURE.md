# CivicLens System Architecture

CivicLens is engineered as a modular full-stack public intelligence platform.

```mermaid
graph TD
    User([Analyst / Researcher / Admin]) -->|HTTPS / REST API| Frontend[React 18 + Vite + Tailwind CSS]
    Frontend -->|JWT Bearer Token| DRF[Django REST Framework / API v1]
    
    subgraph Django Core
        DRF --> Accounts[apps.accounts: Auth & Roles]
        DRF --> Constituencies[apps.constituencies: ACs & Boundaries]
        DRF --> Elections[apps.elections: Results & Turnout]
        DRF --> Demographics[apps.demographics: Indicators]
        DRF --> Analytics[apps.analytics: Matrices & Comparisons]
        DRF --> Datasets[apps.datasets: Ingestion Engine]
        DRF --> Intelligence[apps.intelligence: Public Issues & NLP]
        DRF --> Reports[apps.reports: ReportLab & Excel]
        DRF --> Audit[apps.audit: Immutable Logs]
    end

    Django Core --> ORM[(PostgreSQL Relational DB)]
    Django Core --> Redis[(Redis Queue / Cache)]
    Redis --> CeleryWorker[Celery Background Task Worker]
```

## Modular Responsibilities

1. **`apps.accounts`**: User management with custom user model `User` (`Role.ADMIN`, `Role.ANALYST`, `Role.RESEARCHER`, `Role.VIEWER`), SimpleJWT authentication, and role authorization guards.
2. **`apps.constituencies`**: Multi-tiered geographical models: State (`HR`), Districts (22 Haryana administrative districts), and Vidhan Sabha Constituencies with GPS coordinates and boundary metadata.
3. **`apps.elections`**: Historical election returns, political party registrations (`BJP`, `INC`, `INLD`, `JJP`, `AAP`, `IND`), candidate performance, turnout percentages, and winning margin calculations.
4. **`apps.demographics`**: Census and statistical directorate indicators categorized into literacy, employment, infrastructure, and socioeconomic metrics.
5. **`apps.analytics`**: Aggregated state metrics, multi-constituency comparative matrices, and turnout trends.
6. **`apps.datasets`**: Upload handling for structured CSV, XLSX, and JSON datasets with row validation and rollback protection.
7. **`apps.intelligence`**: Civic topic monitoring, text classification, and journalistic sentiment analysis.
8. **`apps.reports`**: PDF dossier rendering with ReportLab, Excel workbooks with openpyxl, and CSV table generation.
9. **`apps.audit`**: Administrative event and access tracking.

