const express = require('express');
const path = require('path');
const { createClient } = require('@libsql/client');
require('dotenv').config();

const app = express();
app.use(express.json());

// Define os headers obrigatórios do Pygbag para WebAssembly funcionar corretamente
// DEVE ficar ANTES das rotas e do express.static
app.use((req, res, next) => {
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    res.setHeader("Cross-Origin-Embedder-Policy", "credentialless");
    next();
});

const PORT = process.env.PORT || 3000;

// Configura o banco SQLite local ou Turso
const dbUrl = process.env.TURSO_URL || "file:ranking.db";
const dbAuthToken = process.env.TURSO_AUTH_TOKEN || undefined;

const db = createClient({
    url: dbUrl,
    authToken: dbAuthToken
});

// Inicializar a tabela de ranking e métricas
async function initDb() {
    try {
        await db.execute(`
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                pontos INTEGER NOT NULL,
                vidas INTEGER DEFAULT 0,
                insignias_d INTEGER DEFAULT 0,
                insignias_a INTEGER DEFAULT 0,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);
        await db.execute(`
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                chapter TEXT NOT NULL,
                found_bugs INTEGER NOT NULL,
                false_positives INTEGER NOT NULL,
                total_bugs INTEGER NOT NULL,
                recall_percent REAL NOT NULL,
                precision_percent REAL NOT NULL,
                score_gained INTEGER NOT NULL,
                time_spent_seconds REAL NOT NULL,
                m4_time_spent_seconds REAL DEFAULT 0,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `);
        console.log("Banco de dados SQLite/Turso conectado e tabelas verificadas/criadas!");
    } catch (e) {
        console.error("Erro ao inicializar banco de dados:", e);
    }
}
initDb();

// API: Salvar pontuação (POST /api/score)
app.post('/api/score', async (req, res) => {
    try {
        const { nome, pontos, vidas, insignias_d, insignias_a } = req.body;
        if (!nome || typeof pontos !== 'number') {
            return res.status(400).json({ error: "Nome e pontos são obrigatórios." });
        }
        await db.execute({
            sql: "INSERT INTO ranking (nome, pontos, vidas, insignias_d, insignias_a) VALUES (?, ?, ?, ?, ?)",
            args: [nome, pontos, vidas || 0, insignias_d || 0, insignias_a || 0]
        });
        res.json({ success: true });
    } catch (e) {
        console.error("Erro ao salvar score:", e);
        res.status(500).json({ error: "Erro interno do servidor" });
    }
});

// API: Retornar Leaderboard (GET /api/leaderboard)
app.get('/api/leaderboard', async (req, res) => {
    try {
        const result = await db.execute("SELECT nome, MAX(pontos) as pontos, vidas, insignias_d, insignias_a FROM ranking GROUP BY nome ORDER BY pontos DESC LIMIT 5");
        res.json(result.rows);
    } catch (e) {
        console.error("Erro ao buscar ranking:", e);
        res.status(500).json({ error: "Erro interno do servidor" });
    }
});

// API: Salvar métricas pedagógicas (POST /api/metrics)
app.post('/api/metrics', async (req, res) => {
    try {
        const { nome, chapter, found_bugs, false_positives, total_bugs, recall_percent, precision_percent, score_gained, time_spent_seconds, m4_time_spent_seconds } = req.body;
        if (!nome || !chapter) {
            return res.status(400).json({ error: "Nome e capítulo são obrigatórios." });
        }
        await db.execute({
            sql: `INSERT INTO metrics 
                 (nome, chapter, found_bugs, false_positives, total_bugs, recall_percent, precision_percent, score_gained, time_spent_seconds, m4_time_spent_seconds) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            args: [
                nome, chapter, 
                found_bugs || 0, false_positives || 0, total_bugs || 0, 
                recall_percent || 0, precision_percent || 0, score_gained || 0, 
                time_spent_seconds || 0, m4_time_spent_seconds || 0
            ]
        });
        res.json({ success: true });
    } catch (e) {
        console.error("Erro ao salvar métricas:", e);
        res.status(500).json({ error: "Erro interno do servidor" });
    }
});

// Serve o jogo Pygame compilado pelo Pygbag
app.use('/', express.static(path.join(__dirname, 'game_source', 'build', 'web')));



app.listen(PORT, () => {
    console.log(`DECODIFICA: Servidor Híbrido rodando em http://localhost:${PORT}`);
    console.log(`Jogo Pygame (WASM) rodando em http://localhost:${PORT}/`);
});
