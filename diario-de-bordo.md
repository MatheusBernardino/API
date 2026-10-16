### Entradas

#### Semana de 18/09

- **Quem trabalhou e quanto:** Matheus — 4h; Joab — 4h
- **O que foi feito:**
  - Inicialização e estruturação do repositório no GitHub, remoção de arquivos e instruções de template (`LEIA-ME.md`), configuração do esqueleto do `README.md` e redação da primeira versão do `plano-de-acao.md` (Matheus).
  - Pesquisa exploratória de viabilidade técnica comparando projetos de VTubers versus automação para Canais Dark, levantamento das diretrizes da Trilha B (Comunicação) e alinhamento da proposta técnica da equipe (Joab).
- **Obstáculo:** Escolha entre os temas de VTubers e Canais Dark; custou ~2h de discussão da equipe. Resolvido optando por Canais Dark devido à menor complexidade técnica de integração de APIs REST e facilidade de replicação pelo público.
- **Contato com o público:** Nenhum contato nesta semana.
- **Evidência coletada:** n.a. (semana de alinhamento conceitual, pesquisa e estruturação inicial do repositório).
- **Próxima semana:** Estruturar o guia de instalação no `README.md` e testar as requisições básicas na API do Edge TTS e Pexels.

---

#### Semana de 25/09

- **Quem trabalhou e quanto:** Matheus — 5h; Joab — 4h
- **O que foi feito:**
  - Estruturação dos diretórios de código (`src/`) e rastreabilidade (`evidencias/`), configuração de dependências (`requirements.txt`), variáveis de ambiente (`.env.example`), implementação dos scripts de validação inicial (`src/teste_edge_tts.py` e `src/teste_pexels.py`) e consolidação das primeiras evidências e planilha `evidencias.csv` (Matheus).
  - Redação do tutorial técnico inicial no `README.md` com pré-requisitos, instruções de instalação do ambiente, obtenção de chaves de API e roteiro de execução dos testes de síntese de voz e busca de mídia (Joab).
- **Obstáculo:** Entender a estrutura e o funcionamento das APIs que serão usadas na automação (Edge TTS, Pexels e Gemini); custou ~2h de leitura e testes de rotas. Resolvido com scripts de teste dedicados.
- **Contato com o público:** Nenhum contato nesta semana.
- **Evidência coletada:** Print da execução do terminal e arquivos de teste salvos em `evidencias/2026-09-25-execucao-terminal.png`, `evidencias/2026-09-25-teste-audio-edgetts.mp3` e mídias do Pexels(`2026-09-25-teste-pexels-video.mp4`,`2026-09-25-teste-pexels-imagem-id-9784238.jpeg`,`2026-09-25-teste-pexels-imagem-id-4900859.png` ), catalogadas no `evidencias.csv`.
- **Próxima semana:** Integrar a geração de roteiros com a API do Gemini (`src/gerador_roteiro.py`), estruturar o fluxo principal no `src/main.py` e preparar a entrega do Marco 1 (02/10).

---

#### Semana de 02/10

- **Quem trabalhou e quanto:** Matheus — 6h; Joab — 5h
- **O que foi feito:**
  - Modularização do pipeline de áudio (`src/fala.py`), download e corte de mídias (`src/material.py`), montagem e renderização com MoviePy (`src/video.py`), orquestrador completo (`src/main.py`), rotina de extração e salvamento de créditos dos criadores do Pexels (`creditos.txt`), redação da ficha `marco-1.md` e consolidação final das evidências (Matheus).
  - Implementação do gerador de roteiros com a Gemini API (`src/gerador_roteiro.py`) com schema estruturado em JSON para 8 cenas, engenharia de prompt para gerar termos de busca compatíveis com o Pexels, tratamento de instabilidade/erro 503 com retentativas automáticas e atualização do `README.md` com o guia de execução da pipeline completa (Joab).
- **Obstáculo:** Garantir a formatação estrita do JSON retornado pelo Gemini e contornar erros temporários de sobrecarga 503 da API; custou ~3h. Resolvido refinando o system prompt e adicionando exponential backoff.
- **Contato com o público:** Mapeamento dos criadores de conteúdo e canais dark (@oLoboShortsBR, @seeanimais e @estranhascuriosidade) e envio de mensagens e e-mails de abordagem e convite de teste após termos a pipeline funcional do Marco 1; sem resposta ainda (aguardando feedback para o Marco 2).
- **Evidência coletada:** Captura do tráfego do GitHub em `evidencias/2026-10-02-acessos_github.png`, abordagem aos criadores em `evidencias/2026-10-03-dms_criador.pdf` e atualização da planilha `evidencias.csv`.
- **Próxima semana:** Acompanhar o retorno e o feedback do público externo e iniciar os refinamentos de usabilidade e tratamento de falhas.

---

#### Semana de 09/10

- **Quem trabalhou e quanto:** Matheus — 4h; Joab — 6h
- **O que foi feito:**
  - Higienização de dados pessoais em evidências e expurgo definitivo do histórico Git via rebase interativo; padronização métrica de tráfego do repositório (191 visualizações acumuladas) e definição formal de rotina de coleta quinzenal no `marco-1.md` e `plano-de-acao.md`; preparação de ambiente na nuvem via Google Colab com link de execução direta e badge no `README.md`; registro da nova evidência de testes unitários no `evidencias.csv` (Matheus).
  - Criação do arquivo formal de licença de código aberto `LICENSE` (MIT) e sua documentação no `README.md`; refatoração de resiliência e tratamento de falhas em `src/main.py` e `src/material.py` (fail-fast com exceções customizadas `ChaveInvalidaError`/`PexelsError` e adição de timeouts explícitos nas requisições do Pexels: 5s conexão, 15s busca e 60s download); implementação da suíte de 13 testes unitários automatizados com `pytest` em `tests/test_falhas.py` (Joab).
- **Obstáculo:** Garantir testes reproduzíveis sem consumir cotas reais das APIs ou expor credenciais em testes automatizados; custou ~2h. Resolvido utilizando `unittest.mock` para simular cenários de chaves ausentes, respostas 401 de autenticação e timeouts de rede de forma totalmente determinística.
- **Contato com o público:** Disponibilização de acesso sem necessidade de setup local através do Google Colab para facilitar testes por criadores sem familiaridade com terminal e Python.
- **Evidência coletada:** Registro e captura da execução integral da suíte de 13 testes unitários com pytest em `evidencias/2026-10-11-execucao_pytest.png` e atualização do repositório e planilha `evidencias.csv`.
- **Próxima semana:** Acompanhar feedback dos criadores contatados, analisar sugestões de novos formatos de vídeo e aprimoramentos no modelo já criado para o Marco 2.

---

#### Semana de 16/10

- **Quem trabalhou e quanto:** Matheus — 3h; Joab — 0h
- **O que foi feito:**
  - Correção das inconsistências apontadas no diário de bordo: ajuste da referência para `src/fala.py`, especificação dos timeouts reais do Pexels e atualização dos nomes exatos das evidências de 25/09 (Matheus).
  - Abertura de chamado junto ao suporte do GitHub para solicitação de _garbage collection_ e limpeza de cache de commits órfãos, já atendido e concluído pela plataforma (Matheus).
  - Coleta do print de tráfego na data fixa de 16/10 (`evidencias/2026-10-16-visitantes_github.png`), registro no `evidencias.csv` e alinhamento do Campo 7 no `plano-de-acao.md` para visitantes únicos (Matheus).
- **Obstáculo:** Nenhum obstáculo técnico enfrentado nesta semana.
- **Contato com o público:** Nenhum contato nesta semana.
- **Evidência coletada:** Captura da tela de tráfego quinzenal em `evidencias/2026-10-16-visitantes_github.png`, registrada no `evidencias.csv`.
- **Próxima semana:** Iniciar a resolução das pendências do Marco 2 (tratamento de erro 403 do Edge TTS no `src/fala.py` para não gerar áudio vazio e anexar a evidência do 3º criador).
