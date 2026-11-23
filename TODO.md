# VitalX — TODO & Improvement Roadmap

A roadmap for evolving VitalX from a personal health dashboard into a solid, maintainable data engineering project. Organised from "quick wins" to longer-term architectural work. No code has been changed — this is purely a reading-based recommendation list.

---

## For Cline to solve

- need a visual to show days app has been used - there's a .sql file and function in service layer -
- need a visual to show total calories burnt - .sql file for it -

## 1. Data Quality & Schema (Foundation)

These are the highest-impact changes for a data engineer. They protect your data integrity as the project grows.

### Add Primary Keys & Constraints
- [ ] Add a surrogate `id SERIAL PRIMARY KEY` to `vitalx_walk`, `vitalx_sleep`, and `vitalx_streak` tables (the `weather` table already has this pattern).
- [ ] Add `UNIQUE (todays_date)` constraint on `vitalx_walk` and `vitalx_sleep` to prevent duplicate same-day entries at the database level (currently only enforced in application logic).
- [ ] Add `NOT NULL` constraints where missing and `CHECK` constraints for business rules (e.g., `steps_walked > 0`, `hours_slept >= 0`).

### Fix Count Logic
- [ ] `get_total_days_walked()` currently does `count(*)` which counts rows, not distinct dates. If duplicates ever slip through, this will overcount. Change to `count(distinct todays_date::date)`.
- [ ] `get_total_days_slept()` has the same issue — use `count(distinct todays_date::date)`.

### Centralise "Days Active" Logic
- [ ] The new `days_active()` function in `app_layer/app.py` duplicates walk/sleep date aggregation logic that belongs in the service layer. Move it into `src/vitalx/service.py` as `get_days_active()` with its own SQL file in `dbo/analytics/`, then call it from the frontend.

## 2. Backend & Data Pipeline

### Weather Pipeline
- [ ] Replace the `while true; do ... sleep 86400; done` loop in the Docker Compose `weather` service with a proper scheduler (cron inside the container, or a separate lightweight scheduler). Infinite loops are hard to monitor and restart.
- [ ] Add a "last successful weather fetch" timestamp to the database so the UI can show data freshness (stale weather vs. current).
- [ ] Add retry with exponential backoff for the Open-Meteo API call (currently uses `retry_requests` which is good, but consider circuit-breaking if the API is down for days).

### Backup Strategy
- [ ] CSV backup uses `if_exists="replace"` which is destructive — consider appending or versioning instead, especially since you keep only 7 days.
- [ ] Add a restore test that runs in CI to verify backups are actually restorable.
- [ ] Move backup logic into the database (pg_cron or similar) once on Raspberry Pi, as noted in the README.

### Configuration
- [ ] Move hardcoded values (latitude/longitude, Skyrim step thresholds, streak 6000-step threshold) into a config file or environment variables instead of being hardcoded in Python.
- [ ] The `.env` file contains `DB_PASSWORD` — confirm it is in `.gitignore` and never committed.

## 3. Testing Strategy

You already have 56 passing tests — great foundation. Here's how to level up:

### Test Coverage
- [ ] Add a `pytest-cov` step to `make test` and aim for 80%+ coverage on the service layer.
- [ ] Add integration tests that spin up a real PostgreSQL container (via `pytest-postgresql` or docker) and test against actual SQL, not just mocks.
- [ ] Add frontend tests for the Dash callbacks (`submit_walk`, `submit_sleep`, `toggle_sleep_quality`) using Dash's testing utilities.

### Test Organisation
- [ ] Rename test directories to be more descriptive: `tests/unit/`, `tests/integration/`, `tests/e2e/`.
- [ ] Add a test for the new `days_active()` function.

## 4. Frontend & UI

### Polishing
- [ ] Add the "Days Active" stat card (already implemented) — consider adding a trend indicator (e.g., "+2 this week").
- [ ] Add a "streak calendar" heatmap showing which days have entries (GitHub contribution graph style).
- [ ] Add client-side form validation feedback that appears before submission (currently validation only happens after clicking submit).
- [ ] Add a "clear form" button after successful submission.

### Accessibility & UX
- [ ] Add `aria-label` attributes to buttons and inputs for screen readers.
- [ ] Ensure colour contrast ratios meet WCAG AA standards (the crimson/black theme can be tricky).
- [ ] Add a "no data" state for charts when there's no history yet (partially done).

## 5. Observability & Operations

### Logging & Monitoring
- [ ] Add structured JSON logging instead of plain text for easier parsing in production.
- [ ] Add log rotation configuration that is visible and documented (currently `RotatingFileHandler` with 3 backups — good, but document it).
- [ ] Add a simple `/health` endpoint to the Dash app that returns database connectivity status.

### Alerting
- [ ] Add basic alerting (email or Slack webhook) if the weather pipeline fails for >24 hours.
- [ ] Add disk space monitoring for the backup/exports folders on the Raspberry Pi.

## 6. Documentation

### Project Docs
- [ ] Add an `ARCHITECTURE.md` with a diagram of the 3-layer architecture (UI → Service → DB) and data flow.
- [ ] Add a `CONTRIBUTING.md` since you mentioned working with an AI agent as your frontend developer — this sets expectations for how changes should be made.
- [ ] Add a `CHANGELOG.md` to track what changed in each version.
- [ ] Document the `.env` required variables in a `.env.example` file (without real secrets).

### Code Docs
- [ ] Add docstrings to the SQL files explaining what each query does and why.
- [ ] Add inline comments to complex logic in `skyrim.py` (the state machine / journey calculation).
- [ ] Document the `prek.toml` pre-commit configuration and what hooks run.

## 7. Data Engineering Growth Goals

Since you're studying to become a data analyst/engineer, here are specific skills you can practice by extending VitalX:

### Data Modeling
- [ ] Build a star/snowflake schema: create `dim_date`, `dim_location`, `fact_walks`, `fact_sleep` tables for analytical queries.
- [ ] Add a `dbt` project to transform raw tables into analytics-ready models.

### Data Validation
- [ ] Add Great Expectations or pandera schemas to validate data at ingestion (e.g., steps must be within a realistic range).
- [ ] Add data quality tests that fail the pipeline if null rates spike.

### Orchestration
- [ ] Replace the Docker loop with Apache Airflow, Prefect, or Dagster for scheduling weather fetches and backups.
- [ ] Add a DAG that runs daily: fetch weather → validate → load → backup → notify.

### Visualisation
- [ ] Add a month-over-month comparison chart (steps this month vs. last month).
- [ ] Add correlation analysis (does more sleep correlate with more steps?).
- [ ] Export a summary dashboard as a PDF/email on the first of each month.

## 8. Quick Wins (Do This Weekend)

If you want immediate progress, start here:

1. [ ] Add `id SERIAL PRIMARY KEY` to all tables.
2. [ ] Add `UNIQUE (todays_date)` to walk and sleep tables.
3. [ ] Move `days_active()` from `app.py` into `service.py` with its own SQL file.
4. [ ] Add `.env.example` with placeholder values.
5. [ ] Add `pytest-cov` and a coverage gate to `make test`.
6. [ ] Fix `get_total_days_walked` and `get_total_days_slept` to count distinct dates.
7. [ ] Add a `CHANGELOG.md` documenting the features you've already built.

---

## How to Use This File

- Pick **one** item per week so you don't get overwhelmed.
- Mark items as `[x]` when completed.
- Add new items as you learn and the project evolves.
- This is a living document — your project is already impressive; this is just about making it more robust as you grow into the data engineering role.

---

**Project status:** Functional dashboard with walk/sleep tracking, streak gamification, weather integration, CSV+PG backups, and 56 passing tests. Running on Docker with a Raspberry Pi deployment planned.

*Generated after end-to-end code review of the VitalX codebase.*