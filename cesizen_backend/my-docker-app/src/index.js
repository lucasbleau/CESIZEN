const express = require('express');
require('dotenv').config();               // <-- added
const db = require('./db');               // <-- added

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => res.sendStatus(200));
app.get('/', (req, res) => res.send({ service: 'cesizen-api', status: 'ok' }));

// DB test endpoint
app.get('/db', async (req, res) => {
  try {
    const result = await db.query('SELECT 1 as ok');
    res.json({ db: 'ok', rows: result.rows });
  } catch (err) {
    console.error('DB error', err);
    res.status(500).json({ db: 'error', error: err.message });
  }
});

app.get('/api/example', (req, res) => {
  res.json({ message: 'Example response' });
});

// start server
const server = app.listen(port, () => {
  console.log(`CESIZEN API listening on port ${port}`);
});

// graceful shutdown
const shutDown = () => {
  console.log('Received shutdown signal, closing server...');
  server.close(() => {
    console.log('Server closed.');
    process.exit(0);
  });
  // Force close after timeout
  setTimeout(() => {
    console.error('Forcing shutdown.');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', shutDown);
process.on('SIGINT', shutDown);