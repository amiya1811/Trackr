# Expense Tracker with Data Visualization using Pandas and Matplotlib

**App name:** Trackr  
**Tagline:** Track Smarter. Spend Better.

A GitHub-ready Streamlit web app for tracking income and expenses, analysing transaction data with Pandas, and visualizing results with Matplotlib.

## Main features
- Dashboard with income, expenses, cash flow, and transaction metrics
- Matplotlib charts: category donut chart, monthly spending line chart, income-vs-expense bar chart
- Pandas-based filtering, grouping, summaries, month comparisons, and spending insights
- Add, edit, delete, search, and filter transactions
- CSV import and export
- Category budgets and progress indicators
- Savings goals and contributions
- Reports downloadable as CSV
- SQLite local database

## Tech stack
Python · Streamlit · Pandas · Matplotlib · SQLite (`sqlite3`)

## Deploy online with GitHub + Streamlit Community Cloud

### 1. Upload this project to GitHub
1. Download and extract this ZIP.
2. Sign in to GitHub and create a **new repository** (for example, `trackr-expense-tracker`).
3. Keep the repository public if you want the simplest free deployment setup.
4. From the extracted folder, upload the project files and folders to the repository's root. Make sure `app.py` and `requirements.txt` are at the repository root, not inside an extra nested folder.
5. Commit the files.

### 2. Deploy the GitHub repository
1. Open **https://share.streamlit.io/** and sign in with GitHub.
2. Click **Create app** / **Deploy an app**.
3. Select the repository you just uploaded.
4. Set the branch to `main` (or whichever branch you used).
5. Set **Main file path** to `app.py`.
6. Click **Deploy** and wait for dependency installation and startup.
7. Streamlit will provide a public URL that you can share.

### 3. Update the live app
Edit the files in GitHub and commit your changes. Streamlit Community Cloud normally rebuilds/restarts the app after commits to the connected branch.

## Run locally in VS Code
```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bat
.venv\Scripts\activate.bat
```

Then:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` if it does not open automatically.

## Important note about online data storage
The app uses SQLite at `data/trackr.db`. The hosted app can create this file at runtime, but the local filesystem on free hosting is not guaranteed to be permanent across app restarts, rebuilds, or sleeping/redeploy events. Treat the hosted version as a demo unless you add a persistent external database. Do not enter sensitive financial information into a public demo.

## CSV import format
Required columns: `date`, `description`, `category`, `type`, `amount`  
Optional columns: `payment_method`, `notes`

```csv
date,description,category,type,amount,payment_method,notes
2026-10-01,Groceries,Food & Dining,Expense,850,UPI,Weekly shopping
2026-10-01,Salary,Salary,Income,42000,Bank transfer,Monthly salary
```

## Where the project title's libraries are used
- **Pandas:** DataFrames, transaction filtering, category/month grouping, totals, trend analysis, CSV processing, and outlier analysis.
- **Matplotlib:** the dashboard's donut, line, and bar charts.

## Project structure
```text
.
├── app.py
├── analytics.py
├── charts.py
├── database.py
├── styles.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── .gitkeep
└── reports/
    └── .gitkeep
```

## Academic disclaimer
This is an educational micro-project, not financial advice. Pattern observations are simple statistical indicators, not fraud detection.
