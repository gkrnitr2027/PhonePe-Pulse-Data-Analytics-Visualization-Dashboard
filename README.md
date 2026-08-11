📱 PhonePe Pulse Data Analytics Dashboard

An end-to-end Data Engineering and Business Intelligence project built using the open-source PhonePe Pulse dataset.

The project extracts nested JSON data, transforms and cleans it using Python, stores the processed data in PostgreSQL, and provides an interactive analytics dashboard using Streamlit and Plotly.

🏗️ Project Workflow
PhonePe Pulse JSON
       ↓
Python ETL
       ↓
Data Cleaning & Transformation
       ↓
CSV Files
       ↓
PostgreSQL
       ↓
SQLAlchemy
       ↓
Streamlit + Plotly Dashboard

Pipeline
Extract – Reads nested JSON files containing state, district, year, quarter, and transaction data.
Transform – Cleans data, handles missing keys/schema variations, and creates structured datasets.
Load – Loads processed data into PostgreSQL using SQLAlchemy.
Analyze – Uses SQL queries to generate business metrics.
Visualize – Displays interactive charts and KPIs through Streamlit.
🛠️ Tech Stack
Python 3.10+
Pandas & JSON
PostgreSQL
SQLAlchemy & Psycopg2
Streamlit
Plotly
Git & GitHub
🗄️ Main Datasets
aggregated_transactions

State-level transaction data containing:

State
Year
Quarter
Transaction Type
Transaction Count
Transaction Amount
top_transactions

District-level transaction data containing:

State
Year
Quarter
District
Transaction Count
Transaction Amount
📊 Dashboard Features
💰 Total Transaction Value and Volume
🗺️ State-wise transaction analysis
💳 Payment category distribution
📈 Yearly transaction trends
🏙️ Top district transaction rankings
🔎 Interactive filters and visualizations
📁 Project Structure
phonepe_pulse_project/
│
├── pulse/                      # PhonePe Pulse dataset
├── extract_data.py             # ETL & JSON processing
├── load_to_postgres.py         # PostgreSQL data loader
├── app.py                      # Streamlit dashboard
├── aggregated_transactions.csv
├── top_transactions.csv
├── requirements.txt
└── README.md

🚀 Setup & Run
1. Create Virtual Environment
python -m venv pulse_env
.\pulse_env\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt


Or:

pip install pandas sqlalchemy psycopg2-binary streamlit plotly

3. Get PhonePe Pulse Data
git clone https://github.com/PhonePe/pulse.git

4. Run ETL
python extract_data.py

5. Create PostgreSQL Database

Create a database named:

phonepe_pulse


Then run:

python load_to_postgres.py

6. Launch Dashboard
streamlit run app.py


Open:

http://localhost:8501

🎯 Project Objectives

This project demonstrates practical skills in:

Data Extraction & ETL
Python & Pandas
JSON Data Processing
PostgreSQL & SQL
Data Cleaning
Business Analytics
Data Visualization
Interactive Dashboard Development
📚 Data Source

PhonePe Pulse Open-Source Dataset

https://github.com/PhonePe/pulse

👨‍💻 Author

G.K.

Data Analytics | Data Engineering | Python | SQL | PostgreSQL
