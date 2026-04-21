# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:51:20 2026

@author: LENOVO
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import imageio.v2 as imageio

df = pd.read_csv("sales_data.csv")

df

# Basic check
df.head()
df.info()

# Checking missing and duplicate values

df.isnull().sum()

df.duplicated().sum()

# Feature Engineering

df['Date'] = pd.to_datetime(df['Date'])


df['Month'] = df['Date'].dt.month

# Sales Trend
monthly_sales = df.groupby('Month')['Total_Sales'].sum().reset_index()

plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_sales, x='Month', y='Total_Sales', marker='o')
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.show()

# Product Performance

product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
sns.barplot(x=product_sales.index, y=product_sales.values)
plt.title("Product Performance")
plt.tight_layout()
plt.show()

# Customer Segmentation

df['Customer_Group'] = pd.qcut(df['Total_Sales'], q=4,
                              labels=['Low', 'Medium', 'High', 'Premium'])

sns.boxplot(x='Customer_Group', y='Total_Sales', data=df)
plt.title("Customer Segmentation by Revenue")
plt.show()


# Violin Plot
sns.violinplot(x='Product', y='Total_Sales', data=df)
plt.title("Revenue Distribution by Product")
plt.xticks(rotation=45)
plt.show()

# Correlation Heatmap

corr = df[['Quantity', 'Price', 'Total_Sales']].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# Dashboard Layout..

fig, axes = plt.subplots(2, 2, figsize=(12,10))

# Sales trend
sns.lineplot(ax=axes[0,0], data=monthly_sales, x='Month', y='Total_Sales')
axes[0,0].set_title("Sales Trend")

# Product performance
sns.barplot(ax=axes[0,1], x=product_sales.index, y=product_sales.values)
axes[0,1].set_title("Product Revenue")

# Customer segmentation
sns.boxplot(ax=axes[1,0], x='Customer_Group', y='Total_Sales', data=df)
axes[1,0].set_title("Customer Segmentation")

# Distribution
sns.violinplot(ax=axes[1,1], x='Product', y='Total_Sales', data=df)
axes[1,1].set_title("Distribution by Product")

plt.tight_layout()
plt.savefig("visualizations/dashboard_demo.png")
plt.show()


# Interactive Plot
import plotly.express as px

fig = px.bar(df, x='Product', y='Total_Sales', color='Product',
             title="Interactive Product Revenue")

fig.show(renderer="browser")


# Styling

sns.set_palette("viridis")
plt.style.use('ggplot')

# Interactive Plot - Monthly Sales
fig = px.line(monthly_sales, x='Month', y='Total_Sales', title="Interactive Sales Trend")
fig.show(renderer="browser")

# Interactive Dropdown

fig = px.bar(df, x='Product', y='Total_Sales', color='Product',
             title="Product Revenue Interactive")

fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(label="All", method="update", args=[{"visible": [True]}]),
            ]
        )
    ]
)

fig.show(renderer="browser")

# Cohesive Theme

sns.set_palette("viridis")
plt.rcParams['figure.facecolor'] = '#f5f5f5'


image = imageio.imread("visualizations/dashboard_demo.png")

# Repeat same image to create GIF
frames = [image] * 10  

imageio.mimsave("visualizations/dashboard.gif", frames, duration=0.5)


