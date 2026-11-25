# Processo de produção — @to.scale8 (formato "E se...?" de engenharia em low-poly)

Referência pronta: `exemplo-ep03/` (vídeo publicado: videos/ep03-tirar-um-pilar-v2.mp4).
Leia o `pilar.html` inteiro antes de escrever uma cena nova: ele tem toda a infraestrutura
(câmeras, HUD, legendas sincronizadas, etiquetas, poeira, colapso, boneco de capacete).

## Formato (o que funcionou nas referências e foi aprovado pelo Lucas)
- 60 a 90 s, vertical 1080x1920, 30 fps.
- Gancho em pergunta "E se você ...?" com título grande na tela (palavra-chave amarela).
- Estrutura: pergunta → explica o "esqueleto" (como a coisa funciona) → faz a coisa absurda →
  consequência com números reais → piora (colapso/ruína visual quando fizer sentido) →
  "do jeito certo" (solução de engenharia) → pergunta ao público ("comenta").
- Boneco fixo: capacete amarelo, colete laranja, bigode (mascote do canal).
- Legenda de 1 a 3 palavras, caixa alta, branca com contorno preto, palavra-chave em amarelo.
- HUD no canto superior esquerdo (rótulo + número grande + subtítulo), etiquetas tipo pílula ✓/✗.
- Aviso no fim: "Ilustração. Mexer em estrutura só com projeto de engenheiro." (ou equivalente ao tema).
- Números: só valores de engenharia corretos ou ordens de grandeza marcadas com "~". Conferir na web.

## Narração (lições aprendidas — NÃO pular)
- Voz: Chatterbox Multilingual, language_id="pt", exaggeration=0.8, cfg_weight=0.3.
- Escrever o roteiro em frases CURTAS separadas por " | " no roteiro.json. O tts.py gera frase por
  frase, testa até 4 variações, escolhe a mais fiel (whisper) e coloca pausas reais:
  0,75 s depois de "?", 0,65 s depois de "...", 0,5 s depois de ".", e deixa 6% mais lento.
- Perguntas sempre terminando em "?" e separadas da frase seguinte.
- Frases de 1-2 palavras ("Dá.", "Tira ele.") costumam sair erradas: conferir o log e, se precisar,
  regenerar só aquele trecho: `python3 tts.py <id_do_trecho>`.
- Duração mínima do vídeo: 60 s. Se ficar curto, aumentar EXTRA (pausas dramáticas) no build_timeline.py.

## Passo a passo (em /home/claude/ep, com EP=/home/claude/ep)
1. `pip install --break-system-packages chatterbox-tts faster-whisper soundfile` (torch já vem);
   three.js: `npm install three@0.170.0`; Playwright fica em /opt/npm-tools e o Chrome em /usr/bin/google-chrome.
2. Escolher o próximo tema de `temas.md` que não esteja em `usados.md`. Pesquisar os números.
3. Escrever `roteiro.json` (ids de trecho + frases com " | ").
4. `python3 tts.py` (≈1,5 min por trecho em CPU) → `python3 build_timeline.py` → gera timeline.js/json e voz_total.wav.
5. Escrever `cena.html` (copiar a base do pilar.html; trocar modelo 3D, tomadas e HUD por trecho;
   tempos sempre ancorados em palavras com `wordTime(trecho, "palavra")`).
6. Prévia: `HTML=cena.html node render.mjs preview t1 t2 ...` e OLHAR os quadros (tomadas abertas com
   câmera a 18-22 m, nada cortado, câmera nunca dentro de objeto, título sem sobrepor rótulos).
7. `python3 mix.py` (trilha original + efeitos + voz) — ajustar os efeitos aos eventos do roteiro novo.
8. Render em 4 partes paralelas: `HTML=cena.html node render.mjs video seg/s0.mp4 0 T1 &` ... ; juntar com
   concat `-c copy`, somar `audio_final.wav` com `-map 0:v -map 1:a -c:v copy -c:a aac`.
9. Conferir contact sheet (1 quadro a cada ~2,5 s) e a duração.
10. Subir para `videos/epNN-slug.mp4` no repositório, adicionar o tema em `usados.md`.
11. Buffer (organização "My organization", canal TikTok @to.scale8): criar o post como RASCUNHO
    (saveToDraft: true), legenda com pergunta + hashtags (#engenharia #construcaocivil #obra #curiosidades),
    metadata.tiktok.isAiGenerated = true, thumbnailOffset num quadro forte.
    NÃO publicar: o Lucas aprova cada post no app do Buffer (Add to Queue / horário 19:00).
