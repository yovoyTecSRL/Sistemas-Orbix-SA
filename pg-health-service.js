
// Simple microservicio Express para health-check de PostgreSQL
// npm install express pg dotenv

require('dotenv').config();
const express = require('express');
const { Client } = require('pg');

const app = express();
const PORT = process.env.PG_HEALTH_PORT || 3001;

app.get('/pg-health', async (_req, res) => {
const client = new Client({
host: process.env.PG_HOST || 'localhost',
port: process.env.PG_PORT || 5432,
user: process.env.PG_USER || 'postgres',
password: process.env.PG_PASSWORD || "",
database: process.env.PG_DATABASE || 'postgres',
});
try {
await client.connect();
await client.query('SELECT 1');
res.status(200).json({ status: 'ok' });
} catch (err) {
console.error('PostgreSQL health check failed:', err.message);
res.status(503).json({ status: 'error', error: err.message });
} finally {
await client.end();
}
});

app.listen(PORT, () => {
console.log('🛡️  PostgreSQL health service listening on port ' + PORT);
});
