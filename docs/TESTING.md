# CivicLens Automated Testing Documentation

CivicLens enforces high testing standards across both backend API layers and frontend user interface workflows.

## Backend Pytest Suite

Run all backend unit and API integration tests:
```bash
backend\venv\Scripts\python.exe -m pytest -v
```

### Covered Test Cases:
- `test_user_login`: Verifies JWT authentication with valid credentials.
- `test_user_registration`: Tests user signups with secure password policies and role defaults.
- `test_constituencies_api`: Validates constituency retrieval, pagination, and filtering.
- `test_dashboard_analytics_api`: Verifies dynamic KPI calculations, turnout rates, and party shares.
- `test_constituency_comparison_api`: Verifies multi-constituency comparison payload computations.
- `test_demographics_api`: Validates socioeconomic indicators and categories.
- `test_elections_turnout_api`: Validates historical voter participation analytics.
- `test_news_intelligence_api`: Tests news retrieval and topic tags.
- `test_news_trends_api`: Tests topic frequency and tone breakdown endpoints.

---

## Frontend Vitest Suite

Run frontend unit and component tests:
```bash
cd frontend
npx vitest run
```

### Covered Test Cases:
- `LoginPage`: Tests form input rendering, authentication triggers, and demo credential display.
- `SettingsPage`: Validates user profile updates and form interaction.

