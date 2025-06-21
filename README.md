# Kidney Stone Navigator

This is a Streamlit web application for clinical decision support and patient education regarding kidney stones. It is based on a Jupyter Notebook and provides a user-friendly interface to assess patient profiles, analyze 24-hour urine results, and receive management recommendations.

## Setup

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\\venv\\Scripts\\activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the setup is complete, you can run the Streamlit app with the following command:

```bash
streamlit run app.py
```

This will start a local web server, and you can view the application in your browser at the provided URL (usually `http://localhost:8501`). 