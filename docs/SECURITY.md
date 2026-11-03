# CivicLens Security & Privacy Policy

CivicLens is engineered strictly for public-interest research, policy evaluation, and analytical transparency.

## Security Practices

1. **Authentication & Authorization**
   - JWT tokens with HMAC-SHA256 signing via `djangorestframework-simplejwt`.
   - Access token lifetime: 60 minutes. Refresh token lifetime: 7 days.
   - Blacklist support on rotation and explicit logout.
   - Granular RBAC (`ADMIN`, `ANALYST`, `RESEARCHER`, `VIEWER`).

2. **Data Integrity & Protection**
   - Passwords hashed using PBKDF2 with SHA256 iterations.
   - Full SQL injection prevention via Django ORM parametrized queries.
   - Cross-Origin Resource Sharing (CORS) configured with standard headers.
   - File upload validation inspecting MIME types and extensions.
   - Database transactions (`transaction.atomic`) ensuring rollbacks on malformed ingestion rows.

3. **Ethical Boundaries (Non-Negotiable)**
   - **No Voter Profiling:** CivicLens does not ingest or store individual voter registries or personally identifiable voter habits.
   - **No Behavioral Targeting:** The platform does not perform micro-targeting or psychographic profiling.
   - **Descriptive Tone Only:** News sentiment analyses classify article text tone, never claiming to estimate overall public voter opinions.

