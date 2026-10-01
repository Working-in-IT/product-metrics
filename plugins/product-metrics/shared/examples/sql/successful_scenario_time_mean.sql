-- Educational implementation 1; beacon.successful_scenario_time_mean, definition_version: 1.
-- SQLite; named parameters bound by the client. All timestamps are UTC.
-- Same start cohort as success_rate.sql, even when success occurs next month.
WITH cohort AS (
    SELECT outcome, duration_seconds
    FROM scenario_facts
    WHERE product_id = :product_id
      AND started_at >= :period_start
      AND started_at < :period_end
), totals AS (
    SELECT
        COALESCE(SUM(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END), 0) AS successes,
        COALESCE(SUM(CASE WHEN outcome = 'success' THEN duration_seconds ELSE 0 END), 0) AS duration_sum_seconds
    FROM cohort
)
SELECT
    :product_id AS product_id,
    :period_start AS period_start,
    :period_end AS period_end,
    :as_of AS as_of,
    successes,
    duration_sum_seconds,
    CASE
        WHEN julianday(:as_of) < julianday(:period_end) + 3 THEN 'preliminary'
        WHEN successes = 0 THEN 'no_successes'
        ELSE 'calculated'
    END AS calculation_status,
    CASE
        WHEN julianday(:as_of) >= julianday(:period_end) + 3
        THEN 1.0 * duration_sum_seconds / NULLIF(successes, 0)
        ELSE NULL
    END AS mean_seconds
FROM totals;
