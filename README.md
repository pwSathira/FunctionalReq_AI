# Laundromat Requirements Automation System

This project automates the extraction and rephrasing of functional requirements from a laundromat system description using Natural Language Processing (NLP) and Google's Gemini AI.

## Prerequisites

*   Python 3.6+
*   A Google API Key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

## Setup

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the virtual environment:**

    *   **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

    *   **Linux/macOS:**

        ```bash
        source .venv/bin/activate
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the Google API Key as an environment variable:**

    ```bash
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

    (Replace `"YOUR_GOOGLE_API_KEY"` with your actual API key.)
    
5.  **Rename sample.env -> .env**

6.  **Run**
    ```bash
    python main.py
    ```   

   
