# Arquitetura do Projeto: DECODIFICA - Guardiões das Lendas

Este documento descreve a arquitetura técnica, as tecnologias envolvidas e o fluxo de dados do projeto **DECODIFICA**.

## 1. Visão Geral

O projeto é dividido em duas partes principais:
1. **Frontend (Jogo)**: Uma aplicação interativa e gamificada construída em Python usando a biblioteca Pygame. O jogo roda diretamente no navegador dos alunos através do **Pygbag** (WebAssembly).
2. **Backend (Servidor e Banco de Dados)**: Uma API em Node.js com Express e SQLite para coletar as métricas de desempenho dos alunos e exibi-las em um ranking.

---

## 2. Frontend: Jogo em Pygame (WebAssembly)

O núcleo interativo do aluno reside de forma modularizada nos arquivos `main.py`, `ui.py` e `data.py`. O ciclo do jogo é assíncrono para garantir total compatibilidade com o Pygbag no navegador.

### 2.1 Tecnologias
- **Linguagem**: Python 3.12
- **Engine Gráfica**: Pygame (CE / Web)
- **Compilador/Packager Web**: Pygbag 0.9.3 (Converte Python para WebAssembly)

### 2.2 Máquina de Estados (Game States)
A progressão do jogo é guiada por uma variável global `game_state`. As transições cobrem todos os fluxos do jogo:
- `MENU` e `NAME_INPUT`: Registro do jogador e tela inicial.
- `CINEMATIC`: Contextualização da história (lore do vírus e o pergaminho).
- `ROADMAP` e `GALERIA`: Mapa das Lendas (trilha desbloqueável) e Galeria de Arte (recompensas visuais por completar as lendas).
- `CHAPTER_INTRO`: Tela de missão, informando o nível de dificuldade antes do início do capítulo.
- `MECANICA_1` a `MECANICA_5`: Ciclo principal de gameplay (Decomposição, Abstração, Algoritmo, Síntese do Guardião e Lenda Restaurada).
- `CREATOR_WRITE` e `CREATOR_CORRUPT`: O "Modo Mestre", onde o aluno vira o autor, escreve sua lenda e corrompe palavras intencionalmente.
- `GAME_OVER` e `FIM`: Telas de desfecho do capítulo (derrota por perda de vidas ou conclusão com submissão de pontuação final ao servidor).
- `RANKING`: Hall dos Guardiões, puxando os dados em tempo real do banco de dados via API.

**Transições**: Implementamos delays e estados intermediários (ex: `MECANICA_1_WIN`) para permitir que o jogador visualize o feedback (cores e animações) antes de avançar para o próximo desafio.

### 2.3 Interface e UX
- **Resolução Nativa**: 1280x720 (16:9).
- **Temática Visual**: Amazônica (Verde Floresta, Dourado do Guaraná, Laranja Tucano, com alertas de perigo em Vermelho).
- **Efeitos Especiais**: Partículas independentes (vagalumes flutuantes, animações no cristal do guardião).
- **Preloader**: Template customizado (`custom.tmpl`) no Pygbag para apresentar o jogo imersivamente antes do download concluir.

---

## 3. Backend: Servidor e API (Node.js)

O arquivo `server.js` hospeda a infraestrutura de backend. Sua função dupla é servir os arquivos estáticos compilados pelo Pygbag e prover as rotas da API REST conectadas a um banco de dados persistente.

### 3.1 Tecnologias
- **Linguagem**: JavaScript (Node.js)
- **Framework**: Express.js
- **Banco de Dados**: SQLite (`better-sqlite3`)

### 3.2 Responsabilidades
- **Hospedagem Estática**: A rota `/` aponta para a pasta `build/web/`, servindo o pacote `decodifica.apk`, `index.html` e o runtime do Pygbag.
- **Coleta de Métricas (Implementado)**: A rota `/api/score` recebe requisições do jogo e salva o Score, Insígnias e Vidas no arquivo `decodifica.db`.
- **Leaderboard (Implementado)**: A rota `/api/leaderboard` retorna o ranking ordenado de todos os jogadores (Hall dos Guardiões).

---

## 4. Integração Frontend ⇄ Backend

Como o Pygame roda isolado no navegador via WebAssembly, toda a comunicação com o servidor Node.js acontece via chamadas HTTP assíncronas utilizando a integração de JavaScript embutida no Pygbag.

### 4.1 O Fluxo de Dados
1. O aluno joga o DECODIFICA. Ao atingir o final da jornada (Tela de FIM), o código Python empacota o desempenho num JSON.
2. Usando o módulo `js` nativo do Pygbag (`import js`), o Python aciona a API nativa do navegador executando `js.fetch("/api/score", ...)`.
3. O Node.js recebe o `POST` contendo os dados do aluno e os consolida no SQLite.
4. Quando o aluno ou professor clica em "Ver Ranking", o Python faz um `fetch("/api/leaderboard")` e renderiza os dados formatados do banco diretamente na tela do jogo.

---

## 5. Estrutura de Diretórios (Resumo)
```text
DECODIFICA/
│
├── game_source/         # Diretório principal do jogo
│   ├── main.py          # Lógica de estados e renderização do Pygame (Frontend)
│   ├── ui.py            # Componentes visuais (Botões, Modais, HUD)
│   ├── data.py          # Dados locais (Textos, regras, configurações dos capítulos)
│   └── custom.tmpl      # Template modificado para a tela de loading do Pygbag
│
├── server.js            # Lógica do Express/Node.js e banco de dados (Backend)
├── decodifica.db        # Banco de dados SQLite persistente gerado pelo Node
├── package.json         # Dependências do Node (express, better-sqlite3)
│
├── build/web/           # Código compilado pelo Pygbag (HTML/JS/WASM)
│   ├── index.html       # Arquivo de entrada do jogo no browser
│   └── decodifica.apk   # Assets e scripts empacotados pelo Pygbag
│
└── DOC/                 # Documentação técnica e metodológica do projeto
    ├── Arquitetura.md   # Este documento
    ├── REC/             # Concepção, planejamento e Level Design
    └── GUIA/            # Guias de processamento e validação cognitiva
```

---

## 6. Próximos Passos (Evolução)
- Elaborar e redigir novos capítulos (lendas adicionais) para ampliar o banco de dados de missões em `data.py`.
- Realizar sessões de playtest com alunos do Ensino Fundamental para refinar a curva de dificuldade e as taxas de recall.
- (Opcional) Desenvolver um painel administrativo protegido por senha na web para que professores possam extrair os relatórios em CSV diretamente do banco `decodifica.db`.
