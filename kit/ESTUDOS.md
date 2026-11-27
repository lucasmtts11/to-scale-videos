# Regras tiradas dos estudos (leitura obrigatória antes de cada episódio)

Fontes: os 8 estudos de vídeos de referência (documentos do projeto AUTOMACOES no claude.ai, em
`CLAUDE/canal tiktok/estudos/*/estudo.md`), a análise de quadros do vídeo da Bitmap e os artigos que o Lucas
mandou em 25/11 (Matheus Celtic, jaffa/Virlo, eigen/seek(t)). Quando uma regra daqui conflitar com feedback
direto do Lucas, vale o feedback do Lucas (ex.: ele pediu pausas naturais na narração, então não usamos a
narração "sem pausa nenhuma" das referências).

## 1. Gancho (0 a 3 s)
- Algo já se mexe nos quadros 0 a 3. Nunca abrir com tela parada (o ep03 perdeu a maior parte do público em 4 s).
- Pergunta "E se...?" na tela em letras grandes, palavra-chave amarela, e o mascote já reagindo.
- Tema ligado à vida de quem assiste rende mais que absurdo distante ("sua casa", "seu churrasco", "o Brasil").
  É hipótese do artigo do Celtic; conferir com as métricas.

## 2. Roteiro
- Estrutura: pergunta → como funciona → faz a coisa absurda → consequência com números → piora visual → virada → pergunta ao público.
- Mostrar o que dá errado ANTES da explicação/solução (@desmontandoomundo: chuva e deslizamento antes da drenagem).
- Escolha com número e contador deixa o vídeo legível para quem chega no meio (@vidadabia: HUD fixo "R$ 1.410 / R$ 1.500"; @itsshukee: "33/100").
- Cartão de dado com FONTE quando o número vem de órgão oficial ("ESTIMATIVA IBGE 2025", "TACO"): dá credibilidade (@animaet).
- Fecho com pergunta direta que vira pauta: "Qual exagero vem a seguir? Comenta". Quando um tema vier dos comentários,
  abrir o episódio com "Vocês pediram: ..." (@vidadabia, @animaet).
- De vez em quando, gancho de PARTE 2 no fim ("e se fossem 100?"), que faz seguir o perfil (@itsshukee). Só quando
  a parte 2 for realmente produzida no dia seguinte.
- Humor: exagero visual e onomatopeias na tela (BUUURP!, TUUUM!, BIIII!). Narrador com personalidade (@dwxzmusic).
  Sem palavrão.
- Legenda do post com ressalva curta ("Ilustração exagerada", "Simulação hipotética"): protege contra crítica e gera comentário.
- Originalidade: copiar o MOLDE, nunca o conteúdo. Variar a estrutura de vez em quando (ordem das partes, tipo de
  virada, cenário), não só trocar o tema; vídeo em série idêntico todo dia é tratado como repetitivo pelas plataformas.

## 3. Ritmo e câmera
- Troca de tomada a cada 2 a 5 s, de preferência no início de uma frase da narração (@mildly.elsewhere corta a cada 2-3 s;
  @desmontandoomundo a cada 4-7 s). Um trecho de 10 s precisa de 2 a 4 tomadas, não uma só.
- Câmera sempre em movimento lento (aproximação, travelling, órbita). Nada totalmente parado.
- Troca de cena com corte seco, no pico de uma fala ou de um som. Suavidade fica no movimento dentro da cena.

## 4. Movimento (análise de quadros da Bitmap)
- Duração de cada movimento: 12 a 20 quadros (0,4 a 0,7 s). Acelera em 1/3 do tempo e desacelera em 2/3 (ease-out mais longo).
- Objeto que "chega" (mascote, pilar, pilha, porta-aviões) usa mola com 5 a 15% de overshoot. Texto sem overshoot.
- Escalonar elementos 4 a 8 quadros entre si; nunca mover tudo junto.
- Depois de cada ação, segurar 6 a 10 quadros parado.
- Mascote entra com squash/stretch e trajetória em arco.

## 5. Narração e legenda
- Voz: Chatterbox com a voz de referência do canal (`kit/voz_referencia.wav`, o tts.py usa sozinho). Sem ela, o timbre
  muda de episódio para episódio.
- Pausas: as do tts.py (0,5 a 0,75 s), que o Lucas aprovou. Não alongar além disso fora dos EXTRAs dramáticos.
- Legenda de 1 a 3 palavras, caixa alta, branca com contorno preto, palavra-chave amarela, centro-baixo.
- Som como parte da linha do tempo: cada evento visual forte (impacto, contagem, buzina) tem efeito no mesmo quadro.

## 6. Conferência antes de publicar
- Contact sheet (1 quadro a cada ~2,5 s) + quadros antes e depois de cada troca de cena.
- Checar: nada cortado; texto não cobre rosto do mascote nem o objeto principal; números da HUD conferem com a fala;
  valor-chave fica pelo menos 1,5 s na tela; legenda não sobrepõe HUD.
- Só valores conferidos na web ou ordens de grandeza com "~".

## 7. Medição (ainda não implantado, depende do Lucas)
- Critério para escolher formato e tema: vezes a média do próprio canal, nunca views brutas (Celtic + Virlo).
- Fechamento semanal (findings.md): para cada vídeo, base, desempenho contra a média e uma mudança; vira regra
  depois de 3 repetições.

## Medições nos vídeos (26/11) — referências x nossos episódios
Medido com diferença de quadros (fps 30, 72x128): troca de tomada = pico de diferença; "parado" = quadro quase igual ao anterior.

| vídeo | tomada média | maior tomada | quadros parados | movimento mediano |
|---|---|---|---|---|
| @animaet (Ilhas Faroé, 125 s) | 1,7 s | 4,8 s | 11% | 1,6 |
| @dwxzmusic (casa impossível, 141 s) | 3,0 s | 6,0 s | 7% | 1,3 |
| @itsshukee (100 gênios, 45 s) | 3,8 s | 6,7 s | 24% | 0,5 |
| @mildly.elsewhere (dique seco, 70 s) | câmera sempre em movimento (corte não detectável) | — | 21% | 4,5 |
| **nosso ep04 (picanha)** | **6,4 s** | **11,6 s** | **58%** | **0,2** |
| **nosso ep05 v1 (Brasil pulando)** | **7,8 s** | **18,1 s** | **43%** | **0,4** |
| **nosso ep05 v2 (refeito com as regras)** | **3,8 s** | **11,6 s** | **19%** | **0,8** |

Conclusões:
- Nossas tomadas duram o dobro ou o triplo das referências e metade dos quadros fica praticamente parada.
  Regra: tomada média de 2,5 a 4 s, nenhuma acima de 5 s; câmera com deslocamento visível em toda tomada
  (no kit: função `cam()` do exemplo-ep05 v2, que corta no início de cada frase e divide trechos longos).
- Pausas na fala: @dwxzmusic tem ~9 pausas por minuto (média 0,43 s), parecido com as nossas (~8/min, 0,55 s).
  @animaet e @mildly quase não pausam. As pausas que o Lucas pediu estão dentro do que funciona.
- Primeiro corte: as referências cortam entre 3 e 7 s; o ep05 v1 só cortava aos 18 s.

## Checklist rápido (marcar no fim de cada episódio)
- [ ] Movimento nos quadros 0 a 3 e pergunta na tela
- [ ] Algo dá errado antes da explicação
- [ ] Pelo menos um contador ou cartão de dado (com fonte quando houver)
- [ ] Tomadas de 2 a 5 s (média 2,5 a 4 s), corte seco no começo da frase; medir com kit/medir_cortes.py
- [ ] Movimentos com ease-out, mola nos objetos que chegam, elementos escalonados
- [ ] Voz de referência carregada (log do tts.py mostra "voz de referência: ...wav")
- [ ] Valor-chave ≥ 1,5 s na tela; nada cortado ou sobreposto no contact sheet
- [ ] Pergunta final que vira pauta + ressalva na legenda do post
