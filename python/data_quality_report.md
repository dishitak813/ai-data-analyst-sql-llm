# Data Quality Report

## Overview

This report documents data quality issues identified and resolved during the cleaning of:

* Campaign Performance Data
* Shopify Sales Data

The objective was to ensure consistency, accuracy, and usability for downstream analytics (SQL, Power BI, AI tool).

---

# 1. Campaign Data Cleaning

## 1.1 Duplicate Records

* **Issue:** Potential duplicate rows
* **Action:** Checked using `df.duplicated()`
* **Result:** No significant duplicates found / removed if present

---

## 1.2 Date Format Issues

* **Issue:** Mixed or invalid date formats
* **Action:** Converted using `pd.to_datetime(errors='coerce')`
* **Result:** Invalid values converted to `NaT`

---

## 1.3 Invalid Dates

* **Issue:** ~5984 invalid date entries
* **Action:** Identified using null checks
* **Handling:** Left as `NaT` (no safe imputation possible)

---

## 1.4 Missing Values

* **Issue:** Missing values across multiple columns
* **Strategy:**

  * Numerical columns → kept as is or 0 where logical
  * Categorical columns → filled with `"unknown"`
* **Reason:** Preserve maximum data while avoiding incorrect assumptions

---

## 1.5 Metric Validation (CTR, CPC, CPM, ROI)

* **Issue:** Derived metrics not present or unreliable
* **Action:** Recalculated from base columns:

  * CTR = Clicks / Impressions
  * CPC = Spend / Clicks
  * CPM = Spend / Impressions × 1000
  * ROI = Revenue / Spend
* **Result:** Created clean calculated columns

---

## 1.6 String Normalisation

* **Issue:** Inconsistent casing and formatting
* **Action:**

  * Converted to lowercase
  * Trimmed spaces
  * Replaced 'nan', 'none' with null
* **Result:** Standardised categorical values

---

## 1.7 Final Status

* Data cleaned and loaded into: `cleaned_campaigns.db`
* Table: `campaigns`

---

# 2. Shopify Sales Data Cleaning

## 2.1 Duplicate Records

* **Issue:** Possible duplicate transactions
* **Action:** Checked and removed duplicates
* **Result:** Dataset ensured unique transactions

---

## 2.2 Date & Timestamp Standardisation

* **Columns:**

  * Date
  * Transaction Timestamp
  * Order Created At
  * Order Updated At

* **Issue:** Mixed formats and timezone strings

* **Action:**

  * Converted to datetime using pandas
  * Preserved timezone where applicable

---

## 2.3 Invalid Date Logic

* **Checks Performed:**

  * Order Created ≤ Order Updated
  * Transaction Timestamp ≥ Order Created

* **Result:**

  * Invalid order dates: 0
  * Invalid transaction times: 787 (due to missing/inconsistent timestamps)

---

## 2.4 Missing Values

* **Issue:** Null values in multiple columns
* **Strategy:**

  * Critical columns preserved
  * Categorical → filled with `"unknown"`
  * Optional fields → left null

---

## 2.5 String Normalisation

* **Issue:** Inconsistent text formats (e.g., Product Tags, Country)
* **Action:**

  * Lowercased all strings
  * Trimmed whitespace
  * Cleaned null-like values (`nan`, `None`)
* **Result:** Uniform categorical values

---

## 2.6 Complex Fields Handling

* **Example:** Product Tags (comma-separated values)
* **Handling:** Kept as string but standardised formatting
* **Note:** Could be exploded in advanced analysis

---

## 2.7 Final Status

* Data cleaned and loaded into: `cleaned_shopify.db`
* Table: `shopify_sales`

---

# 3. Summary of Improvements

| Area           | Improvement                  |
| -------------- | ---------------------------- |
| Dates          | Standardised across datasets |
| Missing Values | Handled with clear strategy  |
| Metrics        | Recalculated for accuracy    |
| Strings        | Normalised and cleaned       |
| Data Integrity | Logical checks applied       |
| SQL Readiness  | Structured and loaded        |

---

# 4. Conclusion

The datasets are now:

* Clean and consistent
* Ready for SQL querying
* Suitable for Power BI dashboards
* Usable for AI-driven insights

All transformations were performed with minimal data loss and clear justification.
