# Entrega de Marco 2 — 13/11/2026

## Identificação

- **Equipe:** Matheus Bernardino de Sousa (422628) e Joab da Silva Rocha (495920)
- **Marco e data:** Marco 2 — 13/11/2026
- **Trilha:** Trilha B — Curadoria e divulgação (Área Temática: Comunicação)
- **Endereço público do produto:** https://github.com/MatheusBernardino/API
- **Commit ou tag desta entrega:** `<SHA_DO_COMMIT_DE_SEXTA>` (Tag: `marco-2`)

---

## Campo 1 — O que funciona hoje

1. **Gerar vídeo vertical completo pelo terminal:** Executar `python src/main.py`, digitar um tema no prompt (ex.: `Buracos Negros`) e receber na pasta `temp_media/run_<timestamp>_buracos_negros/` o vídeo renderizado `video_final.mp4` (com narração neural sincronizada e vídeos verticais em HD do Pexels) junto com o arquivo `creditos.txt` listando autores e links de cada mídia.
2. **Executar o gerador no navegador sem instalar nada (Google Colab):** Abrir `https://colab.research.google.com/drive/14Ck-v9NyS3qpsbuRZjD2pew3ZHHVVgbE?usp=sharing`, informar as chaves `PEXELS_API_KEY` e `GEMINI_API_KEY` nos campos mascarados, digitar o tema desejado e baixar o arquivo `video_final.mp4` gerado na sessão.
3. **Validar o tratamento de falhas offline com a suíte automatizada:** Executar `python -m pytest -v` na raiz do repositório (sem necessidade de internet ou chaves no `.env`) e receber a aprovação dos 19 testes automatizados (`19 passed`) cobrindo chaves ausentes/inválidas, limite de requisições (429), timeouts HTTP (5s/15s/60s) e erro 403/áudio vazio do Edge TTS.

---

## Campo 2 — O que mudou desde o marco anterior

- **Passou a existir:**
  - Tratamento completo de falhas no módulo de voz (`src/fala.py`) com a exceção `TTSError`: falhas HTTP (como erro 403 do Edge TTS), queda de rede, timeout ou resposta vazia agora exibem mensagem clara, apagam qualquer arquivo `.mp3` vazio/incompleto residual e encerram o `src/main.py` com código de saída `1`.
  - Suíte expandida para **19 testes unitários** com `pytest` (`tests/test_falhas.py` com 13 testes + `tests/test_tts.py` com 6 novos testes para o Edge TTS).
  - Ambiente interativo no **Google Colab** linkado com badge no `README.md` para permitir que criadores de conteúdo testem a ferramenta sem configurar Python ou FFmpeg localmente.
  - Higienização e reestruturação do `evidencias.csv` (mantendo estritamente os indicadores do Campo 7), comprovação visual do 3º criador (`@oLoboShortsBR`) em `evidencias/2026-10-03-dms_criador.pdf` e rotina quinzenal de captura de visitantes únicos (16/10, 30/10 e 13/11).
  - Correção da tabela de procedência de timeouts no `README.md` (diferenciando os 10s de `src/teste_pexels.py` dos 5s, 15s e 60s de `src/material.py`) e expurgo definitivo de caches órfãos junto ao suporte do GitHub.
- **Foi cortado, e por quê:**
  - Nenhum recurso técnico do guia foi cortado; na documentação e rastreabilidade, foram cortadas as 10 linhas de registros de execução de testes locais do `evidencias.csv` (pois execução de teste interno não é indicador de alcance do Campo 7) e a métrica antiga de visualizações totais (`Total Views`), substituída pela medição de visitantes únicos (`Unique Visitors`).

---

## Campo 3 — Alcance

| Indicador | Planejado | Obtido até hoje | Onde está a evidência |
| :-- | :-- | :-- | :-- |
| Total de visitantes únicos do repositório público (Contagem) | Pelo menos 20 visitantes únicos | `<X>` visitantes únicos somados nas janelas quinzenais (3 em 16/10 + 1 em 30/10 + `<Y>` em 13/11) | `evidencias/2026-10-16-visitantes_github.png`, `evidencias/2026-10-30-visitantes_github.png`, `evidencias/2026-11-13-visitantes_github.png` e `evidencias.csv` |
| Avaliação escrita de criadores/editores externos (Qualitativa) | Pelo menos 2 retornos escritos | 3 criadores abordados (`@oLoboShortsBR`, `@seeanimais`, `@estranhascuriosidade`); `<inserir retorno se houver, ou informar 0 retornos até o momento>` | `evidencias/2026-10-03-dms_criador.pdf` e `evidencias.csv` |

**O que o público externo disse.** Nenhum dos três canais abordados respondeu até o momento. Plano para mudar até o Marco 3: realizar nova rodada de contato direto com editores iniciantes e perfis menores enviando diretamente o link do Google Colab (que dispensa instalação local) e formulário rápido de 2 perguntas.

---

## Campo 4 — Obstáculo e replanejamento

- **Obstáculo:** Bloqueio intermitente (erro HTTP 403) no serviço gratuito do Microsoft Edge TTS devido à desatualização de tokens na versão anterior da biblioteca `edge-tts`, que fazia o script falhar com traceback bruto e deixar um arquivo `.mp3` de 0 bytes na pasta da cena.
- **Tempo custado:** Cerca de 3 horas entre diagnóstico, atualização de dependências e escrita dos mocks de teste.
- **O que fizemos a respeito:** Atualizamos a dependência para `edge-tts>=7.2.7` (com `aiohttp>=3.9.0`), implementamos a exceção `TTSError` em `src/fala.py` que remove automaticamente arquivos `.mp3` vazios/corrompidos em caso de erro e criamos 6 testes unitários em `tests/test_tts.py` simulando erro 403, falha de rede e áudio vazio.

---

## Campo 5 — Autopontuação

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | | 2.0 | Pipeline funcional de ponta a ponta, fail-fast para chaves/TTS (sem deixar `.mp3` vazio), timeouts explícitos e 19 testes passando no pytest. |
| D2 Alcance e adequação ao público | | 1.0 | 3 abordagens documentadas e Google Colab disponível para uso sem setup, mas ainda sem retorno escrito do público externo e com baixo número de visitantes únicos. |
| D3 Documentação e reprodutibilidade | | 2.0 | `README.md` completo com passo a passo, link para Google Colab, tabela de falhas, procedência exata dos timeouts (5s/15s/60s e 10s), limites do Pexels e licença MIT. |
| D4 Registro do processo | | 2.0 | `diario-de-bordo.md` corrigido e atualizado semanalmente com tarefas e horas nominais por integrante, e `evidencias.csv` restrito aos indicadores do Campo 7. |
| D5 Autoavaliação e reflexão | Sim | - | Aplicável apenas ao Marco 3 e à Socialização. |

- **Pontos obtidos:** 7.0
- **Pontos aplicáveis:** 8.0 (D1 + D2 + D3 + D4)
- **Nota calculada (10 × obtidos / aplicáveis):** **8.75**

---

## Antes de entregar

- [ ] O endereço do produto abre numa máquina que não é a nossa.
- [ ] O que o Campo 1 promete foi testado hoje, não na semana passada.
- [ ] O `README.md` corresponde ao que o produto faz agora.
- [ ] O diário tem entrada de todas as semanas desde o último marco.
- [ ] Toda evidência do Campo 3 tem data e está em `evidencias/`.
- [ ] O commit informado está publicado.

