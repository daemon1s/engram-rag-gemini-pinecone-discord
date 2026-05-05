import { Pool, QueryResultRow } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: parseInt(process.env.DB_PORT || '5432'),
  ssl: false
});

export const db = {
  query: <T extends QueryResultRow = any>(text: string, params?: any[]) => pool.query<T>(text, params),
};
