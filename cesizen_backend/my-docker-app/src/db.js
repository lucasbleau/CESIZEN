const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST || process.env.PGHOST || 'db',
  port: parseInt(process.env.DB_PORT || process.env.PGPORT || '5432', 10),
  user: process.env.DB_USER || process.env.POSTGRES_USER || process.env.PGUSER || 'cesizen',
  password: process.env.DB_PASSWORD || process.env.POSTGRES_PASSWORD || process.env.PGPASSWORD || 'password',
  database: process.env.DB_NAME || process.env.POSTGRES_DB || process.env.PGDATABASE || 'cesizen_import',
  max: 5,
  idleTimeoutMillis: 30000,
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  pool,
};