# Kidney Stone Navigator

This is a Django web application for clinical decision support and patient education regarding kidney stones. It provides a user-friendly interface to assess patient profiles, analyze 24-hour urine results, and receive management recommendations.

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Running the Application Locally](#running-the-application-locally)
- [Deployment to Vercel](#deployment-to-vercel)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Kidney_Stones
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application Locally

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`

3. For admin access, visit `http://127.0.0.1:8000/admin/`

## Deployment to Vercel

Follow these steps to deploy on [Vercel](https://vercel.com):

1. **Push your code to a Git repository** (GitHub, GitLab, or Bitbucket).
2. **Import the project in Vercel** and configure the environment variables:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_SETTINGS_MODULE=kidney_stones_django.settings_production`
   - `DATABASE_URL` (optional, uses SQLite if not set)
3. Vercel will automatically run `python vercel_build.py` during the build step.
4. After deployment, your Django app will be served via Vercel's serverless
   functions and static CDN.

## Environment Variables

Create a `.env` file in the project root with the following variables (see `.env.example` for reference):

```
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=kidney_stones_django.production_settings

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgres://user:password@host:port/dbname

# Debug mode (set to False in production)
DEBUG=False

# Security settings
SECURE_SSL_REDIRECT=True
```

## Project Structure

```
Kidney_Stones/
├── kidney_stones_app/        # Main Django app
├── kidney_stones_django/     # Project settings
├── static/                   # Static files
├── templates/                # HTML templates
├── .env.example              # Example environment variables
├── .gitignore
├── manage.py
├── requirements.txt          # Python dependencies
└── runtime.txt              # Python version for development
```

## Troubleshooting

- If you encounter build issues on Vercel, check the build logs in the Vercel dashboard
- Ensure all environment variables are properly set in Vercel
- For local development, make sure your Python version matches the one in runtime.txt
