# @nickoshuo (Nicko Shuo): "Lesson: even the bouncer can't stand still" (How I make techno)
Arquivo enviado pelo Lucas em 27/11 (sem link nem métricas). 28 s · 720x1280 · 30 fps · em inglês · sem narração (só a música, "Osadki", 140 BPM, Alhena Records)
Arquivos: contact.jpg (1 quadro por segundo) · det.jpg (detalhes aos 5,5 s e 17,3 s)

## Roteiro (só texto na tela, digitado palavra por palavra no ritmo da música)
- 0-3 s: "You can't stand still to techno." / sublinha: "even the bouncer can't"
- 4-8 s: "It starts with **the hats.**" / "they take your shoulders"
- 9-12 s: "Then **the lead.**" / "it gets in your head"
- 12-16 s: "Then **the kick.**" / "and your feet are gone"
- 17-19 s: "One sound, one body part." → "GIVE EVERY BODY PART ITS OWN SOUND" / "shoulders · head · feet"
- 20-23 s: "What gets you **first?**" / "hats · lead · kick – tell me below"
- 24-28 s: "MAKE TECHNO WITH ME" / "follow to get in" + cartão final com o @ do Instagram (tela escurece)
- Ideia central: cada instrumento vira uma parte do corpo do segurança. Quem assiste VÊ a música.

## Visual
- Personagem 2D vetorial (estilo cartoon com sombra suave): segurança careca, barba, óculos escuros, ponto no ouvido,
  braços cruzados, ao lado de corda de VIP e porta com luz dourada. Fundo escuro e limpo, só um ponto de luz.
- Rótulos com linha tracejada apontando para o corpo: LEAD→head, HATS→shoulders, KICK→feet. O rótulo do instrumento
  que está tocando acende (fica branco); os outros ficam apagados. Ondas/traços aparecem na parte do corpo no batida.
- Anel dourado pulsa no chão a cada kick (movimento desde o quadro 0).
- Cabeçalho fixo tipo "ficha": LESSON / TRACK / LABEL / 140 BPM e o título da série "HOW I MAKE TECHNO".
- Barra de progresso fina embaixo do texto: mostra quanto falta do vídeo.
- Logo do Instagram + @ que muda de lugar a cada poucos segundos (marca d'água contra repost).

## Ritmo e câmera
- UMA tomada só, câmera parada, por 24 s (medir_cortes.py: 1 corte, o fade para o cartão final aos 24 s; 38% dos quadros
  quase parados). Funciona porque o movimento é a própria batida: algo pulsa a cada tempo e o texto avança no compasso.
- Texto entra palavra por palavra, sincronizado com a música (não com voz).

## O que aproveitar no @to.scale8
1. **CTA de múltipla escolha**: "What gets you first? hats · lead · kick – tell me below". Dar as opções na tela facilita
   o comentário (basta digitar uma palavra). Para nós: "Qual vem a seguir? 🍔 McDonald's · ☕ café · 🌶️ pimenta" e o
   mais votado vira episódio ("Vocês pediram").
2. **Rótulo com linha apontando para a parte do corpo, que acende quando é citado**: encaixa perfeito nos episódios de
   comida (ESTÔMAGO, FÍGADO, RINS, CÉREBRO com linha até o órgão no raio-x, aceso só quando a narração fala dele).
3. **Barra de progresso** fina na tela: sinaliza que o vídeo é curto e "quase acabando", ajuda a reter até o fim.
4. **Ficha fixa de série no topo** (LESSON/TRACK/BPM): identidade de série. Para nós: "E SE...? · EP 07 · COMIDA" +
   quantidade em destaque ("50 L"), visível o vídeo todo para quem chega no meio.
5. **Som = imagem**: cada evento sonoro tem um efeito visual no mesmo quadro (anel no chão no kick). Reforça nossa regra
   de "som como parte da linha do tempo".
6. Tomada única só funciona quando o personagem pulsa no ritmo o tempo todo. Para vídeo explicativo narrado, continua a regra de cortes a cada 2-5 s.
7. Duração curta (28 s) com uma ideia só. Lembrete: o Lucas definiu mínimo de 60 s para o nosso formato; não muda.

## Como reproduzir
- Tudo dá com o que temos (canvas 2D/three.js + mix.py). O personagem 2D de alta qualidade exigiria ilustração
  vetorial; o nosso low-poly 3D continua.
