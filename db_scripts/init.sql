SELECT 'CREATE DATABASE KBANK'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'KBANK');