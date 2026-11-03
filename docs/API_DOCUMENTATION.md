# CivicLens REST API Documentation

Base URL: `/api/v1/`
Swagger Interactive Explorer: `/api/docs/`
OpenAPI 3.0 Schema: `/api/schema/`

## Authentication

- `POST /api/v1/auth/login/`: Obtain JWT access and refresh token pair.
- `POST /api/v1/auth/register/`: Register a new researcher account.
- `POST /api/v1/auth/token/refresh/`: Refresh expired access token.
- `POST /api/v1/auth/logout/`: Blacklist current refresh token.
- `GET  /api/v1/auth/profile/`: Retrieve current authenticated profile.
- `PATCH /api/v1/auth/profile/`: Update profile details.

## Constituencies & Geography

- `GET /api/v1/states/`: List states with district and constituency counts.
- `GET /api/v1/districts/`: List districts with parent state filtering.
- `GET /api/v1/constituencies/`: Paginated constituencies list with search & district filter.
- `GET /api/v1/constituencies/{id}/`: Detailed constituency profile with boundaries.

## Elections & Results

- `GET /api/v1/elections/`: Historical election cycles with winner and margin calculations.
- `GET /api/v1/elections/{id}/`: Detailed election returns and candidate positions.
- `GET /api/v1/elections/turnout/`: Average turnout percentage and polled votes by year.
- `GET /api/v1/elections/winning-margins/`: Top victory margins by election cycle.
- `GET /api/v1/elections/parties/`: Registered political parties.

## Demographic Indicators

- `GET /api/v1/demographics/`: Paginated demographic records filtered by category and region.
- `GET /api/v1/demographics/indicators/`: Distinct catalog of available indicator names.
- `GET /api/v1/demographics/trends/`: Aggregated time-series trend of indicators.

## Analytics Engine

- `GET  /api/v1/analytics/dashboard/`: Statewide overview KPIs, turnout trends, and seat shares.
- `GET  /api/v1/analytics/constituency/{id}/`: Comprehensive historical elections and indicators for a single constituency.
- `POST /api/v1/analytics/compare/`: Side-by-side comparative matrices for multiple constituencies.
- `GET  /api/v1/analytics/party-performance/`: Vote share and seat tallies across party lines.

## Public Issue Intelligence

- `GET /api/v1/intelligence/articles/`: Monitored regional news articles with sentiment tags.
- `GET /api/v1/intelligence/trends/`: Topic volume density and tone distribution.
- `GET /api/v1/intelligence/categories/`: Available civic category topics.

## Datasets & Reports

- `GET  /api/v1/datasets/`: Registry of ingested datasets and validation status.
- `POST /api/v1/datasets/upload/`: Ingest CSV/XLSX file with immediate transactional validation.
- `GET  /api/v1/datasets/{id}/preview/`: Inspect first 10 rows of raw dataset.
- `POST /api/v1/reports/generate/`: Compile PDF, XLSX, or CSV analytical report.
- `GET  /api/v1/reports/{id}/download/`: Download compiled file attachment.

