-- CyberSpy Database Schema

-- Table to store analysis results from various modules (File, URL, QR, PCAP)
CREATE TABLE IF NOT EXISTS analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    filename TEXT NOT NULL,       -- Name of the file, URL, or identifier
    risk_score INTEGER,           -- 0-100 Security Risk Score
    summary TEXT,                 -- AI or Scanner Summary
    details JSONB,                -- Structured technical details (threats, capabilities)
    source TEXT                   -- Source of analysis (e.g., "VirusTotal", "Gemini AI")
);

-- Index for faster querying by source and risk score
CREATE INDEX IF NOT EXISTS idx_analysis_source ON analysis_results(source);
CREATE INDEX IF NOT EXISTS idx_analysis_risk ON analysis_results(risk_score);
