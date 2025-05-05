# CQC Django App

This README provides instructions to set up and run the CQC Django app locally.

## Prerequisites

Ensure you have the following installed:
- Python (>= 3.8)
- pip (Python package manager)
- virtualenv (optional but recommended)

## Setup Instructions

1. **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd CQC
    ```

2. **Create and Activate a Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Development Server**
    ```bash
    python cqc/manage.py runserver
    ```

5. **Access the Application**
    Open your browser and navigate to `http://127.0.0.1:8000`.

## Additional Notes

- To create a superuser for admin access:
  ```bash
  python cqc/manage.py createsuperuser
  ```
- For static files, ensure `collectstatic` is run if needed:
  ```bash
  python cqc/manage.py collectstatic
  ```

## Troubleshooting

- Ensure all dependencies are installed correctly.
- Check for incorrect configurations in `settings.py`.
- SQLite database file is included in the repository, so no need to run migrations.

