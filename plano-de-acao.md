## Identificação

- **Equipe:** Joab da Silva Rocha - 495920 , Matheus Bernardino de Sousa - 422628
- **Trilha:** (B) curadoria e divulgação
- **Área temática da PREX:** Comunicação
- **Por que essa área,** em uma linha: Ação focada na produção de conteúdo educativo e guia interativo de divulgação tecnológica sobre consumo de APIs para criadores independentes.
- **Repositório:** https://github.com/MatheusBernardino/API/

## Campo 1 — O problema
Criadores de conteúdo independentes e editores iniciantes que desejam produzir vídeos automatizados (canais dark) enfrentam barreiras técnicas e de alto custo para integrar e consumir APIs de geração de roteiro, síntese de voz e acervo de mídias.

## Campo 2 — O público externo
Quem é, onde está, quantos são.

- **Quem é:** Editores e criadores de vídeos automatizados para redes sociais (YouTube, TikTok, Instagram).
- **Duas ou três pessoas reais desse grupo:**
- **Já falamos com alguma? Quando falaremos?** Primeiro contato em setembro (entre 18/09 e 25/09) para mapeamento inicial de dúvidas e envio do rascunho/final.
- **Como essa pessoa vai descobrir que o produto existe:** Através do repositório aberto no GitHub, compartilhamento em comunidades digitais de criadores e envio direto aos contatos mapeados.

## Campo 3 — Trilha e produto

- **O que é, em uma frase que caiba num tuíte, e onde ficará publicado:** Um guia e tutorial interativo (Trilha B) publicado em repositório aberto no GitHub que ensina criadores de conteúdo independentes a consumir e integrar APIs gratuitas de síntese de voz (Edge TTS), busca de mídias de fundo (Pexels API) e geração de roteiros para canais dark.
- **O que NÃO faz parte:** Não inclui o desenvolvimento de um software de edição de vídeo próprio, a criação de avatares virtuais 2D/3D (VTubers) ou a contratação de APIs pagas de renderização.
## Campo 4 — Fontes de dados

##### Fonte 1: Síntese de Voz (Text-to-Speech) 
| | |
| ------ | ------ | 
| Nome e órgão | **Microsoft Edge TTS** (Serviço de síntese de voz via biblioteca Python `edge-tts`) | 
| Endereço | `https://pypi.org/project/edge-tts/` | 
| Licença — e o que ela permite ao nosso produto | Gratuita e de acesso aberto (sem necessidade de chave de API ou cadastro); permite conversão de texto em áudio sem custos para o público. | 
| Atualização — periodicidade declarada e data do dado mais recente | Conversão executada em tempo real sob demanda. | 
| Dado pessoal? — se sim, granularidade e o que será agregado | Não. Processa apenas o texto digitado do roteiro. |

##### Fonte 2: Mídias de Fundo (Stock Footage) 
| | | 
| ------ | ------ | 
| Nome e órgão | **Pexels API** (Pexels) | 
| Endereço | `https://www.pexels.com/api/documentation/` | 
| Licença — e o que ela permite ao nosso produto | Licença Pexels gratuita para uso pessoal e comercial (via chave de API gratuita); permite busca automatizada de fotos e vídeos em HD. | 
| Atualização — periodicidade declarada e data do dado mais recente | Acervo atualizado continuamente pela plataforma. | 
| Dado pessoal? — se sim, granularidade e o que será agregado | Não. Processa apenas palavras-chave de busca (ex: "tecnologia", "natureza"). |

##### Fonte 3: Roteirização (LLM) 
| | | 
| ------ | ------ | 
| Nome e órgão | **Google Gemini API** (Google AI) | 
| Endereço | `https://ai.google.dev/docs` | 
| Licença — e o que ela permite ao nosso produto | Cota gratuita para desenvolvedores (Free Tier via API Key); permite geração REST de roteiros estruturados em JSON. | 
| Atualização — periodicidade declarada e data do dado mais recente | Processamento em tempo real sob demanda. |
| Dado pessoal? — se sim, granularidade e o que será agregado | Não. Processa apenas prompts genéricos de criação de conteúdo. |

## Campo 5 — Papéis

| Integrante | Papel | O que fica sob sua responsabilidade |
| ------ | ------ | ------ | 
| **Matheus** | **Co-Desenvolvedor Técnico e Gestor de Processos** | • **Desenvolvimento Técnico:** Testes de requisição HTTP REST na API de síntese de voz (**Edge TTS**) e validação da geração de roteiros na **Gemini API**.<br />• **Redação e Documentação:** Coautoria das seções técnicas do tutorial e exemplos de código do `README.md`.<br />• **Gestão e Processo:** Atualização semanal das entradas do `diario-de-bordo.md` e auxílio na abordagem ao público externo. |
| **Joab** | **Co-Desenvolvedor Técnico e Gestor de Alcance** | • **Desenvolvimento Técnico:** Testes de busca automatizada de mídias na **Pexels API** e configuração do gerenciamento de chaves de API (`.env`).<br />• **Redação e Documentação:** Coautoria da explicação didática sobre os conceitos de API/JSON e revisão do tutorial.<br />• **Gestão e Processo:** Condução direta das mensagens com os criadores de conteúdo externos, organização da pasta `evidencias` e manutenção do `evidencias.csv`. |

## Campo 6 — Cronograma

| Data | O que estará pronto | 
| ------ | ------ | 
| 02/10 (Marco 1) | Plano final aprovado e primeira versão do guia com os exemplos básicos de requisição das APIs em formato de rascunho. | 
| 13/11 (Marco 2) | Guia completo e funcional de ponta a ponta, permitindo que um usuário externo consiga testar as integrações sozinho. | 
| 27/11 (Marco 3) | Produto final publicado com documentação (README) completa, diário de bordo consolidado e evidências de alcance salvas. | 
| 04/12 (Socialização) | Apresentação pública do projeto realizada e folha de presença do público impressa e entregue. | 

**Dependências externas.** Obtenção de chaves gratuitas de API (Pexels e Google Gemini). Pedidos e cadastros serão realizados nesta primeira semana de trabalho.
## Campo 7 — Indicadores

| | Medida | Como será coletada | Valor que seria bom | 
| ------ | ------ | ------ | ------ | 
| Contagem | Acessos e visualizações únicas ao repositório público do tutorial. | Métricas do repositório no GitHub (Insights/Traffic) coletadas entre 02/10 e 27/11\. | Pelo menos 30 visualizações únicas no repositório. | 
| Qualitativa | Avaliação escrita de criadores de conteúdo/editores externos sobre a clareza do guia. | Mensagens de retorno ou formulário curto aplicado aos criadores que testaram o tutorial, registrados em `evidencias.csv`. | Pelo menos 2 retornos escritos confirmando que conseguiram executar a integração sem ajuda. |

## Antes de entregar: a prova dos nove

- [ ] Riscamos tudo o que não conseguiríamos terminar até 13/11.
- [ ] O que sobrou ainda ajuda alguém.
- [ ] Uma pessoa de fora entende o Campo 1 e o Campo 3 sem explicação oral.
- [ ] A data da primeira conversa com o público está marcada.
- [ ] Os indicadores podem ser coletados sem depender de terceiro.

---

