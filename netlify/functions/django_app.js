const { builder } = require('@netlify/functions');
const serverless = require('serverless-http');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Path to the WSGI application
const wsgiPath = path.join(process.cwd(), 'kidney_stones_django', 'wsgi.py');

// Check if the WSGI file exists
if (!fs.existsSync(wsgiPath)) {
  console.error('WSGI file not found at:', wsgiPath);
  process.exit(1);
}

// Create a simple Express-like handler for Django
const handler = async (event, context) => {
  // Set environment variables for the Django process
  process.env.DJANGO_SETTINGS_MODULE = 'kidney_stones_django.settings';
  process.env.PYTHONPATH = process.cwd();
  
  // Start the Gunicorn server
  const gunicorn = spawn('gunicorn', [
    '--bind', '0.0.0.0:8000',
    '--workers', '1',
    '--timeout', '30',
    'kidney_stones_django.wsgi:application'
  ], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: process.env
  });

  // Log Gunicorn output
  gunicorn.stdout.on('data', (data) => {
    console.log(`Gunicorn stdout: ${data}`);
  });

  gunicorn.stderr.on('data', (data) => {
    console.error(`Gunicorn stderr: ${data}`);
  });

  // Wait for Gunicorn to start (simple delay for demo purposes)
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Forward the request to the running Gunicorn server
  const response = await fetch('http://localhost:8000' + event.path, {
    method: event.httpMethod,
    headers: event.headers,
    body: event.body
  });

  // Parse the response
  const body = await response.text();
  const headers = Object.fromEntries(response.headers.entries());
  
  // Clean up the Gunicorn process
  gunicorn.kill();

  return {
    statusCode: response.status,
    headers,
    body
  };
};

// Export the Netlify Function
module.exports.handler = builder(handler);
