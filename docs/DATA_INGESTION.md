# CivicLens Data Ingestion Pipeline

CivicLens provides an automated ingestion engine for processing electoral, demographic, and geographical datasets into structured relational database schemas.

## Ingestion Architecture

```
Uploaded File (CSV / XLSX / JSON)
        │
        ▼
Validation Guard (Type, Size, Format)
        │
        ▼
Pandas Normalization & Column Inspection
        │
        ├── Type: ELECTIONS ──────► ECI Returns Parser ──► Transactional Upsert (cl_elections, cl_election_results)
        ├── Type: DEMOGRAPHICS ───► Indicators Parser ───► Transactional Upsert (cl_demographic_indicators)
        └── Type: CONSTITUENCIES ─► Boundary Parser ─────► Transactional Upsert (cl_states, cl_districts, cl_constituencies)
        │
        ▼
DatasetImportJob Logging (Successful Rows, Failed Rows, Error Logs)
```

## Sample CSV Templates

### 1. Elections CSV (`elections_template.csv`)
```csv
constituency_code,election_year,election_type,candidate_name,party_name,party_abbreviation,votes_received,position,total_valid_votes,total_votes_polled,total_electors
HR-AC-01,2024,VIDHAN_SABHA,Candidate Name,Bharatiya Janata Party,BJP,58420,1,135000,135000,185000
HR-AC-01,2024,VIDHAN_SABHA,Opponent Name,Indian National Congress,INC,52310,2,135000,135000,185000
```

### 2. Demographics CSV (`demographics_template.csv`)
```csv
name,category,region_type,region_identifier,region_name,value,unit,reference_year
Total Population,DEMOGRAPHICS,CONSTITUENCY,HR-AC-01,Kalka,215000,Count,2024
Literacy Rate,LITERACY,CONSTITUENCY,HR-AC-01,Kalka,82.4,%,2024
Primary Health Centres,HEALTHCARE,CONSTITUENCY,HR-AC-01,Kalka,8,Count,2024
```

