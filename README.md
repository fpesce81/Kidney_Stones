# Kidney Stone Navigator

This is a Django web application for clinical decision support and patient education regarding kidney stones. It provides a user-friendly interface to assess patient profiles, analyze 24-hour urine results, and receive management recommendations.

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Running the Application Locally](#running-the-application-locally)
- [Deployment to Netlify](#deployment-to-netlify)
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

## Deployment to Netlify

This application is configured for deployment on Netlify using serverless functions. Follow these steps to deploy:

1. **Push your code to a Git repository** (GitHub, GitLab, or Bitbucket)

2. **Deploy to Netlify:**
   - Log in to your [Netlify](https://app.netlify.com/) account
   - Click on "New site from Git"
   - Select your Git provider and repository
   - Configure the build settings:
     - Build command: `./build.sh`
     - Publish directory: `staticfiles`
   - Click "Deploy site"

3. **Set up environment variables in Netlify:**
   - Go to Site settings > Build & deploy > Environment
   - Add the following required variables:
     - `DJANGO_SECRET_KEY`
     - `DJANGO_SETTINGS_MODULE=kidney_stones_django.production_settings`
     - `PYTHON_VERSION=3.11.0`
   - Add any other environment variables from your `.env` file

4. **Configure build settings (if not detected automatically):**
   - Set the Python version to 3.11.0 in the runtime.txt file
   - Ensure the build command is set to `./build.sh`

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
├── netlify/                  # Netlify serverless functions
├── static/                   # Static files
├── templates/                # HTML templates
├── .env.example              # Example environment variables
├── .gitignore               
├── manage.py                
├── netlify.toml             # Netlify configuration
├── requirements.txt          # Python dependencies
└── runtime.txt              # Python version for Netlify
```

## Troubleshooting

- If you encounter build issues on Netlify, check the build logs in the Netlify dashboard
- Ensure all environment variables are properly set in Netlify
- For local development, make sure your Python version matches the one in runtime.txt