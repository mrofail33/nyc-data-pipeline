-- 1. Complaints by borough
SELECT
    borough,
    COUNT(*) AS complaint_count
FROM service_requests
GROUP BY borough
ORDER BY complaint_count DESC;

-- 2. Most common complaint types
SELECT
    complaint_type,
    COUNT(*) AS complaint_count
FROM service_requests
GROUP BY complaint_type
ORDER BY complaint_count DESC
LIMIT 10;

-- 3. Complaints by month
SELECT
    created_month,
    COUNT(*) AS complaint_count
FROM service_requests
GROUP BY created_month
ORDER BY created_month;

-- 4. Average resolution time
SELECT
    ROUND(AVG(resolution_time_hours)::numeric, 2) AS avg_resolution_time_hours
FROM service_requests
WHERE resolution_time_hours IS NOT NULL;

-- 5. Busiest complaint periods by hour of day
SELECT
    EXTRACT(HOUR FROM created_date) AS hour_of_day,
    COUNT(*) AS complaint_count
FROM service_requests
GROUP BY hour_of_day
ORDER BY complaint_count DESC;
