#!/usr/bin/env python
"""
Build configuration for Vercel deployment
"""
import os
import subprocess
import sys

def build():
    """Run build commands for Vercel deployment"""
    
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("Creating directories...")
    os.makedirs("staticfiles", exist_ok=True)
    os.makedirs("media", exist_ok=True)
    
    print("Collecting static files...")
    subprocess.check_call([
        sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"
    ])
    
    print("Running migrations...")
    subprocess.check_call([
        sys.executable, "manage.py", "migrate", "--noinput"
    ])
    
    print("Build completed successfully!")

if __name__ == "__main__":
    build()
