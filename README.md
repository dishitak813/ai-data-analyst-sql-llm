# AI Data Analyst — LLM over SQL

An AI-powered data analyst that allows users to query structured databases using natural language instead of SQL.

This system converts user questions into SQL queries using an LLM, executes them on a database, and returns business insights in plain English.

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

## Project Demo

### Streamlit UI
[UI] <img width="2879" height="1603" alt="App UI image" src="https://github.com/user-attachments/assets/ea58686b-6730-49df-8a83-c72531202bf3" />

### Example Query Output
[Output] <img width="2862" height="1473" alt="App UI image" src="https://github.com/user-attachments/assets/0e963552-352f-463f-8c2c-460e30e9536b" />

### Power BI Dashboard
[Dashboard] <img width="2016" height="1135" alt="Dashboard image" src="https://github.com/user-attachments/assets/b3547f8b-e124-4011-9248-8db6437735b6" />


---

## System Architecture

1. User enters query in natural language  
2. LLM converts query → SQL  
3. SQL executes on SQLite database  
4. Query results returned  
5. LLM generates human-readable insights  

### Components:
- LLM (Google Gemini)
- SQLite Database
- Python Processing Layer
- Streamlit UI

---

## Example Interaction

**User Query:**  
Which campaign had the worst CPC in March?

**Generated SQL:**  
```sql
SELECT campaign_name, CPC 
FROM table 
WHERE month = 'March' 
ORDER BY CPC DESC 
LIMIT 1;
```

**Output:**  
Campaign X had the highest CPC in March, indicating inefficient ad spend.

---

## Project Structure

```
/data  
/python  
/sql  
/powerbi  
/ai_tool  
README.md  
requirements.txt  
```

---

## Setup Instructions

```bash
pip install -r requirements.txt  
streamlit run ai_tool/app.py  
```

---

## API Setup

This project uses Google Gemini API.

Add your API key in `ai_tool.ipynb` and `app_func.py`:

```python
from google import genai  
client = genai.Client(api_key="YOUR_API_KEY")  
```

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
- Used `strftime()` for time-based filtering (e.g., month analysis)  
- Avoided exact string matching → used `LIKE` for robustness  
- Ensured column names are quoted to avoid syntax errors  
- Used joins carefully to avoid mismatched date formats  

---

## Prompt Engineering Decisions

- Provided strict schema to LLM → reduces hallucination  
- Forced SQL-only output → avoids explanation noise  
- Cleaned LLM output (removed markdown, formatting issues)  
- Passed ONLY query results to LLM → prevents data leakage  
- Used flexible filtering (`LOWER + LIKE`) for inconsistent values  
- Added conversation history → enables follow-up queries  

---

## Conversation Memory

Implemented using Streamlit session state:
- Stores previous questions and answers  
- Injects context into LLM prompt  
- Enables multi-turn interaction  

**Example:**
- Q1: Which campaign had worst CPC in March?  
- Q2: What about February?  
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

```DAX
Conversion Rate = DIVIDE(SUM(fact_sales[conversions]), SUM(fact_sales[clicks]))  

ROI = DIVIDE(SUM(fact_sales[revenue]), SUM(fact_sales[spend]))  

CPC = DIVIDE(SUM(fact_sales[spend]), SUM(fact_sales[clicks]))  

CTR = DIVIDE(SUM(fact_sales[clicks]), SUM(fact_sales[impressions]))  
```

---

## DAX Logic Explanation

- Used `DIVIDE()` instead of `/` to avoid division-by-zero errors  
- Aggregated values using `SUM()` for correct totals  
- Measures dynamically adjust with filters and slicers  

---

## Example Questions

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

`final_marketing.db` is not included due to size constraints.

It can be recreated using:
- Cleaned datasets in `/python`  
- Processing scripts in `/python`  

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

## Key Learnings

- LLM + SQL integration  
- Prompt engineering for structured output  
- Data validation and preprocessing  
- Power BI dashboarding  
- Building end-to-end AI tools  

---

## 👩‍💻 Author

Dishita  
