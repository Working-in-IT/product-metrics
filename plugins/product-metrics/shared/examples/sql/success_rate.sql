-- Educational implementation 1; beacon.success_rate, definition_version: 1.
-- SQLite; named parameters bound by the client. All timestamps are UTC.
-- Input: prepared scenario_facts as defined in README.md (not raw events).
WITH cohort AS (
    SELECT outcome
    FROM scenario_facts
    WHERE product_id = :product_id
      AND started_at >= :period_start
      AND started_at < :period_end
), totals AS (
    SELECT
        COUNT(*) AS attempts,
        COALESCE(SUM(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END), 0) AS successes
    FROM cohort
)
SELECT
    :product_id AS product_id,
    :period_start AS period_start,
    :period_end AS period_end,
    :as_of AS as_of,
    attempts,
    successes,
    CASE
        WHEN julianday(:as_of) < julianday(:period_end) + 3 THEN 'preliminary'
        WHEN attempts = 0 THEN 'empty_cohort'
        ELSE 'calculated'
    END AS calculation_status,
    CASE
        WHEN julianday(:as_of) >= julianday(:period_end) + 3
        THEN 1.0 * successes / NULLIF(attempts, 0)
        ELSE NULL
    END AS success_rate
FROM totals;
