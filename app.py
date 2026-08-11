import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ---------------------------------------------------------
# 1. Page Configuration & Custom Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="PhonePe Pulse Analytics",
    page_icon="📱",
    layout="wide"
)

st.title("📱 PhonePe Pulse Data Analytics Dashboard")
st.markdown("Real-time SQL analytics built on **Aggregated Transactions** & **Top Transactions**.")

# ---------------------------------------------------------
# 2. Database Connection (PostgreSQL)
# ---------------------------------------------------------
DB_USER = "postgres"           # Your PostgreSQL username
DB_PASSWORD = "12345"  # <-- REPLACE WITH YOUR ACTUAL POSTGRESQL PASSWORD
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "phonepe_pulse"

@st.cache_resource
def get_db_engine():
    connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_string)

try:
    engine = get_db_engine()
except Exception as e:
    st.error(f"Error connecting to PostgreSQL database: {e}")
    st.stop()

def run_sql_query(query, params=None):
    """Executes a SQL query against PostgreSQL and returns a DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params=params)

# ---------------------------------------------------------
# 3. Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Global Filters")

# Fetch available Years dynamically from PostgreSQL
years_df = run_sql_query('SELECT DISTINCT "Year" FROM aggregated_transactions ORDER BY "Year" DESC;')
available_years = ["All"] + list(years_df['Year'].astype(str))
selected_year = st.sidebar.selectbox("Select Year", available_years)

# Fetch available Quarters
available_quarters = ["All", "Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]
selected_quarter_str = st.sidebar.selectbox("Select Quarter", available_quarters)

quarter_map = {"Q1 (Jan-Mar)": 1, "Q2 (Apr-Jun)": 2, "Q3 (Jul-Sep)": 3, "Q4 (Oct-Dec)": 4}
selected_quarter = quarter_map.get(selected_quarter_str, "All")

# Fetch available States for optional filtering
states_df = run_sql_query('SELECT DISTINCT "State" FROM aggregated_transactions ORDER BY "State" ASC;')
available_states = ["All"] + list(states_df['State'])
selected_state = st.sidebar.selectbox("Select State", available_states)

# Build dynamic SQL WHERE clause
where_clauses = []
if selected_year != "All":
    where_clauses.append(f'"Year" = {selected_year}')
if selected_quarter != "All":
    where_clauses.append(f'"Quarter" = {selected_quarter}')
if selected_state != "All":
    safe_state = selected_state.replace("'", "''")
    where_clauses.append(f'"State" = \'{safe_state}\'')

where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

# ---------------------------------------------------------
# 4. Executive Summary KPI Cards
# ---------------------------------------------------------
st.subheader("📊 Executive Summary")

kpi_query = f"""
    SELECT 
        COALESCE(SUM("Transaction_Amount"), 0) AS total_tpv,
        COALESCE(SUM("Transaction_Count"), 0) AS total_count,
        COALESCE(AVG("Transaction_Amount" / NULLIF("Transaction_Count", 0)), 0) AS avg_tx_value
    FROM aggregated_transactions
    {where_sql};
"""
kpi_data = run_sql_query(kpi_query)

tpv = kpi_data['total_tpv'].iloc[0]
count = kpi_data['total_count'].iloc[0]
avg_val = kpi_data['avg_tx_value'].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Payment Value (TPV)", f"₹ {tpv/1e11:.2f} Lakh Cr")
col2.metric("Total Transactions", f"{count/1e7:.2f} Cr")
col3.metric("Avg Transaction Value", f"₹ {avg_val:.2f}")

st.markdown("---")

# ---------------------------------------------------------
# 5. Dashboard Tabs
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📊 Aggregated Transaction Insights", "📍 Top Districts Leaderboard"])

# =========================================================
# TAB 1: AGGREGATED TRANSACTIONS
# =========================================================
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.write("### 🏆 State-wise Transaction Volume")
        state_query = f"""
            SELECT 
                "State", 
                SUM("Transaction_Amount") AS total_amount,
                SUM("Transaction_Count") AS total_count
            FROM aggregated_transactions
            {where_sql}
            GROUP BY "State"
            ORDER BY total_amount DESC
            LIMIT 10;
        """
        df_state = run_sql_query(state_query)

        if not df_state.empty:
            fig_state = px.bar(
                df_state, 
                x='total_amount', 
                y='State', 
                orientation='h',
                labels={'total_amount': 'Total Value (₹)', 'State': 'State'},
                color='total_amount',
                color_continuous_scale='Purples'
            )
            fig_state.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            st.plotly_chart(fig_state, use_container_width=True)
        else:
            st.info("No data found for the selected filters.")

    with col_b:
        st.write("### 🍕 Payment Category Share")
        cat_query = f"""
            SELECT 
                "Transaction_Type", 
                SUM("Transaction_Amount") AS total_amount
            FROM aggregated_transactions
            {where_sql}
            GROUP BY "Transaction_Type"
            ORDER BY total_amount DESC;
        """
        df_cat = run_sql_query(cat_query)

        if not df_cat.empty:
            fig_cat = px.pie(
                df_cat, 
                values='total_amount', 
                names='Transaction_Type', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No data found for the selected filters.")

    # Growth Trend Line Chart over Years
    st.write("### 📈 Yearly Transaction Growth Trend")
    trend_query = """
        SELECT 
            "Year", 
            SUM("Transaction_Amount") AS total_amount,
            SUM("Transaction_Count") AS total_count
        FROM aggregated_transactions
        GROUP BY "Year"
        ORDER BY "Year" ASC;
    """
    df_trend = run_sql_query(trend_query)
    
    if not df_trend.empty:
        fig_trend = px.line(
            df_trend,
            x='Year',
            y='total_amount',
            markers=True,
            title="Overall TPV Trend Across All Available Years",
            labels={'total_amount': 'Total Payment Value (₹)', 'Year': 'Year'},
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# =========================================================
# TAB 2: TOP DISTRICTS LEADERBOARD
# =========================================================
with tab2:
    st.write("### 📍 Leaderboard: Top 10 Districts")

    # Filter strictly for Districts
    top_query = f"""
        SELECT 
            "Entity_Name" AS district_name,
            "State",
            SUM("Transaction_Amount") AS total_amount,
            SUM("Transaction_Count") AS total_count
        FROM top_transactions
        WHERE "Entity_Type" = 'Districts'
        {" AND " + " AND ".join(where_clauses) if where_clauses else ""}
        GROUP BY "Entity_Name", "State"
        ORDER BY total_amount DESC
        LIMIT 10;
    """
    df_top = run_sql_query(top_query)

    col_t1, col_t2 = st.columns([2, 1])

    with col_t1:
        if not df_top.empty:
            fig_top = px.bar(
                df_top,
                x='district_name',
                y='total_amount',
                color='State',
                title="Top 10 Districts by Transaction Amount",
                labels={'total_amount': 'Total Amount (₹)', 'district_name': 'District'},
                barmode='group'
            )
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("No district data found for the selected filters.")

    with col_t2:
        st.write("### Data Summary")
        if not df_top.empty:
            df_display = df_top.copy()
            df_display['total_amount'] = df_display['total_amount'].apply(lambda x: f"₹{x:,.2f}")
            df_display['total_count'] = df_display['total_count'].apply(lambda x: f"{x:,}")
            st.dataframe(
                df_display[['district_name', 'State', 'total_amount', 'total_count']], 
                hide_index=True
            )
        else:
            st.info("No rows to display.")