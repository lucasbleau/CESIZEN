-- Tables de base
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS breathing_exercises (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  inhale_seconds INT NOT NULL,
  hold_seconds INT NOT NULL,
  exhale_seconds INT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_sessions (
  id SERIAL PRIMARY KEY,
  user_id INT,
  exercise_id INT,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  duration_seconds INT,
  notes TEXT
);