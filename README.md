# AI Data Analyst — LLM over SQL

## Overview
This project builds an AI-powered data analyst that converts natural language queries into SQL, executes them on a structured database, and returns insights in plain English using an LLM.

The system integrates data cleaning, SQL querying, Power BI dashboarding, and AI-based reasoning into a single end-to-end pipeline.

---

## Features

- Natural language → SQL query generation  
- SQL execution on cleaned datasets  
- AI-generated business insights  
- Streamlit-based interactive UI  
- Conversation memory for follow-up questions  
- Data validation and quality checks  
- Power BI dashboard for visual analytics  

---

## System Architecture

User Question  
→ LLM generates SQL  
→ SQL executed on SQLite  
→ Result passed to LLM  
→ LLM generates explanation  

---

## Project Structure

/data  
/python  
/sql  
/powerbi  
/ai_tool  
README.md  
requirements.txt  

---

## Setup Instructions

pip install -r requirements.txt  
streamlit run ai_tool/app.py  

---

## API Setup

This project uses Google Gemini API.

Add your API key in `ai_tool.ipynb` and `app_func.py` files:

from google import genai  
client = genai.Client(api_key="YOUR_API_KEY")  

---

## Data Processing (Thinking & Decisions)

### Why data cleaning was necessary:
Raw datasets contained:
- Duplicate records  
- Inconsistent date formats  
- Missing values  
- Incorrect precomputed metrics  

### Key decisions:
- Recomputed metrics (CTR, CPM, CPC, ROI) instead of trusting raw values  
- Standardised text fields to avoid query mismatches  
- Preserved data instead of aggressive row deletion  

---

## SQL Design Decisions

- Used SQLite for lightweight querying  
- Used strftime() for time-based filtering (e.g., month analysis)  
- Avoided exact string matching → used LIKE for robustness  
- Ensured column names are quoted to avoid syntax errors  
- Used joins carefully to avoid mismatched date formats  

---

## Prompt Engineering Decisions

- Provided strict schema to LLM → reduces hallucination  
- Forced SQL-only output → avoids explanation noise  
- Cleaned LLM output (removed markdown, formatting issues)  
- Passed ONLY query results to LLM → prevents data leakage  
- Used flexible filtering (LOWER + LIKE) to handle inconsistent values  
- Added conversation history → enables follow-up queries  

---

## Conversation Memory (Bonus)

Implemented using Streamlit session state:
- Stores previous questions and answers  
- Injects context into LLM prompt  
- Enables multi-turn interaction  

Example:
Q1: Which campaign had worst CPC in March?  
Q2: What about February?  
→ Model understands context without repeating full question  

---

## Power BI Dashboard

A Power BI dashboard was built to visualize campaign performance and business metrics.

### Pages Included:
- Overview (KPIs, trends)  
- Channel breakdown  
- Audience insights  

### Key Visuals:
- KPI cards (Revenue, Spend, ROI)  
- Bar charts (Performance by platform)  
- Donut chart (Channel mix)  
- Matrix (Region performance)  
- Scatter plot (Spend vs Conversions)  

---

## DAX Measures Used

Conversion Rate = DIVIDE(SUM(fact_sales[conversions]), SUM(fact_sales[clicks]))  

ROI = DIVIDE(SUM(fact_sales[revenue]), SUM(fact_sales[spend]))  

CPC = DIVIDE(SUM(fact_sales[spend]), SUM(fact_sales[clicks]))  

CTR = DIVIDE(SUM(fact_sales[clicks]), SUM(fact_sales[impressions]))  

---

## DAX Logic Explanation

- Used DIVIDE() instead of / to avoid division-by-zero errors  
- Aggregated values using SUM() for correct totals  
- Measures dynamically adjust with filters and slicers  

---

## 10 Example Questions

1. Which campaign had the worst CPC in March?  
2. Which campaign has the highest ROI overall?  
3. Summarise UK region performance in terms of revenue and orders.  
4. Which campaign generated the highest revenue?  
5. What is the total spend and revenue by country?  
6. Which campaign has the lowest CTR?  
7. Compare performance across different regions.  
8. What is the monthly trend of revenue and conversions?  
9. Which campaign has the highest spend but low returns?  
10. What about February? (follow-up question using conversation memory)  

---

## Note on Database File

final_marketing.db is not included due to size constraints.

It can be recreated using:
- cleaned datasets in /python 
- processing scripts in /python 

---

## Tech Stack

- Python  
- Pandas  
- SQLite  
- Streamlit  
- Google Gemini API  
- Power BI  
- DAX  

---

## Key Learning

- LLM + SQL integration  
- Prompt engineering for structured output  
- Data validation and preprocessing  
- Power BI dashboarding  
- Building end-to-end AI tools  

---

## 👩‍💻 Author

Dishita
