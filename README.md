# insurance-management-system-221010-221022

Backend (Django REST Framework) with PostgreSQL.

- Environment variables in `backend/.env.example`. Copy to `backend/.env` and adjust as needed.
- Frontend defaults in `frontend/.env.example` (REACT_APP_API_BASE etc).
- API base path: `/api/`
  - `/api/customers/`
  - `/api/policies/`
  - `/api/claims/`
  - `/api/health/` (healthcheck)
- Swagger UI: `/docs`
- Redoc: `/redoc`
- OpenAPI JSON: `/swagger.json`

### Local Development Setup

1.  **Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Seed Demo Data:**
    To populate the database with sample customers, policies, and claims, run:
    ```bash
    python manage.py seed_demo_data
    ```
    You can add `--reset` to clear existing data before seeding.

CORS and Hosts:
- Configure `CORS_ALLOWED_ORIGINS` to include your UI (e.g., `https://localhost:3000`).
- `DJANGO_ALLOWED_HOSTS` should include `localhost`, `127.0.0.1`, and any preview domains.

Database:
- The backend reads standard `DB_*` env variables and connects to PostgreSQL on `DB_PORT=5001` by default.