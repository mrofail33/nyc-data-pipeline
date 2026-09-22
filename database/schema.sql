CREATE TABLE IF NOT EXISTS service_requests (
    unique_key TEXT PRIMARY KEY,
    created_date TIMESTAMP NOT NULL,
    closed_date TIMESTAMP,
    agency TEXT,
    agency_name TEXT,
    complaint_type TEXT,
    descriptor TEXT,
    status TEXT,
    borough TEXT,
    incident_zip TEXT,
    city TEXT,
    resolution_description TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    resolution_time_hours DOUBLE PRECISION,
    created_month TEXT
);

CREATE INDEX IF NOT EXISTS idx_service_requests_borough
    ON service_requests (borough);

CREATE INDEX IF NOT EXISTS idx_service_requests_complaint_type
    ON service_requests (complaint_type);

CREATE INDEX IF NOT EXISTS idx_service_requests_created_date
    ON service_requests (created_date);
