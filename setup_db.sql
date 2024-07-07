
-- Create production database if it doesn't exist
CREATE DATABASE hng_prod_db;
-- Create test database if it doesn't exist
CREATE DATABASE hng_test_db;

-- Create user if not exists
DO
$$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles
    WHERE rolname = 'hng_dev'
  ) THEN
    CREATE USER hng_dev WITH PASSWORD 'hng_dev_pwd';
  END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE hng_prod_db TO hng_dev;
GRANT ALL PRIVILEGES ON DATABASE hng_test_db TO hng_dev;