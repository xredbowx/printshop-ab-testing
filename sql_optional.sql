-- Optional PostgreSQL query after loading data/experiment.csv into experiment
SELECT variant, COUNT(*) AS visitors, SUM(converted) AS conversions,
 ROUND(100.0*AVG(converted),3) AS conversion_pct
FROM experiment GROUP BY variant;
