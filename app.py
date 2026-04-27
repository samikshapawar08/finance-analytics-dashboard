import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine

st.set_page_config(page_title="Finance Dashboard", layout="wide")


db_url = os.environ.get("DATABASE_URL")

if not db_url:
    db_url = "postgresql://postgres:newpassword123@host:5432/finance_db"

engine = create_engine(db_url)

# THEN THIS
df = pd.read_sql("SELECT * FROM finance_data", engine)

df = pd.read_sql("SELECT * FROM finance_data", engine)


total_revenue = df['revenue'].sum()
total_profit = df['profit'].sum()
total_cost = df['cost'].sum()
profit_margin = (total_profit / total_revenue) * 100


monthly = df.groupby('month').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'cost': 'sum'
}).sort_index()

monthly['margin'] = (monthly['profit'] / monthly['revenue']) * 100
monthly['contribution'] = (monthly['revenue'] / total_revenue) * 100

# ---------------- INSIGHTS ----------------
best_month = monthly['revenue'].idxmax()
best_margin_month = monthly['margin'].idxmax()

# ---------------- UI ----------------
st.title("📊 Finance Analytics Dashboard")

# KPI ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{round(total_revenue,2)}")
col2.metric("Profit", f"₹{round(total_profit,2)}")
col3.metric("Cost", f"₹{round(total_cost,2)}")
col4.metric("Margin", f"{round(profit_margin,2)}%")

st.markdown("---")

# CHARTS ROW 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue vs Profit vs Cost")
    st.line_chart(monthly[['revenue','profit','cost']])

with col2:
    st.subheader("🥧 Revenue Contribution %")
    st.bar_chart(monthly['contribution'])

# CHARTS ROW 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Monthly Revenue")
    st.bar_chart(monthly['revenue'])

with col2:
    st.subheader("📉 Profit Margin Trend")
    st.line_chart(monthly['margin'])

st.markdown("---")

# INSIGHTS
st.subheader("🔍 Key Insights")

st.write(f"📈 Best Revenue Month: **{best_month}**")
st.write(f"🔥 Best Margin Month: **{best_margin_month}**")