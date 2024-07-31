import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("C:/Users/Kumar Madhusudan/Desktop/data/Customer.csv")
df[df.duplicated(subset=['Customer_ID'], keep=False)]
df.Customer_ID.unique().shape
df1=pd.read_csv("C:/Users/Kumar Madhusudan/Desktop/data/Order.csv")
df1.shape
df1[df1.duplicated(subset=['Order_ID'], keep=False)]
df1.Customer_ID.unique().shape
df3=pd.merge(df,df1, on="Customer_ID", how="inner")
df_grouped = df3.groupby('Country').agg({'Order_ID': 'count', 'Amount': 'sum'}).reset_index()
min_transactions_country = df_grouped.loc[df_grouped['Order_ID'].idxmin()]
min_sales_amount_country = df_grouped.loc[df_grouped['Amount'].idxmin()]
min_transactions_country
min_sales_amount_country
df3['Age_Category'] = df3['Age'].apply(lambda x: 'Less than 30' if x < 30 else '30 and above')
df_grouped = df3.groupby(['Age_Category', 'Item'])['Amount'].sum().reset_index()
df_max_product = df_grouped.loc[df_grouped.groupby('Age_Category')['Amount'].idxmax()]
df_max_product
dfgrouped=df3.groupby(['Country', 'Item'])['Amount'].sum().reset_index()
df_max_product = dfgrouped.loc[dfgrouped.groupby('Country')['Amount'].idxmax()]
df_max_product
df2=pd.read_json("C:/Users/Kumar Madhusudan/Desktop/data/Shipping.json")
df4=df2[df2.Status=='Pending']
df5=pd.merge(df,df4, on="Customer_ID", how="inner")
df6=pd.merge(df5,df1,on="Customer_ID",how="inner")
df7=df6.groupby(['Country','Status'])['Amount'].sum().reset_index()
customer_orders = df3.groupby('Customer_ID').agg(
    Total_Transactions=('Order_ID', 'count'),
    Total_Amount_Spent=('Amount', 'sum'),
    Last_Order_Date=('Order_ID', 'max'),  # Simulating order date with Order_ID
    Last_Order_Amount=('Amount', 'max')
).reset_index()

final_df = pd.merge(customer_orders, df2, on='Customer_ID', how='inner')
final_df['Status'].fillna('No Recent Shipping', inplace=True)
final_df = pd.merge(df, final_df, on='Customer_ID', how='inner')

# Plot total amount spent by country
plt.figure(figsize=(12, 6))
sns.barplot(data=final_df, x='Country', y='Total_Amount_Spent', estimator=sum, ci=None)
plt.title('Total Amount Spent by Country')
plt.xlabel('Country')
plt.ylabel('Total Amount Spent')
plt.show()

# Plot total transactions by country
plt.figure(figsize=(12, 6))
sns.barplot(data=final_df, x='Country', y='Total_Transactions', estimator=sum, ci=None)
plt.title('Total Transactions by Country')
plt.xlabel('Country')
plt.ylabel('Total Transactions')
plt.show()

age_category = df.copy()
age_category['Age_Category'] = age_category['Age'].apply(lambda x: 'Under 30' if x < 30 else '30 and Above')
merged_age_df = pd.merge(age_category, df1, on='Customer_ID', how='left')

most_purchased = merged_age_df.groupby(['Age_Category', 'Item']).size().reset_index(name='Counts')
most_purchased = most_purchased.sort_values(by='Counts', ascending=False).groupby('Age_Category').first().reset_index()


# Plot most purchased product by age category
plt.figure(figsize=(12, 6))
sns.barplot(data=most_purchased, x='Age_Category', y='Counts', hue='Item')
plt.title('Most Purchased Product by Age Category')
plt.xlabel('Age Category')
plt.ylabel('Counts')
plt.show()
