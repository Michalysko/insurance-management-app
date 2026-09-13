# Insurance App

A deployed full-stack portfolio application for managing insured people, insurance types, and insurance contracts. The project uses a Django REST API backend, a React frontend, token authentication, role-based access, PostgreSQL in production, and bilingual Czech/English UI support.

## Live Demo

- Live application: https://insurance-app-jade-pi.vercel.app
- Backend API: https://insurance-app-api-dx6t.onrender.com/api
- GitHub repository: https://github.com/Michalysko/insurance-management-app

The backend is hosted on a free Render instance, so the first request after a period of inactivity may take a short moment while the service wakes up.

## Demo Access

Administrator account:

```text
Username: demo_admin
Password: superpassword2026
```

Client account:

```text
Username: demo_client
Password: clientpassword2026
```

The administrator can manage insured people, insurance types, and insurance contracts. The client can view only their own profile and their own contracts.

## Project Purpose

This project was built as a practical full-stack portfolio application. It demonstrates how a CRUD system can be structured with a separate REST API, relational data, authentication, role-based permissions, search, pagination, validation, deployment configuration, and a React user interface. The application also includes a small interactive demo assistant that helps visitors understand the administrator and client workflows.

## Features

- Token-based authentication
- Administrator and insured client roles
- CRUD management for insured people
- CRUD management for insurance types
- CRUD management for insurance contracts
- Client profile page
- Client contract overview
- Backend search for insured people by name, address, and phone number
- Search and filtering for insurance contracts
- Pagination for larger datasets
- Czech and English language switcher
- Bilingual insurance type names
- Interactive demo assistant for first-time visitors
- Frontend and backend form validation
- Centralized frontend API client
- Environment-based configuration for local and production environments
- Production deployment with separate frontend, backend, and database services

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Token Authentication
- PostgreSQL in production
- SQLite for local development
- django-cors-headers
- dj-database-url
- WhiteNoise
- Gunicorn

### Frontend

- JavaScript
- React
- React Router
- Vite
- CSS

### Deployment

- Vercel for the React frontend
- Render for the Django backend
- Neon PostgreSQL for the production database

### Development Tools

- Git
- GitHub
- PyCharm
- VS Code

## Project Structure

```text
Insurance App/
├── backend/
│   ├── backend/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── insured/
│   │   ├── management/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── .env.example
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   └── translations.js
│   ├── .env.example
│   ├── package.json
│   ├── vercel.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## Data Model Overview

The application is built around three main domain entities:

- `InsuredPerson` stores personal data about insured clients and can be linked to a Django user account.
- `InsuranceType` stores available insurance categories in Czech and English with a default amount.
- `InsuranceContract` connects an insured person with an insurance type and stores contract-specific data such as subject, amount, contract date, and validity date.

## User Roles

### Administrator

The administrator can:

- create, edit, delete, and search insured people,
- create, edit, and delete insurance types,
- create, edit, delete, and search insurance contracts,
- switch the interface between Czech and English.

### Insured Client

The insured client can:

- view their own profile,
- view their own insurance contracts,
- use the Czech/English language switcher.

## API Endpoints

Main API routes:

```text
POST /api/login/
GET  /api/me/
GET  /api/my-profile/
GET  /api/my-contracts/

/api/insured-people/
/api/insurance-types/
/api/insurance-contracts/
```

The main CRUD endpoints are implemented with Django REST Framework viewsets and routers.

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Michalysko/insurance-management-app.git
cd insurance-management-app
```

### 2. Backend Setup

Go to the backend folder:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv ../venv
```

On Windows:

```bash
../venv/Scripts/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder. You can use `backend/.env.example` as a template.

Minimum local configuration:

```env
DJANGO_SECRET_KEY=your-local-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin user if needed:

```bash
python manage.py createsuperuser
```

Start the backend server:

```bash
python manage.py runserver
```

Backend runs at:

```text
http://127.0.0.1:8000/
```

### 3. Frontend Setup

Open a second terminal and go to the frontend folder:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Create a `.env` file inside the `frontend/` folder. You can use `frontend/.env.example` as a template.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Start the development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173/
```

## Environment Variables

The project uses environment variables for both local development and production deployment.

Backend examples:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-backend-domain.onrender.com
DJANGO_CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.vercel.app
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
```

Frontend example:

```env
VITE_API_BASE_URL=https://your-backend-domain.onrender.com/api
```

Real `.env` files are intentionally ignored by Git and must not be committed.

## Quality Checks

### Backend

```bash
cd backend
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

The backend test suite currently covers authentication, administrator and client permissions, insured person CRUD operations, insurance contract creation, client profile access, and protection of client-specific contract data.

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

Current project status:

- Django system check passes.
- Backend automated tests pass.
- Frontend lint passes.
- Frontend production build passes.
- The application is deployed and available as a public demo.

## Security Notes

This repository is public, so sensitive data is kept outside version control.

Ignored files include:

- `.env`
- `backend/.env`
- `backend/db.sqlite3`
- `backend/staticfiles/`
- `frontend/node_modules/`
- `frontend/dist/`
- `venv/`

The deployed demo uses:

- `DEBUG=False`,
- environment-based `SECRET_KEY`,
- production `ALLOWED_HOSTS`,
- configured CORS and CSRF trusted origins,
- HTTPS-only production settings,
- PostgreSQL hosted on Neon.

## Screenshots

### Login Page

![Login page](docs/screenshots/login-page.png)

### Administrator - Insured People

![Administrator - insured people page](docs/screenshots/admin-insured-people.png)

### Client - My Profile

![Client - my profile page](docs/screenshots/client-profile.png)

## Roadmap

Planned improvements:

- Add screenshots to this README.
- Add a small dashboard with summary statistics.
- Expand backend tests for insurance type CRUD operations, search, and validation.
- Improve demo data handling with a repeatable seed command.
- Add safer demo-mode restrictions for destructive administrator actions.
- Continue polishing responsive design for mobile and tablet viewports.
- Improve accessibility details such as labels, focus states, and keyboard navigation.

## What I Learned

While building this project, I practiced:

- designing relational models in Django,
- building REST API endpoints with Django REST Framework,
- implementing token authentication,
- separating administrator and client access,
- connecting a React frontend to a Django backend,
- handling pagination and search,
- managing state in React,
- working with Git and GitHub,
- preparing environment-based configuration,
- deploying a full-stack application with separate frontend, backend, and database services,
- improving project structure and security for a public repository.

## Project Status

The application is functional, deployed, and actively being improved as a portfolio project. It is intended as a learning and demonstration project, not as production software for real insurance operations.
