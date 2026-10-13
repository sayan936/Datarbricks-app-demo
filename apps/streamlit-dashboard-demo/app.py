import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Performance Dashboard")
st.markdown("Demo dashboard built with **Streamlit** + **Plotly** on Databricks Apps.")

# ------------------------------------------------------------------
# Generate dummy data
# ------------------------------------------------------------------
np.random.seed(42)

regions = ["North", "South", "East", "West"]
products = ["Widget A", "Widget B", "Gadget C", "Gadget D"]
categories = ["Electronics", "Accessories"]

n_rows = 500
today = datetime.today()
dates = [today - timedelta(days=int(d)) for d in np.random.randint(0, 365, n_rows)]

df = pd.DataFrame({
    "date": dates,
    "region": np.random.choice(regions, n_rows),
    "product": np.random.choice(products, n_rows),
    "category": np.random.choice(categories, n_rows),
    "units_sold": np.random.randint(1, 100, n_rows),
    "revenue": np.random.uniform(10, 500, n_rows).round(2),
})
df["revenue"] = df["revenue"] * df["units_sold"]

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_products = st.sidebar.multiselect("Product", products, default=products)

df_filtered = df[
    df["region"].isin(selected_regions)
    & df["product"].isin(selected_products)
]

# ------------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_revenue = df_filtered["revenue"].sum()
total_units = df_filtered["units_sold"].sum()
avg_order = df_filtered["revenue"].mean()
unique_products = df_filtered["product"].nunique()

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Avg Order Value", f"${avg_order:,.0f}")
col4.metric("Unique Products", f"{unique_products}")

st.divider()

# ------------------------------------------------------------------
# Charts
# ------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Region")
    rev_by_region = df_filtered.groupby("region")["revenue"].sum().reset_index()
    fig_bar = px.bar(
        rev_by_region, x="region", y="revenue", color="region",
        text_auto="$.0f",
    )
    fig_bar.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Revenue Trend Over Time")
    rev_over_time = (
        df_filtered.groupby(df_filtered["date"].dt.to_period("M"))["revenue"]
        .sum()
        .reset_index()
    )
    rev_over_time["date"] = rev_over_time["date"].dt.to_timestamp()
    fig_line = px.line(
        rev_over_time, x="date", y="revenue",
        markers=True,
    )
    fig_line.update_layout(height=350)
    st.plotly_chart(fig_line, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Product Mix")
    rev_by_product = df_filtered.groupby("product")["revenue"].sum().reset_index()
    fig_pie = px.pie(
        rev_by_product, values="revenue", names="product",
        hole=0.4,
    )
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right2:
    st.subheader("Units Sold by Category")
    units_by_cat = df_filtered.groupby("category")["units_sold"].sum().reset_index()
    fig_cat = px.bar(
        units_by_cat, x="category", y="units_sold", color="category",
        text_auto=True,
    )
    fig_cat.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Data table
# ------------------------------------------------------------------
st.subheader("Raw Data Sample")
st.dataframe(df_filtered.head(50), use_container_width=True)

st.caption("Dummy data generated with NumPy — no external data source required.")