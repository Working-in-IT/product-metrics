-- Synthetic prepared rows. No raw-event processing is tested by this fixture.
CREATE TABLE scenario_facts (
    product_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('success', 'failed', 'cancelled', 'timeout')),
    duration_seconds INTEGER,
    PRIMARY KEY (product_id, scenario_id),
    CHECK (
        (outcome = 'success' AND duration_seconds IS NOT NULL AND duration_seconds BETWEEN 0 AND 86400)
        OR (outcome <> 'success' AND duration_seconds IS NULL)
    )
);

INSERT INTO scenario_facts VALUES
    ('beacon', 's1', '2026-08-01T00:00:00Z', 'success', 3600),
    ('beacon', 's2', '2026-08-15T12:00:00Z', 'success', 7200),
    ('beacon', 's3', '2026-08-31T23:59:59Z', 'success', 86400),
    ('beacon', 's4', '2026-08-20T12:00:00Z', 'failed', NULL),
    ('beacon', 's5', '2026-08-20T13:00:00Z', 'cancelled', NULL),
    ('beacon', 's6', '2026-08-20T14:00:00Z', 'timeout', NULL),
    ('beacon', 'before', '2026-07-31T23:59:59Z', 'success', 1),
    ('beacon', 'end', '2026-09-01T00:00:00Z', 'failed', NULL),
    ('atlas', 'other', '2026-08-01T00:00:00Z', 'success', 1);
