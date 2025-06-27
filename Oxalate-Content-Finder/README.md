# Oxalate Content Finder

This is a simple web application that allows you to search for the oxalate content of various foods. The data is embedded directly within the application, eliminating the need for file uploads.

## Features

-   **Embedded Oxalate Database**: The application comes with a pre-loaded dataset of over 100 foods and their oxalate content, categorized by food type.
-   **Food Search**: Easily search for specific foods and view their oxalate levels.
-   **Oxalate Level Categorization**: Oxalate content is categorized into "Very High", "High", "Moderate", "Low", and "Very Low" for quick understanding.
-   **Responsive Design**: The application is designed to be user-friendly across different devices.

## How to Use

1.  **Open `index.html`**: Simply open the `index.html` file in your web browser.
2.  **Search for Food**: Use the search bar to type in the name of a food.
3.  **View Results**: The application will display the oxalate content and its category.

## Oxalate Level Categories

The oxalate levels are categorized as follows:

-   **Very High**: > 100 mg per serving
-   **High**: 50 - 100 mg per serving
-   **Moderate**: 20 - 49 mg per serving
-   **Low**: 10 - 19 mg per serving
-   **Very Low**: < 10 mg per serving

## Technical Details

-   **Frontend**: HTML, CSS, JavaScript
-   **Data**: Hardcoded JavaScript array within `script.js`
-   **No External Libraries**: The application is built with vanilla JavaScript, HTML, and CSS, with no external dependencies.

## Running the Application (Optional: Using a Python Server)

If you prefer to serve the application via a local web server (e.g., for development or to avoid browser security restrictions on local file access):

1.  **Ensure Python is Installed**: Make sure you have Python 3 installed on your system.
2.  **Run `server.py`**: Open your terminal or command prompt, navigate to the directory where `server.py` is located, and run the following command:

    ```bash
    python server.py
    ```

3.  **Access in Browser**: Your default web browser should automatically open to `http://localhost:8000/`. If not, open your browser and navigate to that address manually.

## Disclaimer

The oxalate content data provided in this application is for informational purposes only and should not be considered medical advice. Always consult with a healthcare professional for dietary recommendations, especially if you have health concerns related to oxalate intake.