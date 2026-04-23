from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine("postgresql://postgres:newpassword123@localhost:5432/finance_db")

@app.route('/')
def dashboard():
    df = pd.read_sql("SELECT * FROM finance_data", engine)

    # ---------------- BASIC KPIs ----------------
    total_revenue = df['revenue'].sum()
    total_profit = df['profit'].sum()
    total_cost = df['cost'].sum()
    profit_margin = (total_profit / total_revenue) * 100

    # ---------------- MONTHLY AGG ----------------
    monthly = df.groupby('month').agg({
        'revenue': 'sum',
        'profit': 'sum',
        'cost': 'sum'
    }).sort_index()

    # Margin per month
    monthly['margin'] = (monthly['profit'] / monthly['revenue']) * 100

    # Contribution %
    monthly['contribution'] = (monthly['revenue'] / total_revenue) * 100

    # ---------------- DICTS ----------------
    revenue_data = monthly['revenue'].to_dict()
    profit_data = monthly['profit'].to_dict()
    cost_data = monthly['cost'].to_dict()
    margin_data = monthly['margin'].to_dict()
    contribution_data = monthly['contribution'].to_dict()

    # ---------------- INSIGHTS ----------------
    best_month = monthly['revenue'].idxmax()
    best_margin_month = monthly['margin'].idxmax()

    return render_template(
        "dashboard.html",
        revenue=round(total_revenue,2),
        profit=round(total_profit,2),
        cost=round(total_cost,2),
        margin=round(profit_margin,2),

        best_month=best_month,
        best_margin_month=best_margin_month,

        revenue_data=revenue_data,
        profit_data=profit_data,
        cost_data=cost_data,
        margin_data=margin_data,
        contribution_data=contribution_data
    )

if __name__ == "__main__":
    app.run(debug=True)