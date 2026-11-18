-- Run with psql, connected to the maintenance database postgres.
-- Creates only the database, if missing. No application tables are created.
\set ON_ERROR_STOP on
SELECT 'CREATE DATABASE trycore_evm'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'trycore_evm')
\gexec
