import pandas as pd
from sqlalchemy import create_engine
import os

# ---------------------------------------------------------
# 1. PostgreSQL Database Credentials
# ---------------------------------------------------------
# Update these variables to match your local PostgreSQL setup
DB_USER = "postgres"           # Your PostgreSQL username (usually 'postgres')
DB_PASSWORD = "12345"  # Your PostgreSQL password
DB_HOST = "localhost"          # Usually 'localhost'
DB_PORT = "5432"               # Default PostgreSQL port is 5432
DB_NAME = "phonepe_pulse"      # The database you just created in pgAdmin

# Create the SQLAlchemy engine connecting to PostgreSQL
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

print(f"Connecting to PostgreSQL Database: '{DB_NAME}'...\n")

# ---------------------------------------------------------
# 2. File to Table Mapping
# ---------------------------------------------------------
# We include all 6 files, but the script will intelligently 
# skip the ones with 0 rows based on your extraction results.
files_to_tables = {
    "aggregated_transactions.csv": "aggregated_transactions",
    "top_transactions.csv": "top_transactions",
}

# ---------------------------------------------------------
# 3. Load Data into PostgreSQL
# ---------------------------------------------------------
for csv_file, table_name in files_to_tables.items():
    if os.path.exists(csv_file):
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Check if the DataFrame actually contains data
        if len(df) > 0:
            print(f"Loading '{csv_file}' ({len(df)} rows) into PostgreSQL table '{table_name}'...")
            
            # Push the data to PostgreSQL. 
            # if_exists="replace" will drop the table and recreate it if it already exists.
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            
            print(f"  --> Success! Table '{table_name}' created and loaded.\n")
        else:
            print(f"  [!] Skipping '{csv_file}': File exists but contains 0 rows.\n")
    else:
        print(f"  [!] Warning: '{csv_file}' not found in the directory.\n")

print("=" * 60)
print("PostgreSQL Database build complete! Ready for SQL analysis.")
print("=" * 60)