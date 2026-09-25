##### Semana de 18/09
**Quem trabalhou e quanto:** Matheus — 4h; Joab — 4h

**O que foi feito:**
* Pesquisa introdutória de materiais/conceitos básicos e reunião da equipe para discussão e viabilidade do tema.
* Definição da equipe e escolha formal da Trilha B (Comunicação) com foco em automação para Canais Dark.
* Estruturação do repositório: Configuração da pasta de modelos no GitHub e preenchimento do rascunho inicial do `plano-de-acao.md` (problema, público, fontes de APIs e divisão de papéis).

**Obstáculo:** Escolha entre os temas de VTubers e Canais Dark. Resolvido optando por Canais Dark devido à menor complexidade técnica de integração de APIs REST e maior facilidade de replicação pelo público.

**Contato com o público:** Mapeamento inicial de perfis de criadores de conteúdo e editores independentes para envio do rascunho da metodologia.

**Próxima semana:** Estruturar o esqueleto do guia no `README.md` e testar as requisições básicas na API do Edge TTS e Pexels.

---

##### Semana de 25/09 
**Quem trabalhou e quanto:** Matheus — 4h; Joab — 4h

**O que foi feito:** 
* Configuração da estrutura do repositório no editor de código, organizando as pastas `src/` e `evidencias/`.
* Configuração dos arquivos de ambiente e dependências: `requirements.txt`, `.gitignore` e `.env.example`.
* Elaboração do manual inicial no `README.md` cobrindo o uso e a execução dos scripts.
* Implementação e testes executáveis das requisições para síntese de áudio (`src/teste_edge_tts.py`) e busca de mídias (`src/teste_pexels.py`).

**Obstáculo:** Entender a estrutura e o funcionamento das APIs que serão usadas na automação (Edge TTS, Pexels e Gemini).

**Contato com o público:** Preparação do ambiente e da documentação técnica para permitir o teste por usuários externos e criadores de conteúdo.

**Evidência coletada:** Print da execução do terminal e arquivos de teste salvos na pasta `evidencias/2026-09-25-teste-apis.png` , `evidencias/2026-09-25-teste-audio.mp3` , `2026-09-25-teste-pexels-imagem-id-4900859.png` , `2026-09-25-teste-pexels-imagem-id-9784238.jpeg` , `2026-09-25-teste-pexels-video.mp4`.

**Próxima semana:** Integrar a geração de roteiros com a API do Gemini (`src/gerador_roteiro.py`), estruturar o fluxo principal no `src/main.py` e preparar a entrega do Marco 1 (02/10).

---
