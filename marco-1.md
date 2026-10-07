### Entrega de Marco 1 — 02/10/2026

#### Identificação

- **Equipe:** Matheus Bernardino de Sousa (422628) e Joab da Silva Rocha (495920)
- **Marco e data:** Marco 1 — 02/10/2026
- **Trilha:** Trilha B — Curadoria e divulgação (Área Temática: Comunicação)
- **Endereço público do produto:** https://github.com/MatheusBernardino/API
- **Commit ou tag desta entrega:** Tag: `marco-1`

---

#### Campo 1 — O que funciona hoje

1. **Geração de roteiro estruturado:** Executar `python src/gerador_roteiro.py`, digitar um tema (ex: "carros esportivos") e receber diretamente no terminal o roteiro em JSON com 8 cenas dinâmicas e palavras-chave de busca geradas pelo Gemini.
2. **Síntese de voz neural isolada:** Executar `python src/teste_edge_tts.py` para processar uma frase de texto e gerar um arquivo de áudio `.mp3` de alta qualidade em português sem custos de API.
3. **Pipeline completo de ponta a ponta:** Executar `python src/main.py`, informar o tema desejado e receber o vídeo vertical final renderizado (`video_final.mp4`) com áudio sincronizado e vídeos de fundo do Pexels, organizado na subpasta de execução em `temp_media/`.

---

#### Campo 2 — O que mudou desde o marco anterior

n.a.

---

#### Campo 3 — Alcance

| Indicador                                                   | Planejado                | Obtido até hoje                                                                                                                                    | Onde está a evidência                                                  |
| ----------------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Total de visualizações de páginas no repositório (Contagem) | 30 visualizações         | 191 visualizações acumuladas nos últimos 14 dias registradas no GitHub Insights Traffic                                                           | evidencias/2026-10-02-acessos_github.png e linha no evidencias.csv |
| Abordagem e feedback do público externo (Qualitativa)       | 3 contatos com criadores | E-mails e DMs de convite de teste e feedback enviados para os criadores de conteúdo mapeados (@oLoboShortsBR, @seeanimais e @estranhascuriosidade) | `evidencias/2026-10-03-dms_criador.pdf` e linha no `evidencias.csv`    |

**O que o público externo disse:** Mensagens de abordagem enviadas via e-mail e DM para os criadores de conteúdo mapeados no Marco 1; aguardando o retorno e o feedback escrito sobre o uso do gerador para consolidação no Marco 2.

---

#### Campo 4 — Obstáculo e replanejamento

- **Obstáculo:** Padronização da resposta em JSON retornada pela Gemini API para garantir que as chaves de texto, tempo e termos de busca fossem lidas corretamente pelo módulo de renderização de vídeo (`video.py`).
- **Tempo custado:** Aproximadamente 3 horas de testes e engenharia de prompt.
- **O que fizemos:** Ajustamos o _system prompt_ no `src/gerador_roteiro.py` para forçar a saída estruturada em JSON e adicionamos tratamento de exceção na desserialização com `json.loads`.

---

#### Campo 5 — Autopontuação

| Dimensão                            | n.a.? | Pts (0–2) | Por quê, em uma linha                                                                                     |
| ----------------------------------- | ----- | --------- | --------------------------------------------------------------------------------------------------------- |
| D1 Qualidade técnica                |       | 2.0       | Pipeline modular funcional de ponta a ponta (`gerador_roteiro`, `fala`, `material`, `video` e `main.py`). |
| D2 Alcance e adequação ao público   | Sim   | -         | Em andamento (abordagem inicial enviada ao público e registro de tráfego do repositório coletado).        |
| D3 Documentação e reprodutibilidade |       | 2.0       | README.md completo com guia passo a passo, `.env.example`, licença e limitações declaradas.               |
| D4 Registro do processo             |       | 2.0       | Diário de bordo atualizado semanalmente, papéis bem definidos no Campo 5 e `evidencias.csv` preenchido.   |
| D5 Autoavaliação e reflexão         | Sim   | -         | Aplicável apenas ao Marco 3 e à Socialização.                                                             |

- **Pontos obtidos:** 6.0
- **Pontos aplicáveis:** 6.0 (D1 + D3 + D4)
- **Nota calculada (10 × obtidos / aplicáveis):** **10.0**

---

#### Antes de entregar: Prova dos Nove

- [x] O endereço do produto abre numa máquina que não é a nossa.
- [x] O que o Campo 1 promete foi testado hoje, não na semana passada.
- [x] O README.md corresponde ao que o produto faz agora.
- [x] O diário tem entrada de todas as semanas desde o último marco.
- [x] Toda evidência do Campo 3 tem data e está em `evidencias/`.
- [x] O commit informado está publicado no GitHub.
