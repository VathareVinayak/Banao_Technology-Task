
# Django Role-Based Auth Task

This is a Django-based Django Role-Based Auth web application focused on managing user signups, logins, and dashboards with user roles: patients and doctors. It supports both browser-based views and JSON API responses for integration and testing.

---

## Features

- **User Signup** with profile picture upload and extended profile data.
- **User Login** with role-based dashboard redirection (patient or doctor).
- **Role-based Dashboards** rendering profile info.
- **Logout** functionality.
- Support for **browser form submissions** and **API JSON requests**.
- CSRF protection disabled only for easy API testing (not recommended for production).
- Tailwind CSS used for modern, responsive UI.
- File upload handling with media serving during development.

---

## Tech Stack

- Python 3.11+
- Django 5.1.6
- Tailwind CSS (via CDN)
- NeonDB (PostgreSQL-compatible) for database
- dj_database_url for dynamic DB configuration
- python-dotenv for environment variables

---

## Setup Instructions

1. **Clone the repository**

   ```
   git clone <repo-url>
   cd <project-directory>
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

3. **Configure `.env` file**

   Place a `.env` file in project root with the following content:

   ```
   DATABASE_URL="postgresql://<user>:<password>@<host>/<dbname>?sslmode=require"
   ```

5. **Run database migrations**

   ```
   python manage.py migrate
   ```

6. **Start Django development server**

   ```
   python manage.py runserver
   ```

7. **Access application**

   - Open browser at [http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/)
   - Use Postman for API testing as described below.

---

## API Testing with Postman

### Signup (POST `/accounts/signup/`)

- Use `form-data` body
- Required fields:
  - `first_name`, `last_name`, `username`, `email`
  - `password`, `confirm_password`
  - `user_type` (`patient` or `doctor`)
  - `profile_picture` (file)
  - `address_line1`, `city`, `state`, `pincode`
- Returns JSON success or validation errors.

### Login (POST `/accounts/login/`)

- Use `form-data` or `x-www-form-urlencoded`
- Fields: `username`, `password`
- Returns JSON success message with user role or error.

### Dashboards (GET `/accounts/patient-dashboard/` and `/accounts/doctor-dashboard/`)

- Requires login session cookie
- Returns browser-rendered HTML pages.

### Logout (GET `/accounts/logout/`)

- Logs out user and redirects to login page.

---

## Important Notes

- **CSRF protection** is disabled on signup and login views with `@csrf_exempt` for ease of API testing. **Do not use this in production.**
- Media files uploaded are served locally in development under `/media/` URL.
- Tailwind CSS is included via CDN for quick styling.

---

## Folder Structure

- `cors/` — Django project folder
- `accounts/` — Django app folder (views, models, forms, templates)
- `media/` — Uploaded files storage
- `static/` — For static assets (if configured)
- `.env` — Environment variables file (not committed)

---

## Contact

For issues or contributions, please open an issue or pull request.
