SQL Stock Reporting Suite

A full-stack data reporting project that demonstrates how to collect live stock market data, store it in a relational database, and visualize it through an interactive Streamlit dashboard.

This project is designed as a portfolio-grade example of real-world data engineering and reporting using Python, SQL, and Streamlit.

Project Overview

The SQL Stock Reporting Suite performs the following tasks:

1. Fetches live stock market data from an external API
2. Stores the data in a MySQL database
3. Uses SQL queries and views to generate reports
4. Displays interactive charts and tables in a Streamlit web application

This mirrors how financial reporting dashboards are built in production environments.

What This Project Demonstrates

API data ingestion using Python
Relational database design with MySQL
SQL-based reporting logic
Secure environment variable and secrets management
Web dashboard deployment using Streamlit Cloud

Technology Stack

Backend: Python
Database: MySQL
Data Processing: Pandas
Visualization: Streamlit
Secrets Management: Streamlit Secrets
Deployment: Streamlit Cloud
Version Control: Git and GitHub

Project Structure

```
sql-stock-reporting-suite/
│
├── app/
│   └── dashboard.py        Main Streamlit dashboard
│
├── data/
│   └── fetch_stocks.py     Script to fetch stock data from API
│
├── sql/
│   └── schema.sql          Database schema and tables
│
├── requirements.txt        Python dependencies
└── README.md               Project documentation
```

 Environment Variables and Secrets

This project does not store sensitive information in the repository.

All credentials and API keys are stored using Streamlit Secrets.

Example secrets configuration:

```toml
DB_HOST="your-db-host"
DB_USER="your-db-user"
DB_PASSWORD="your-db-password"
DB_NAME="stock_database"
ALPHAVANTAGE_KEY="your-api-key"
```

These values are accessed in Python using:

```python
import streamlit as st

db_host = st.secrets["DB_HOST"]
api_key = st.secrets["ALPHAVANTAGE_KEY"]
```

Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/yousifsarhan/sqlproject.git
cd sqlproject/sql-stock-reporting-suite
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

bash
pip install -r requirements.txt


Run the Streamlit application:


streamlit run app/dashboard.py


Deployment

The application is deployed using Streamlit Cloud.

Deployment process:

* Push the repository to GitHub
* Connect the repository on Streamlit Cloud
* Add secrets in Manage App settings
* Deploy the application

Features

Live stock price updates
SQL-backed reporting
Interactive charts and tables
Secure credential handling
Cloud-based deployment

Why This Project Matters

This project reflects real-world data workflows commonly used in financial analytics, business intelligence dashboards, and backend-driven web applications.

It demonstrates an understanding of end-to-end systems rather than isolated scripts.

done by

Yousif Sarhan
Bachelor of Multimedia Systems
Aspiring Software and Data Engineer

Future Improvements<img width="1402" height="463" alt="Screenshot 2026-01-07 at 11 02 50 PM" src="https://github.com/user-attachments/assets/c5683bb1-e77d-4a2a-a255-fb0520614bdc" />


Scheduled background data updates
Additional financial indicators<img width="1402" height="564" alt="Screenshot 2026-01-07 at 11 03 07 PM" src="https://github.com/user-attachments/assets/a556de09-0a61-482d-aa1c-caf43f3e7646" />

User-selectable stock symbols
Authentication and user roles

