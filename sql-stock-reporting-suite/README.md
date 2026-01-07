SQL Stock Reporting Suite

Local setup
- Create and activate a venv, then install deps:
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
- Start MySQL and load schema/views/procs:
  mysql -u root < sql/01_schema.sql
  mysql -u root < sql/02_views.sql
  mysql -u root < sql/03_procedures.sql
- Set .env with DB credentials and Alpha Vantage key.
- Run the fetcher:
  python app/fetch_prices.py
- Run the dashboard (new terminal tab):
  streamlit run app/dashboard.py

Streamlit Cloud deployment
- Push this repo to GitHub.
- In Streamlit Cloud, set Main file path to: app/dashboard.py
- Add secrets (TOML) in Manage app -> Settings -> Secrets:
  ALPHAVANTAGE_API_KEY = "your_key"
  DB_HOST = "your_remote_db_host"
  DB_USER = "your_db_user"
  DB_PASSWORD = "your_db_password"
  DB_NAME = "stock_reporting"
  DB_PORT = "3306"
- Use a hosted MySQL database. localhost will not work on Streamlit Cloud.
