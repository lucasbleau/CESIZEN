const db = require('../src/db');
(async () => {
  const rows = [
    ['Respiration 4-4-6', 'Cycle simple', 4, 0, 6],
    ['Cohérence cardiaque', '5-5 classique', 5, 0, 5],
  ];
  const dbInfo = await db.query('SELECT current_database(), current_schema()');
  console.log('DB info:', dbInfo.rows);
  for (const r of rows) {
    const res = await db.query(
      `INSERT INTO public.breathing_exercises(title,description,inhale_seconds,hold_seconds,exhale_seconds)
       VALUES ($1,$2,$3,$4,$5)
       ON CONFLICT (title) DO NOTHING RETURNING id`,
      r
    );
    console.log(r[0], 'inserted?', res.rowCount > 0);
  }
  const count = await db.query('SELECT COUNT(*) FROM public.breathing_exercises');
  console.log('Total now:', count.rows[0].count);
  console.log('Seed OK');
  process.exit(0);
})().catch(e=>{console.error(e);process.exit(1);});