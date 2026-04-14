import sqlite3
from google import genai
import pandas as pd

conn = sqlite3.connect("../sql/final_marketing.db")

client = genai.Client(api_key="AIzaSyBbPHHjOdbOSa23u-6gMhGeJ18FJy-LyUs")

def generate_sql(question):
    prompt = f"""
You are a SQL expert.

Convert the following question into a valid SQLite SQL query.

DATABASE HAS 2 TABLES:

1. campaigns
Columns:
    'Data Source name', 'Date', 'Campaign Name',
    'Campaign Effective Status', 'Ad Set Name', 'Ad Name', 'Country Funnel',
    'Geo Location Segment', 'FB Spent Funnel (INR)', 'spend',
    'Clicks (all)', 'Impressions', 'Page Likes', 'Landing Page Views',
    'Link Clicks', 'Adds to Cart', 'Checkouts Initiated',
    'Adds of Payment Info', 'purchases', 'revenue', 'Website Contacts',
    'Messaging Conversations Started',
    'Adds to Cart Conversion Value (INR)',
    'Checkouts Initiated Conversion Value (INR)',
    'Adds of Payment Info Conversion Value (INR)', 'Row Count', 'CTR',
    'CPC', 'CPM', 'ROI'

2. shopify
Columns:
    'Data Source name', 'Date', 'Currency', 'Sales Channel',
    'Transaction Timestamp', 'Order Created At', 'Order Updated At',
    'Order ID', 'Order Name', 'Country Funnel', 'Geo Location Segment',
    'Billing Country', 'Billing Province', 'Billing City', 'Order Tags',
    'Product ID', 'Product Title', 'Product Tags', 'Product Type',
    'Variant Title', 'Gross Sales (INR)', 'Net Sales (INR)',
    'Total Sales (INR)', 'Orders', 'Returns (INR)', 'Return Rate',
    'Items Sold', 'Items Returned', 'Average Order Value (INR)',
    'New Customer Orders', 'Returning Customer Orders',
    'Average Items Per Order', 'Discounts (INR)', 'Row Count', 'SKU',
    'Customer Sale Type', 'Customer ID', 'Shipping Country',
    'invalid_order_dates', 'invalid_transaction_time', 'ROI_calculated',
    'ROI_flag'

IMPORTANT RULES:
- Use campaigns table for CPC, CTR, CPM, ROI, clicks, impressions, spend, total sales, etc., according to given columns above in campaign
- Use shopify table for revenue, orders, sales_channel, region performance, billing country for region, etc., according to given columns in shopify
- You can JOIN tables using:
    campaigns.date = shopify.date
    AND campaigns.data_source_name = shopify.data_source_name
- Use SQLite syntax (strftime for date filtering)
- ALWAYS wrap column names in double quotes
- Example: "Date", "Campaign Name", "CPC"
- For filtering countries:
  Use flexible matching with LIKE instead of exact match.
  Example:
  WHERE LOWER("Billing Country") LIKE '%united%'
- Only return SQL query (no explanation)

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    sql = response.text.strip()

    # clean markdown
    sql = sql.replace("```sql", "").replace("```sqlite", "").replace("```", "")

    # ✅ ADD CLEANING HERE
    import re

    sql = response.text.strip()

    # remove markdown
    sql = re.sub(r"```.*?\n", "", sql)
    sql = sql.replace("```", "")
    sql = sql.replace("sqlite", "")

    # ✅ fix newline issue
    sql = sql.replace("\\n", " ")

    # optional: remove extra spaces
    sql = " ".join(sql.split())

    return sql.strip()

def run_sql(sql, conn):
    df = pd.read_sql(sql, conn)
    return df

def explain_result(question, df, chat_history):

    # convert dataframe → text (VERY IMPORTANT)
    data_sample = df.head(10).to_string(index=False)

    history_text = ""
    for chat in chat_history:
        history_text += f"Q: {chat['question']}\nA: {chat['answer']}\n"

    prompt = f"""
You are a data analyst.

Previous conversation:
{history_text}

User question:
{question}

SQL result:
{data_sample}

Explain the answer in simple English.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()

def ask_ai(question, conn, chat_history):

    sql = generate_sql(question)

    print("Generated SQL:")
    print(sql)

    df = run_sql(sql, conn)

    print("\nSQL Result:")
    print(df)

    # 3. explain result
    explanation = explain_result(question, df, chat_history)

    print("\nAI Explanation:")
    print(explanation)

    return sql, df, explanation