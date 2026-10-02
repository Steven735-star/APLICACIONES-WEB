# MD Marketing & Design — Workshop 5

**Authors:** Kevin Erazo and Steven Rodríguez  
**Course:** Web Applications  
**Workshop:** Workshop 5 — REST API, JWT, OpenAPI, and Authentication  
**Semester:** Semester II 2026

## Overview

This repository is an academic, reduced-scope version of the **MD Marketing & Design** backend prepared specifically for Workshop 5.

The complete MD project contains additional modules and infrastructure, but this version isolates only the components needed to demonstrate the workshop phase:

- REST API design.
- Public and protected endpoints.
- JWT authentication.
- Access and refresh tokens.
- Refresh-token rotation and revocation.
- Authenticated-user endpoint.
- Protected CRUD operations.
- OpenAPI schema and Swagger UI.
- PostgreSQL persistence.
- Postman testing.

The project uses **Django 5 + Django REST Framework + PostgreSQL**. The instructor allowed each group to use the architecture that best fits its project, so the existing Django-based architecture is preserved instead of migrating the system to FastAPI only for the workshop.

## Architecture

The Workshop 5 version uses:

- **Django 5** — backend framework.
- **Django REST Framework** — REST API implementation and JSON serialization.
- **SimpleJWT** — JWT access and refresh tokens.
- **PostgreSQL 16** — relational database.
- **drf-spectacular** — OpenAPI schema generation and Swagger UI.
- **Docker Compose** — reproducible local execution.

The full MD system also contains other components, but they are intentionally excluded from this academic version because they are outside the scope of Workshop 5.

## Scope Decisions

### Public user registration is not implemented

MD is designed as an internal organizational system. Users are not expected to create their own accounts. Accounts are created and enabled by an authorized administrator through Django Admin.

This is a deliberate identity-governance decision rather than a technical limitation.

### Google/GitHub social authentication is not implemented

External social authentication is not required for the current business workflow. The system uses administrator-managed institutional accounts, so introducing Google or GitHub login would add an unnecessary external identity provider and a second user-provisioning mechanism.

### Remember Me is not implemented as a separate mode

The system uses a uniform JWT expiration policy for internal users. Access and refresh token lifetimes are configured centrally through environment variables.

### Individual ownership of customers is not implemented

Customers are organizational resources shared by authorized staff, not personal resources owned by the user who created them. The customer CRUD requires authentication. Role-based authorization can be added later if the business process requires it.

## Implemented Endpoints

### Public and system endpoints

```text
GET /api/v1/health/
GET /api/v1/public/info/
```

### Authentication

```text
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/
GET  /api/v1/users/me/
```

### Protected Customer CRUD

```text
POST   /api/v1/crm/clientes/
GET    /api/v1/crm/clientes/
GET    /api/v1/crm/clientes/{id}/
PUT    /api/v1/crm/clientes/{id}/
PATCH  /api/v1/crm/clientes/{id}/
DELETE /api/v1/crm/clientes/{id}/
```

The DELETE operation is implemented as a **soft delete**: the customer is marked inactive instead of being physically removed from the database.

### Documentation

```text
GET /openapi/
GET /docs/
```

### Administration

```text
GET /admin/
```

## Running the Project

Create the environment file:

```bash
cp .env.example .env
```

Start the project:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Verify the API and database connection:

```bash
curl http://localhost:8000/api/v1/health/
```

## Create an Administrator

```bash
docker compose exec web python manage.py createsuperuser
```

The administrator can then manage users through:

```text
http://localhost:8000/admin/
```

## JWT Authentication Flow

### Login

Request:

```http
POST /api/v1/auth/login/
Content-Type: application/json
```

```json
{
  "username": "admin_w5",
  "password": "your-password"
}
```

A successful response contains:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

### Current User

```http
GET /api/v1/users/me/
Authorization: Bearer <access-token>
```

The endpoint returns safe account information and does not expose the password or password hash.

### Refresh

```http
POST /api/v1/auth/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh-token>"
}
```

### Logout

```http
POST /api/v1/auth/logout/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh-token>"
}
```

The refresh token is blacklisted so it cannot be reused.

## Swagger / OpenAPI

Open Swagger UI:

```text
http://localhost:8000/docs/
```

Open the generated OpenAPI schema:

```text
http://localhost:8000/openapi/
```

Swagger is used to inspect the API contract and test public and protected endpoints.

## Postman

The workshop version includes a Postman collection for:

- public endpoint testing;
- successful and unsuccessful login;
- JWT-protected requests;
- `/users/me/`;
- customer CRUD;
- token refresh;
- logout;
- invalid or missing token cases.

Do not include real passwords or complete JWT values in screenshots, reports, or GitHub commits.

## Evidence for the Report

The LaTeX report expects evidence screenshots with the following filenames:

```text
01_project_location.png
02_services_health.png
03_public_endpoint.png
04_admin_user.png
05_login_jwt.png
06_users_me.png
07_crud_without_jwt.png
08_crud_with_jwt.png
09_refresh_logout.png
10_swagger.png
11_postman.png
```

If the image files are not present, `main.tex` displays a placeholder box so the document can still compile while evidence is being collected.

## GitHub Notes

Never commit `.env`.

Commit `.env.example` instead.

Typical first push:

```bash
git init
git add .
git commit -m "Workshop 5 - REST API, JWT, OpenAPI and protected CRUD"
git branch -M main
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```

## Authors

- Kevin Erazo
- Steven Rodríguez
