-- =====================================================
-- SCHEMA DESIGN: Growify Data Analytics Assignment
-- =====================================================
-- This schema is designed for Power BI dashboards and AI tools.
-- It follows a simple star schema:
--   - fact_sales → main transactional data
--   - dim_date → time dimension
-- =====================================================


-- =========================================
-- DATE DIMENSION TABLE
-- =========================================

date_range = pd.date_range(start='2025-01-01', end='2026-12-31')

date_df = pd.DataFrame({
    'date': date_range,
    'day': date_range.day,
    'week': date_range.isocalendar().week,
    'month': date_range.month,
    'month_name': date_range.strftime('%B'),
    'quarter': date_range.quarter,
    'year': date_range.year,
    'day_name': date_range.strftime('%A')
})

date_df.to_sql("dim_date", conn, if_exists="replace", index=False)

-- =========================================
-- STEP 3: STAR SCHEMA DESIGN
-- =========================================

-- FACT TABLE: SALES (central table)
DROP TABLE IF EXISTS fact_sales;

CREATE TABLE fact_sales AS
SELECT
    s.date,
    s.data_source_name,
    c.campaign_name,
    s.billing_country,
    s.sales_channel,

    -- SALES METRICS
    s.total_sales_inr AS revenue,
    s.orders,
    s.items_sold,

    -- MARKETING METRICS
    c.spend AS spend,
    c."clicks_(all)" AS clicks,
    c.impressions AS impressions

FROM shopify s
LEFT JOIN campaigns c
ON s.date = c.date
AND s.data_source_name = c.data_source_name;


-- DIMENSION TABLE: CAMPAIGN
DROP TABLE IF EXISTS dim_campaign;

CREATE TABLE dim_campaign AS
SELECT DISTINCT
    campaign_name
FROM campaigns;


-- =========================================
-- STAR SCHEMA RELATIONSHIP (LOGICAL)
-- =========================================

-- fact_sales = central table (contains metrics)
-- dim_campaign = descriptive table (campaign names)
-- dim_date = time dimension (created separately)

-- Relationships:
-- fact_sales.date = dim_date.date
-- fact_sales.campaign_name = dim_campaign.campaign_name  (proxy join)

-- Note:
-- No foreign keys are defined because datasets do not have a reliable unique key.
-- Relationships are maintained logically during querying.


-- =========================================
-- POWER BI AGGREGATION QUERY
-- =========================================

SELECT
    f.data_source_name AS platform,
    f.sales_channel AS channel,
    f.billing_country AS region,
    strftime('%Y-%m', date(f.date)) AS month,

    SUM(f.revenue) AS total_revenue,
    SUM(f.orders) AS total_orders,
    SUM(f.items_sold) AS total_items

FROM fact_sales f

WHERE 
    f.data_source_name IS NOT NULL
    AND f.sales_channel IS NOT NULL
    AND f.date IS NOT NULL
    AND f.billing_country IS NOT NULL

    AND f.data_source_name != 'unknown'
    AND f.sales_channel != 'unknown'
    AND f.billing_country != 'unknown'

GROUP BY
    platform,
    channel,
    region,
    month

ORDER BY
    month, 
    platform, 
    channel;

-- =========================================
-- AI TOOL FLEXIBLE QUERY
-- =========================================

SELECT
    f.data_source_name AS platform,
    f.sales_channel AS channel,
    f.billing_country AS region,
    strftime('%Y-%m', date(f.date)) AS month,

    SUM(f.revenue) AS total_revenue,
    SUM(f.orders) AS total_orders,
    SUM(f.items_sold) AS total_items

FROM fact_sales f

WHERE
    -- Mandatory date filter
    date(f.date) BETWEEN :start_date AND :end_date

    -- Optional filters
    AND (:platform IS NULL OR f.data_source_name = :platform)
    AND (:region IS NULL OR f.billing_country = :region)
    AND (:channel IS NULL OR f.sales_channel = :channel)

    -- Data quality filters
    AND f.data_source_name IS NOT NULL
    AND f.sales_channel IS NOT NULL
    AND f.billing_country IS NOT NULL
    AND f.data_source_name != 'unknown'
    AND f.sales_channel != 'unknown'
    AND f.billing_country != 'unknown'

GROUP BY
    platform,
    channel,
    region,
    month

ORDER BY
    month;


-- =========================================
-- INDEXES FOR PERFORMANCE
-- =========================================

-- Index on date → improves date range filtering
CREATE INDEX IF NOT EXISTS idx_fact_sales_date
ON fact_sales(date);

-- Index on platform → improves platform filtering
CREATE INDEX IF NOT EXISTS idx_fact_sales_platform
ON fact_sales(data_source_name);

-- Index on region → improves region filtering
CREATE INDEX IF NOT EXISTS idx_fact_sales_region
ON fact_sales(billing_country);

-- Index on channel → improves channel filtering
CREATE INDEX IF NOT EXISTS idx_fact_sales_channel
ON fact_sales(sales_channel);


-- =====================================================
-- NOTES
-- =====================================================
-- - Indexes improve read/query performance
-- - Suitable for analytics workloads (Power BI, AI tools)
-- - Negative revenue values retained (refunds/cancellations)
-- =====================================================