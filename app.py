import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------ THEME SWITCH ------------------
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {background-color:#0E1117; color:white;}
        .css-1d391kg {background-color:#161A23;}
        </style>
    """, unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
df = pd.read_csv("sales_data.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# ------------------ SIDEBAR ------------------
st.sidebar.title("📌 Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

df = df[(df["Region"].isin(regions)) & (df["Category"].isin(categories))]

# ------------------ HEADER ------------------
st.title("📊 Sales Analytics Dashboard")
st.caption("Modern Data Analyst Portfolio Project")

# ------------------ KPI CALCULATIONS ------------------
revenue = df["Sales"].sum()
profit = df["Profit"].sum()
orders = df.shape[0]
profit_ratio = (profit / revenue) * 100

# ------------------ KPI CARDS ------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"₹ {revenue:,.0f}")
c2.metric("📈 Total Profit", f"₹ {profit:,.0f}")
c3.metric("🛒 Orders", orders)
c4.metric("🎯 Profit Ratio", f"{profit_ratio:.2f}%")

st.divider()

# ------------------ CHART ROW 1 ------------------
col1, col2 = st.columns(2)

with col1:
    region_sales = df.groupby("Region")["Sales"].sum().reset_index()
    fig1 = px.bar(region_sales, x="Region", y="Sales",
                  title="Sales by Region",
                  color="Region",
                  template="plotly_dark" if theme=="Dark" else "plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig2 = px.pie(cat_sales, names="Category", values="Sales",
                  title="Category Contribution",
                  template="plotly_dark" if theme=="Dark" else "plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ------------------ CHART ROW 2 ------------------
col3, col4 = st.columns(2)

with col3:
    monthly = df.groupby(df["OrderDate"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly["OrderDate"] = monthly["OrderDate"].astype(str)
    fig3 = px.line(monthly, x="OrderDate", y="Sales",
                   markers=True,
                   title="Monthly Sales Trend",
                   template="plotly_dark" if theme=="Dark" else "plotly_white")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    top_products = df.groupby("Product")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    fig4 = px.bar(top_products, x="Product", y="Sales",
                  title="Top Products",
                  color="Product",
                  template="plotly_dark" if theme=="Dark" else "plotly_white")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ------------------ PROFIT CHART ------------------
profit_region = df.groupby("Region")["Profit"].sum().reset_index()
fig5 = px.bar(profit_region, x="Region", y="Profit",
              title="Profit by Region",
              color="Region",
              template="plotly_dark" if theme=="Dark" else "plotly_white")
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ------------------ DOWNLOAD BUTTON ------------------
st.download_button(
    "📥 Download Filtered Data",
    df.to_csv(index=False),
    "Filtered_Sales.csv"
)

# ------------------ DATA TABLE ------------------
st.subheader("Filtered Dataset")
st.dataframe(df, use_container_width=True)

st.success("Dashboard Ready 🚀")