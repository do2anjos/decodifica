# 🎮 Roteiro de Apresentação: DECODIFICA - Guardiões das Lendas da Amazônia

Este é um guia estruturado para você apresentar o seu jogo com segurança, cobrindo desde a ideia pedagógica até a arquitetura técnica que faz ele funcionar.

---

## 1. O que é o DECODIFICA? (O Pitch / Resumo)
> *"O DECODIFICA é um jogo educacional digital voltado para alunos do 4º ano do Ensino Fundamental. O objetivo principal dele é unir o ensino de **Ortografia da Língua Portuguesa** com os pilares do **Pensamento Computacional**."*

- **O Cenário:** O jogo utiliza as ricas **Lendas Amazônicas** (Guaraná, Mapinguari, Cobra Grande e Vitória-Régia).
- **O Desafio:** As lendas foram corrompidas por "bugs" (erros ortográficos e de lógica narrativa). O jogador atua como um Guardião que precisa restaurar essas histórias usando o pensamento lógico.

---

## 2. A Inovação Pedagógica (Português + Computação)
A grande sacada do DECODIFICA é que ele não apenas "ensina a escrever certo". Ele ensina a criança a **pensar como um programador para resolver problemas textuais**. 

O jogo faz isso traduzindo os 4 pilares do Pensamento Computacional em ações reais no jogo:

1. **Decomposição:** Pegar um texto grande e dividi-lo em pedaços menores (parágrafos) para entender o começo, meio e fim.
2. **Abstração:** Varrer o texto ignorando as palavras certas e filtrando apenas as palavras "estranhas" (os bugs ortográficos).
3. **Algoritmo:** Seguir uma sequência exata de passos para revisão de um texto (Ler ➔ Identificar erro ➔ Corrigir).
4. **Reconhecimento de Padrões:** Perceber qual foi a regra gramatical que mais falhou naquele texto (ex: confundir `CH` com `X`).

---

## 3. Alinhamento com a BNCC (Fundamentação Pedagógica)
O jogo não é apenas um "passatempo educativo", ele atende diretamente às competências e habilidades exigidas pela Base Nacional Comum Curricular para o 4º Ano:

* **Ortografia e Gramática (EF04LP01 / EF04LP05):** O aluno é ativamente testado na correção de correspondências fonema/grafema como `S/Z`, `CH/X`, `C/S` e `G/J`.
* **Produção e Coesão Textual (EF04LP02):** Ao organizar os parágrafos soltos da lenda, a criança desenvolve a lógica da narrativa (introdução, desenvolvimento e desfecho).
* **Fluência Leitora (EF15LP10):** A mecânica de "Caça ao Bug" força o que chamamos de *leitura com propósito*. A criança relê o texto ativamente procurando falhas, estimulando a memória fotográfica das palavras.
* **Competência Geral 5 da BNCC:** Utilização do Pensamento Computacional como ferramenta prática e reflexiva de tecnologia digital.

---

## 4. As 5 Mecânicas de Jogo (O Gameplay)
Para cada lenda, o jogador passa por um fluxo exato de 5 mecânicas:

* **Mecânica 1: Reorganização Narrativa (Drag & Drop)**
  * A lenda está embaralhada. O aluno precisa ler e arrastar os parágrafos para a ordem lógica (aplicando Decomposição).
* **Mecânica 2: Caça ao Bug**
  * Com o texto na ordem, o aluno deve clicar nas palavras que estão escritas erradas (aplicando Abstração e atenção seletiva).
* **Mecânica 3: Correção Ortográfica**
  * O jogador precisa escolher a forma certa da palavra ou digitá-la corretamente (Algoritmo de correção).
* **Mecânica 4: Mapa de Padrões**
  * O jogo pergunta qual foi o tipo de erro mais comum da fase (ex: `S` com som de `Z`), gerando metacognição.
* **Mecânica 5: A Recompensa (Síntese)**
  * O texto é exibido limpo, corrigido, e animado, recompensando o jogador com a lenda verdadeira e os pontos.

---

## 5. Progressão: Como o jogo evolui?
O jogo foi planejado com um **Level Design Progressivo** para não frustrar o aluno:
- **Capítulo 1 (Guaraná) - Nível Aprendiz:** Dá dicas visuais da ordem dos parágrafos, poucos bugs, usa múltipla escolha.
- **Capítulo 2 (Mapinguari) - Nível Explorador:** Tira as dicas visuais de posição. Introduz "falsos suspeitos" (palavras difíceis, mas que estão escritas certas) para forçar a atenção.
- **Capítulo 3 (Cobra Grande) - Nível Guardião:** Textos mais longos, mais erros, e o jogador passa a ter que **digitar** a palavra certa em vez de só clicar nas opções.
- **Capítulo 4 (Vitória-Régia) - Nível Mestre:** O teste final de todas as habilidades combinadas.

---

## 6. Arquitetura e Tecnologia (Bastidores)
Se te perguntarem "como o jogo foi feito" ou "o que roda por baixo", aqui está o segredo da tecnologia do DECODIFICA:

* **Front-end / O Jogo (Python & Pygame):** 
  * A engine visual inteira foi programada em Python puro usando a biblioteca Pygame.
* **A Mágica da Web (Pygbag & WebAssembly):**
  * Como fazer um jogo Python rodar no navegador do celular ou PC? Usando a tecnologia **WebAssembly (WASM)** via **Pygbag**. Ele emula e traduz o código Python direto para o navegador em tempo real, sem precisar instalar nada.
* **Back-end e APIs (Node.js & Express):**
  * Para o ranking funcionar em tempo real entre todos os jogadores, existe um servidor em **Node.js** rodando nos bastidores. O jogo em WebAssembly faz requisições (`fetch` HTTP) para enviar os pontos para esse servidor de forma híbrida.
* **Banco de Dados (SQLite / Turso):**
  * O servidor salva os pontos e métricas num banco de dados **SQLite**. Para o Ranking (*Hall dos Guardiões*), a consulta exibe apenas a melhor performance de cada aluno, descartando os registros intermediários automaticamente, gerando uma tabela de classificação justa.

---

## 7. O Sistema de Ranking (A Dinâmica Global)
A forma de avaliar o desempenho dos jogadores ocorre por meio da gamificação:
* O sistema não pune o erro severamente, mas recompensa a maestria!
* O aluno joga até o final e todo o seu esforço é consolidado no **Hall dos Guardiões**.
* O ranking em tempo real estimula a repetição (replayability). A criança joga novamente tentando achar todos os bugs mais rápido e usar menos dicas para conseguir ultrapassar a própria pontuação ou a dos colegas no mural das lendas.

---
> [!TIP]
> **Dica para Apresentação:**
> Quando for falar, foque em como o DECODIFICA resolve o tédio de preencher "fichas de caligrafia e ortografia" colocando a criança numa posição ativa: a de **caçador de bugs**, onde cada vitória se converte em pontos no mural global!

