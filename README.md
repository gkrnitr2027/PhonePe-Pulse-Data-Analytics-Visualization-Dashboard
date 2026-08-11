📱 PhonePe Pulse Data Analytics & Visualization Dashboard

An end-to-end Data Engineering, SQL Analytics, and Business Intelligence project built using the open-source PhonePe Pulse
 dataset.

This project demonstrates a complete data pipeline — from extracting deeply nested JSON files and handling schema variations to transforming the data, loading it into PostgreSQL, and building an interactive Streamlit + Plotly dashboard for business insights.

The dashboard enables users to explore digital payment trends across Indian states, districts, transaction categories, and financial years using dynamic SQL queries.

📌 Project Overview

Digital payments in India generate massive amounts of transactional data across different regions and payment categories.

The goal of this project is to transform PhonePe Pulse's raw JSON data into a structured analytical database and provide an interactive dashboard that answers questions such as:

📈 How has digital payment volume changed over the years?
🗺️ Which states contribute the highest transaction value?
💳 Which payment categories are most popular?
🏙️ Which districts are the major transaction hubs?
💰 How does transaction value vary across different regions?
📊 What are the year-over-year trends in digital payments?

🔄 ETL & Analytics Workflow
1. Extract

The Python ETL pipeline traverses the PhonePe Pulse repository and processes the nested JSON files containing quarterly data.

The extraction process captures information across:

States
Districts
Financial years
Quarters
Transaction categories
Transaction counts
Transaction amounts
2. Transform

The raw JSON data is converted into structured Pandas DataFrames.

The transformation layer handles real-world data challenges including:

Nested JSON structures
Inconsistent directory structures
Missing keys
Schema variations across years
State-name normalization
District-level aggregation
Data type conversion
Duplicate or inconsistent records
3. Load

Cleaned datasets are exported to CSV and loaded into PostgreSQL using SQLAlchemy and Psycopg2.

The database provides a structured foundation for analytical SQL queries.

4. Analyze

The Streamlit application executes parameterized SQL queries against PostgreSQL to generate metrics and visualizations dynamically.

5. Visualize

Plotly is used to create interactive visualizations for:

State-level comparisons
Payment category analysis
Yearly trends
Transaction volume
Transaction value
District rankings
🛠️ Technology Stack
Category	Technology
Programming Language	Python 3.10+
Data Processing	Pandas
Data Format	JSON / CSV
Database	PostgreSQL 14+
Database Connectivity	SQLAlchemy
PostgreSQL Driver	Psycopg2
Dashboard	Streamlit
Visualization	Plotly Express
Development Environment	VS Code / Jupyter / PowerShell
Version Control	Git / GitHub
🗄️ Database Schema

The project currently works with two primary analytical datasets.

1. aggregated_transactions

Contains state-level transaction metrics aggregated by year, quarter, and transaction category.

Column	Type	Description
State	VARCHAR	Normalized Indian state name
Year	INT	Financial year
Quarter	INT	Financial quarter (1–4)
Transaction_Type	VARCHAR	Payment category
Transaction_Count	BIGINT	Number of transactions
Transaction_Amount	FLOAT	Total transaction value in INR
Example transaction categories
Peer-to-peer payments
Merchant payments
Recharge & bill payments
Financial services
Other payment categories available in the source data
2. top_transactions

Contains district-level transaction metrics used for geographical analysis and leaderboards.

Column	Type	Description
State	VARCHAR	Normalized state name
Year	INT	Financial year
Quarter	INT	Financial quarter
Entity_Type	VARCHAR	Entity classification
Entity_Name	VARCHAR	District name
Transaction_Count	BIGINT	Number of transactions
Transaction_Amount	FLOAT	Total transaction value in INR
📊 Dashboard Features
💰 Executive KPIs

The dashboard provides high-level business metrics such as:

Total Payment Value (TPV)
Total Transaction Volume
Average Transaction Value
Overall transaction activity across selected periods
🗺️ Geographic Analysis

Compare payment activity across Indian states using interactive charts.

Users can identify:

Highest transaction-value states
Highest transaction-volume states
Regional payment concentration
Emerging high-growth markets
💳 Payment Category Analysis

Analyze the distribution of transactions across different payment categories.

Interactive charts help identify the relative contribution of:

Peer-to-peer transactions
Merchant payments
Recharges
Bill payments
Other transaction categories
📈 Yearly Growth Analysis

Explore historical digital-payment adoption using time-series visualizations.

The dashboard allows users to identify:

Growth in transaction volume
Growth in transaction value
Changes in payment-category composition
Long-term adoption trends
🏙️ District-Level Leaderboards

Analyze transaction activity at the district level to identify major digital-payment hubs.

Users can explore:

Top districts by transaction volume
Top districts by transaction value
State-wise district performance
Quarterly district trends
📁 Project Structure
phonepe_pulse_project/
│
├── pulse/                         # PhonePe Pulse source repository
│
├── extract_data.py                # JSON extraction & transformation
├── load_to_postgres.py            # CSV → PostgreSQL loader
├── app.py                         # Streamlit dashboard
│
├── aggregated_transactions.csv    # State/category dataset
├── top_transactions.csv           # District-level dataset
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Ignored files & secrets

⚙️ Installation & Setup
Prerequisites

Make sure the following are installed:

Python 3.10+
PostgreSQL 14+
Git
pgAdmin or PostgreSQL command-line tools
1️⃣ Clone the Project
git clone
cd phonepe_pulse_project

2️⃣ Create a Virtual Environment
python -m venv pulse_env


Activate it in Windows PowerShell:

.\pulse_env\Scripts\activate


After activation, you should see something similar to:

(pulse_env) PS C:\...\phonepe_pulse_project>

3️⃣ Install Dependencies
pip install -r requirements.txt


If you haven't created requirements.txt yet:

pip install pandas sqlalchemy psycopg2-binary streamlit plotly


You can then generate the file with:

pip freeze > requirements.txt

4️⃣ Download PhonePe Pulse Dataset

Clone the official PhonePe Pulse repository:

git clone https://github.com/PhonePe/pulse.git


This will create:

phonepe_pulse_project/
└── pulse/


Note: If pulse is already cloned, do not clone it again.

🧹 Important Git Note

If you plan to push this project to GitHub, make sure pulse is not accidentally treated as a nested Git repository.

If pulse is simply part of your project and you don't need its independent Git history:

Remove-Item -Recurse -Force .\pulse\.git


Then:

git add .
git status


If you intentionally want pulse to remain a separate repository, use it as a Git submodule instead.

🗃️ PostgreSQL Setup

Create a PostgreSQL database named:

phonepe_pulse


You can create it through pgAdmin or SQL:

CREATE DATABASE phonepe_pulse;


Make sure PostgreSQL is running on:

localhost:5432

🔐 Database Configuration

Update the PostgreSQL connection details in load_to_postgres.py.

Example:

DATABASE_URL = (
    "postgresql+psycopg2://username:password@localhost:5432/phonepe_pulse"
)

Recommended

Do not commit database passwords to GitHub.

Instead, use environment variables:

$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="phonepe_pulse"


Then access them in Python using:

import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


Add sensitive files to .gitignore:

.env
*.env
__pycache__/
pulse_env/

🚀 Running the Pipeline
Step 1 — Extract & Transform

Run:

python extract_data.py


This processes the PhonePe Pulse JSON files and generates:

aggregated_transactions.csv
top_transactions.csv

Step 2 — Load into PostgreSQL

Make sure the phonepe_pulse database exists and PostgreSQL is running.

Then execute:

python load_to_postgres.py


The script loads the processed CSV datasets into PostgreSQL.

Step 3 — Launch the Dashboard

Run:

streamlit run app.py


The dashboard will be available at:

http://localhost:8501


Open the URL in your browser.

📈 Example Business Questions

The dashboard can be used to answer questions such as:

Transaction Trends
What is the total transaction volume for a particular year?
How has transaction value changed over time?
Which quarter has the highest transaction activity?
Geographic Performance
Which state has the highest transaction value?
Which states have the largest transaction volume?
Which districts are major payment hubs?
Payment Categories
What percentage of transactions are peer-to-peer?
How significant are merchant payments?
How has the payment-category mix changed over time?
District Analysis
Which districts generate the highest transaction value?
Which districts have the highest transaction count?
How does district performance vary between states?
💡 Key Insights

The dashboard is designed to highlight patterns such as:

📈 Long-term growth in digital payment adoption
🗺️ Geographic concentration of payment activity
💳 Changing contribution of different payment categories
🏙️ Emergence of high-volume district-level payment hubs
📊 Differences between transaction volume and transaction value

The actual insights depend on the filters and period selected in the dashboard.

🎯 Project Objectives

This project demonstrates practical experience with:

Data Engineering
ETL Pipeline Development
JSON Data Extraction
Data Cleaning & Transformation
Schema Drift Handling
Relational Database Design
PostgreSQL
SQL Analytics
Python & Pandas
Data Visualization
Interactive Dashboard Development
Business Intelligence
🔮 Future Improvements

Potential enhancements include:

 Add interactive India maps using Plotly
 Add year-over-year growth calculations
 Add state and district filters
 Add automated ETL scheduling
 Add data validation tests
 Add database indexes for frequently queried columns
 Move database credentials entirely to environment variables
 Containerize the application using Docker
 Deploy the Streamlit dashboard online
 Add automated GitHub Actions for testing
 Add more PhonePe Pulse datasets such as user and insurance data
 Add advanced SQL analytics and stored procedures
📚 Data Source

This project uses the publicly available PhonePe Pulse dataset.

Source: PhonePe Pulse — Open Source Data

The dataset provides aggregated information about digital payments in India across states, districts, years, quarters, and transaction categories.

Data Analytics | Data Engineering | Python | SQL | PostgreSQL | Power BI / Streamlit

⭐ If You Found This Project Useful

If this project helped you understand ETL pipelines, PostgreSQL analytics, or dashboard development, consider giving the repository a ⭐ on GitHub.
