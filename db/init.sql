CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS sensor_readings (
  ts TIMESTAMPTZ NOT NULL,
  machine_id TEXT NOT NULL,
  sensor TEXT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  unit TEXT,
  PRIMARY KEY (ts, machine_id, sensor)
);

SELECT create_hypertable('sensor_readings', 'ts', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_readings_machine_ts ON sensor_readings (machine_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_readings_sensor_ts ON sensor_readings (sensor, ts DESC);

-- Optional retention / compression policies:
-- SELECT add_retention_policy('sensor_readings', INTERVAL '180 days');
-- ALTER TABLE sensor_readings SET (timescaledb.compress, timescaledb.compress_segmentby = 'machine_id');
-- SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');
