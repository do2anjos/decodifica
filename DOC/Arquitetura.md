# Arquitetura do Projeto: DECODIFICA - Guardiões das Lendas

Este documento descreve a arquitetura técnica, as tecnologias envolvidas e o fluxo de dados do projeto **DECODIFICA**.

## 1. Visão Geral

O projeto é dividido em duas partes principais:
1. **Frontend (Jogo)**: Uma aplicação interativa e gamificada construída em Python usando a biblioteca Pygame. O jogo roda diretamente no navegador dos alunos através do **Pygbag** (WebAssembly).
2. **Backend (Dashboard do Professor)**: Uma API em Node.js com Express para coletar as métricas de desempenho dos alunos e exibi-las para os professores.

---

## 2. Frontend: Jogo em Pygame (WebAssembly)

O núcleo interativo do aluno reside no arquivo `main.py`. O ciclo do jogo é assíncrono para garantir total compatibilidade com o Pygbag no navegador.

### 2.1 Tecnologias
- **Linguagem**: Python 3.12
- **Engine Gráfica**: Pygame (CE / Web)
- **Compilador/Packager Web**: Pygbag 0.9.3 (Converte Python para WebAssembly)

### 2.2 Máquina de Estados (Game States)
A progressão do jogo é guiada por uma variável global `game_state`. As transições são as seguintes:
- `MENU`: Tela inicial de boas-vindas.
- `INTRO`: Contextualização da história (pergaminho).
- `ROADMAP`: Trilha de capítulos. (Ex: Capítulo 1 - Lenda do Guaraná).
- `MECANICA_1` (Decomposição): Drag & Drop de parágrafos para reconstruir a narrativa.
- `MECANICA_2` (Abstração): Caça aos erros ortográficos (clique para marcar).
- `MECANICA_3` (Algoritmo): Correção de cada palavra errada através de modais interativos.
- `MECANICA_4` (Reconhecimento de Padrão): Análise final do tipo de erro mais frequente.
- `FIM`: Tela de conclusão com pontuação final.

**Transições**: Implementamos delays (usando `message_timer`) e estados intermediários (`_WIN`) para permitir que o jogador visualize o feedback antes de avançar bruscamente para o próximo desafio.

### 2.3 Interface e UX
- **Resolução Nativa**: 1280x720 (16:9).
- **Temática Visual**: Amazônica (Verde Floresta, Dourado do Guaraná, Laranja Tucano).
- **Efeitos Especiais**: Partículas independentes (vagalumes flutuantes, chuva de confetes) processadas e renderizadas no loop principal.
- **Preloader**: Template customizado (`custom.tmpl`) no Pygbag para apresentar o jogo imersivamente antes do download do WebAssembly concluir.

---

## 3. Backend: Servidor e API (Node.js)

O arquivo `server.js` hospeda a infraestrutura de backend. Sua função dupla é servir os arquivos estáticos compilados pelo Pygbag e prover as rotas da API REST.

### 3.1 Tecnologias
- **Linguagem**: JavaScript (Node.js)
- **Framework**: Express.js
- **Banco de Dados (Planejado)**: SQLite, MongoDB, ou armazenamento em memória (para prototipagem rápida).

### 3.2 Responsabilidades
- **Hospedagem Estática**: A rota `/` aponta para a pasta `build/web/`, servindo o pacote `decodifica.apk`, `index.html` e o runtime do Pygbag.
- **Coleta de Métricas**: (Planejado) Receber chamadas de telemetria do Python para salvar métricas do jogador.
- **Dashboard Web**: (Planejado) Páginas HTML/Dashboard servidas para os professores visualizarem tabelas de acertos, tempo gasto e ranking dos alunos.

---

## 4. Integração Frontend ⇄ Backend

Como o Pygame roda isolado no navegador via WebAssembly, toda a comunicação com o servidor Node.js acontecerá via chamadas HTTP (REST API).

### 4.1 O Fluxo de Dados
1. O aluno joga o DECODIFICA. Cada vez que termina uma lenda ou corrige uma palavra, o código Python dispara uma chamada assíncrona.
2. A chamada é feita usando a biblioteca `platform` embutida no Pygbag (que traduz chamadas de rede do Python para a API `fetch()` nativa do JavaScript no navegador).
3. O Node.js recebe um `POST` com os dados: `ID do Aluno`, `Capítulo`, `Pontos`, `Erros`.
4. O Professor acessa `http://localhost:3000/dashboard`, que consulta o Node.js e renderiza o progresso da turma.

---

## 5. Estrutura de Diretórios (Resumo)
```text
DECODIFICA/
│
├── main.py              # Lógica principal do Pygame (Frontend/Jogo)
├── server.js            # Lógica do Express/Node.js (Backend/Dashboard)
├── package.json         # Dependências do Node (express, etc)
├── custom.tmpl          # Template modificado para a tela de loading do Pygbag
│
├── build/web/           # Código compilado pelo Pygbag (HTML/JS/WASM)
│   ├── index.html       # Arquivo de entrada do jogo no browser
│   └── decodifica.apk   # Assets e scripts empacotados pelo Pygbag
│
└── DOC/                 # Documentação técnica e de negócio do projeto
    └── Arquitetura.md   # Este documento
```

---

## 6. Próximos Passos (Evolução)
- Implementar as chamadas assíncronas de `fetch()` no Python para postar as vitórias.
- Construir a interface do **Dashboard do Professor** usando HTML/CSS servido pelo Node.js.
- Criar a funcionalidade para destrancar os próximos Capítulos (Mapinguari, etc) baseados no desempenho.
