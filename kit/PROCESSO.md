# Processo de produção — @to.scale8 (formato "E se...?" em low-poly: comida exagerada, absurdo geral e engenharia de vez em quando)

Referências prontas: `exemplo-ep03/` (engenharia, casa), `exemplo-ep04/` (comida: mesa, pilha de
picanha instanciada, barriga que incha, raio-x do estômago, convidados, etapas 1 hora/1 dia/1 semana) e
`exemplo-ep05/` (absurdo: multidão instanciada de ~3 mil bonecos + "tapete" texturizado para tomadas aéreas,
segunda cena com planeta low-poly, contagem 3-2-1, pulo em câmera lenta, sismógrafo e engarrafamento no HUD).
Referência original: `exemplo-ep03/` (vídeo publicado: videos/ep03-tirar-um-pilar-v2.mp4).
Leia o `pilar.html` inteiro antes de escrever uma cena nova: ele tem toda a infraestrutura
(câmeras, HUD, legendas sincronizadas, etiquetas, poeira, colapso, boneco de capacete).

## Foco do canal (definido pelo Lucas em 24/11)
- Absurdo e exagero que prende atenção: misturar comida exagerada, absurdo geral e, de vez em quando, engenharia.
- Manter diversidade: nunca dois temas seguidos da mesma categoria (ver temas.md).
- O exemplo do pilar mostra o ESTILO (estrutura, narração, legendas, colapso); o cenário 3D muda conforme o tema
  (mesa com comida e boneco, cidade, planeta, etc.). Boneco mascote sempre presente.

## Formato (o que funcionou nas referências e foi aprovado pelo Lucas)
- 60 a 90 s, vertical 1080x1920, 30 fps.
- Gancho em pergunta "E se você ...?" com título grande na tela (palavra-chave amarela).
- Estrutura: pergunta → explica como a coisa funciona → faz a coisa absurda → consequência com números
  reais (para comida: 1 hora / 1 dia / 1 semana) → piora visual (colapso, explosão, inchaço...) →
  virada/curiosidade final → pergunta ao público ("comenta qual exagero vem a seguir").
- Boneco fixo: capacete amarelo, colete laranja, bigode (mascote do canal).
- Legenda de 1 a 3 palavras, caixa alta, branca com contorno preto, palavra-chave em amarelo.
- HUD no canto superior esquerdo (rótulo + número grande + subtítulo), etiquetas tipo pílula ✓/✗.
- Aviso no fim adequado ao tema: engenharia "Ilustração. Mexer em estrutura só com projeto de engenheiro.";
  comida/bebida "Ilustração exagerada. Não tente isso."; absurdo físico: "Simulação hipotética".
- Números: só valores de engenharia corretos ou ordens de grandeza marcadas com "~". Conferir na web.

## Narração (lições aprendidas — NÃO pular)
- Voz: Chatterbox Multilingual, language_id="pt", exaggeration=0.8, cfg_weight=0.3.
- Escrever o roteiro em frases CURTAS separadas por " | " no roteiro.json. O tts.py gera frase por
  frase, testa até 4 variações, escolhe a mais fiel (whisper) e coloca pausas reais:
  0,75 s depois de "?", 0,65 s depois de "...", 0,5 s depois de ".", e deixa 6% mais lento.
- Perguntas sempre terminando em "?" e separadas da frase seguinte.
- Frases de 1-2 palavras ("Dá.", "Tira ele.") costumam sair erradas: conferir o log e, se precisar,
  regenerar só aquele trecho: `python3 tts.py <id_do_trecho>`.
- Frases curtas de aviso também falham ("Não tente isso." saiu "Não tem cheese"): escrever o aviso
  falado numa frase mais longa ("Sério, por favor, não tente fazer isso.") e conferir a similaridade no log.
- MEMÓRIA (lição do ep04): a máquina tem ~8 GB e o tts.py vaza memória; rodar todos os trechos num só
  processo foi morto por OOM no meio. Rodar UM trecho por processo, em sequência e desacoplado do shell:
  `for s in hook escala ...; do python3 tts.py $s >> tts.log 2>&1; done` (script com setsid nohup).
- Duração mínima do vídeo: 60 s. Se ficar curto, aumentar EXTRA (pausas dramáticas) no build_timeline.py.

## Passo a passo (em /home/claude/ep, com EP=/home/claude/ep)
1. `pip install --break-system-packages chatterbox-tts faster-whisper soundfile` (torch já vem);
   three.js: `npm install three@0.170.0`; Playwright fica em /opt/npm-tools e o Chrome em /usr/bin/google-chrome.
2. Escolher o próximo tema de `temas.md` que não esteja em `usados.md`. Pesquisar os números.
   ANTES de escolher: `git pull` e conferir `usados.md` E os posts recentes no Buffer (list_posts). Em 25/11 duas
   execuções rodaram em paralelo e as duas fizeram o ep04 (picanha); a segunda perdeu ~1h30 de TTS/render.
   Repetir a conferência antes de subir o vídeo: se o tema já apareceu no main, não subir duplicado.
3. Escrever `roteiro.json` (ids de trecho + frases com " | ").
4. `python3 tts.py` (≈1,5 min por trecho em CPU) → `python3 build_timeline.py` → gera timeline.js/json e voz_total.wav.
5. Escrever `cena.html` (copiar a base do pilar.html; trocar modelo 3D, tomadas e HUD por trecho;
   tempos sempre ancorados em palavras com `wordTime(trecho, "palavra")`).
6. Prévia: `HTML=cena.html node render.mjs preview t1 t2 ...` e OLHAR os quadros (tomadas abertas com
   câmera a 18-22 m, nada cortado, câmera nunca dentro de objeto, título sem sobrepor rótulos).
7. `python3 mix.py` (trilha original + efeitos + voz) — ajustar os efeitos aos eventos do roteiro novo.
8. Render em 4 partes paralelas: `HTML=cena.html node render.mjs video seg/s0.mp4 0 T1 &` ... ; juntar com
   concat `-c copy`, somar `audio_final.wav` com `-map 0:v -map 1:a -c:v copy -c:a aac`.
9. Prévias: montar uma grade (PIL) com 12-18 quadros e olhar tudo de uma vez; checar se pílulas/rótulos
   não cobrem a cabeça do boneco e se `wordTime` não pega a palavra errada (ex.: "três" aparece duas vezes).
10. Conferir contact sheet (1 quadro a cada ~2,5 s) e a duração.
11. Subir para `videos/epNN-slug.mp4` no repositório, adicionar o tema em `usados.md`.
12. Buffer (organização "My organization", canal TikTok @to.scale8): desde 25/11 o Lucas aprovou publicação
    AUTOMÁTICA diária, desde 26/11 às 17:00 (Brasília; antes era 19:00). Criar o post agendado: mode "customScheduled", dueAt "AAAA-MM-DDT17:00:00-03:00",
    saveToDraft false, legenda com pergunta + 4 a 6 hashtags do tema (#curiosidades #ese #exagero + específicas),
    metadata.tiktok.isAiGenerated = true, thumbnailOffset num quadro forte. Se já passou das 17:00, "shareNow".
    Conferir com get_post que ficou "scheduled" sem erro. Se o vídeo não estiver bom, NÃO agendar e avisar o Lucas.

## Lições do ep05 (26/11)
- INSTALAÇÃO: o `pip install chatterbox-tts` baixa o torch completo com CUDA (~3 GB, ~20 min a 4 MB/s; o
  download.pytorch.org é bloqueado pelo proxy). Disparar o pip em segundo plano no PRIMEIRO minuto e escrever
  roteiro/cena enquanto baixa. `npm install three` pode rodar em paralelo, separado.
- Máquina com 2 CPUs: render a ~1,3 quadro/s por processo; 3 partes em paralelo fazem 90 s de vídeo em ~10 min.
- InstancedMesh com instâncias longe da origem SOME (frustum culling usa a geometria original):
  sempre `mesh.frustumCulled = false` em multidões, carros, pilhas etc.
- Tomadas aéreas (câmera a 200-300 m) com `camera.near = 0.05` dão z-fighting entre planos próximos
  (chão x tapete): usar near 0,5 ou mais.
- Aceitar similaridade 0,86 deixou passar palavra errada ("pessoas" saiu "péssulas"). Se o log mostrar palavra
  estranha, regenerar o trecho com limite mais alto (cópia do tts.py com `sim >= 0.97`).
- O valor-chave revelado na última palavra do trecho (ex.: "próton", "átomo") ficava <1 s na tela: dar EXTRA
  de 1,3-1,4 s nesses trechos no build_timeline.py.
- `rm preview/*` é bloqueado pela checagem de segurança: o render.mjs agora aceita `PD=pasta` para gravar
  as prévias numa pasta nova a cada rodada.
- Render sai com ~20 Mbps (crf 18); ao juntar com o áudio, reencodar com `-crf 23 -maxrate 5M -bufsize 10M`
  (90 s ≈ 33 MB) para ficar bem abaixo do limite de 100 MB do GitHub.
