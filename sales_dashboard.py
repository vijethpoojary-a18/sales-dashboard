import pandas as pd

# Load data
df = pd.read_csv("sales_data.csv")

# Convert date column
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

print("Dataset Preview:")
print(df.head())

print("\nTotal Revenue:", df["Sales"].sum())
print("Total Profit:", df["Profit"].sum())
print("Total Orders:", df["OrderID"].count())
import matplotlib.pyplot as plt

# Create Month column
df["Month"] = df["OrderDate"].dt.to_period("M")

# Group by month
monthly_sales = df.groupby("Month")["Sales"].sum()

print("\nMonthly Sales:")
print(monthly_sales)

# Plot line chart
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)

plt.show()
# Sales by Category
category_sales = df.groupby("Category")["Sales"].sum()

print("\nSales by Category:")
print(category_sales)

# Pie chart
plt.figure()
category_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Sales by Category")
plt.ylabel("")

plt.show()