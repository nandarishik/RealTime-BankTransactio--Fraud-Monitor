import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Real-Time Fraud Detection Dashboard",
    page_icon="💳",
    layout="wide"
)

# --- Database Connection ---
conn = st.connection("postgres", type="sql")

# --- App Title ---
st.title("💳 Real-Time Banking Fraud Transaction Monitoring")

# --- Data Loading ---
# The ttl parameter caches the data for 2 seconds, preventing excessive queries
# but ensuring the data is fresh on each rerun.
df = conn.query('SELECT * FROM transactions ORDER BY timestamp DESC', ttl="2s")

# Ensure timestamp is in datetime format for plotting
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get the most recent data for display
latest_transactions = df.head(50) # For charts
detected_frauds = df[df['is_flagged'] == 1]

# --- Key Metrics ---
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(
    label="Total Transactions Processed 🔄",
    value=f"{len(df)}"
)
kpi2.metric(
    label="Total Volume Processed 💵",
    value=f"${df['amount'].sum():,.2f}"
)
kpi3.metric(
    label="Potential Frauds Detected 🚨",
    value=f"{len(detected_frauds)}"
)

# --- Visualizations ---
fig_col1, fig_col2 = st.columns([3, 2])

with fig_col1:
    st.subheader("Transaction Amounts Over Time (Last 50)")
    fig_line = px.line(
        latest_transactions,
        x='timestamp',
        y='amount',
        title='Transaction Flow',
        template='plotly_white',
        markers=True
    )
    fig_line.update_layout(xaxis_title='Time', yaxis_title='Transaction Amount ($)')
    st.plotly_chart(fig_line, use_container_width=True)

with fig_col2:
    st.subheader("Fraud vs. Legitimate Distribution")
    status_counts = df['is_flagged'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    status_counts['status'] = status_counts['status'].map({0: 'Legitimate', 1: 'Fraudulent'})
    fig_pie = px.pie(
        status_counts,
        names='status',
        values='count',
        title='Legitimate vs. Fraudulent',
        color='status',
        color_discrete_map={'Legitimate': 'green', 'Fraudulent': 'red'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Detected Frauds Table ---
st.subheader("🚨 Alerts: Transactions Flagged as Potential Fraud")
if not detected_frauds.empty:
    st.dataframe(detected_frauds[['timestamp', 'user_id', 'amount', 'merchant', 'location_city']].sort_values(by='timestamp', ascending=False))
else:
    st.info("No high-value fraud detected yet.")

# --- Auto-refresh logic ---
st.rerun(ttl=5)