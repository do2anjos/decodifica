const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve o jogo Pygame compilado pelo Pygbag
app.use('/', express.static(path.join(__dirname, 'build/web')));

// Se a gente precisar adicionar o Dashboard do Professor no futuro:
app.use('/dashboard', express.static(path.join(__dirname, 'dashboard')));

// Define os headers obrigatórios do Pygbag para WebAssembly funcionar corretamente
app.use((req, res, next) => {
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
    next();
});

app.listen(PORT, () => {
    console.log(`DECODIFICA: Servidor Híbrido rodando em http://localhost:${PORT}`);
    console.log(`Jogo Pygame (WASM) rodando em http://localhost:${PORT}/`);
});
