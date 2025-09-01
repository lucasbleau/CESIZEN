const fs = require('fs');
const path = require('path');
const db = require('../src/db'); // doit exposer .query

const MIGRATIONS_DIR = path.join(__dirname, '..', 'migrations');

async function ensureTable() {
  await db.query(`CREATE TABLE IF NOT EXISTS schema_migrations(
    id SERIAL PRIMARY KEY,
    filename TEXT UNIQUE NOT NULL,
    run_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  );`);
}

async function applied() {
  const res = await db.query('SELECT filename FROM schema_migrations');
  return new Set(res.rows.map(r => r.filename));
}

async function run() {
  await ensureTable();
  const done = await applied();

  if (!fs.existsSync(MIGRATIONS_DIR)) {
    console.log('No migrations directory, creating.');
    fs.mkdirSync(MIGRATIONS_DIR, { recursive: true });
    return;
  }

  const files = fs.readdirSync(MIGRATIONS_DIR)
    .filter(f => f.match(/^\d+_.*\.sql$/))
    .sort();

  for (const file of files) {
    if (done.has(file)) continue;
    const full = path.join(MIGRATIONS_DIR, file);
    const sql = fs.readFileSync(full, 'utf8');
    process.stdout.write(`→ Applying ${file} ... `);
    try {
      await db.query('BEGIN');
      await db.query(sql);
      await db.query('INSERT INTO schema_migrations(filename) VALUES ($1)', [file]);
      await db.query('COMMIT');
      console.log('OK');
    } catch (e) {
      await db.query('ROLLBACK');
      console.error(`FAIL\n${e.message}`);
      process.exit(1);
    }
  }
  console.log('Migrations complete.');
  process.exit(0);
}

run().catch(e => {
  console.error(e);
  process.exit(1);
});