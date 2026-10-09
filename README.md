 # Guia de Automação para Canais Dark (Edge TTS + Pexels API + Gemini AI)

Um guia e conjunto de scripts em Python para automatizar a criação de conteúdo para canais dark, realizando síntese de voz gratuita e busca automatizada de mídias de fundo via API.

## Para quem é
Criadores de conteúdo, estudantes de Ciência de Dados e entusiastas que desejam aprender a consumir APIs web para produção automatizada de vídeos e mídias curtas.

## Requisitos
- **Python 3.10 ou superior** (desenvolvido e testado na 3.12).
- Chaves gratuitas das APIs do Pexels e do Google Gemini (veja o passo 4).

## Como usar
Passo a passo para clonar e executar os testes na sua máquina:

1. Clone o repositório:
```bash
git clone https://github.com/MatheusBernardino/API.git
cd API
```

2. Crie e ative o ambiente virtual (.venv):
No Linux/macOS:
*(Caso não tenha o módulo venv instalado, no Ubuntu/Debian execute: `sudo apt install python3-venv`)*
```bash
python3 -m venv .venv
source .venv/bin/activate
```
No Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Copie o arquivo `.env.example` para `.env` e insira as suas chaves de API reais (Pexels e Google Gemini):
```env
PEXELS_API_KEY=sua_chave_pexels_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
```

5. Execute o pipeline completo do projeto:
O projeto inclui um orquestrador que conecta a IA, a síntese de voz e a busca de vídeos automaticamente.
```bash
# Para gerar um vídeo completo (pede o tema no terminal):
python src/main.py
```

E o que sai:
```text
Digite o tema do vídeo (ou deixe em branco para o padrão): Buracos Negros

[1/3] Gerando roteiro com Gemini para: 'Buracos Negros'...
[Roteiro] 8 cenas geradas com sucesso!

[2/3] Iniciando produção do vídeo (temporários em: temp_media/run_20261003_104000_buracos_negros)...
[Cena 1/8] Sintetizando áudio...
[Cena 1/8] Baixando mídia para a keyword: 'black hole'...
...
[Render] Montando e interpolando arquivos via FFmpeg...
[Sucesso] Vídeo final gerado em: temp_media/run_20261003_104000_buracos_negros/video_final.mp4

[3/3] Pipeline concluído! Abra o arquivo 'temp_media/run_20261003_104000_buracos_negros/video_final.mp4' para assistir.
```

Se preferir testar os componentes de forma isolada:
```bash
# Gerar apenas o roteiro em JSON (Gemini):
python src/gerador_roteiro.py

# Testar apenas o fluxo de renderização com dados falsos (Edge TTS + Pexels + FFmpeg):
python src/teste_pipeline.py
```


## Se algo der errado
O programa para na primeira falha e encerra com código de saída 1, com uma mensagem objetiva:

| Situação | O que acontece |
| :-- | :-- |
| `PEXELS_API_KEY` ou `GEMINI_API_KEY` ausente no `.env` | Avisa e encerra antes de qualquer chamada. |
| Chave do Gemini inválida | Encerra na 1ª tentativa, sem repetir. Falhas temporárias (ex.: erro 503) são repetidas até 5 vezes. |
| Chave do Pexels inválida (401/403) | Mensagem clara e encerramento. |
| Limite do Pexels atingido (429) | Mensagem pedindo para aguardar. |
| Sem resposta do Pexels | Timeout (5s para conectar; 15s na busca e 60s no download). |

## Limite de requisições do Pexels
O plano gratuito da API do Pexels permite, por padrão, **200 requisições por hora e 20.000 por mês** (conferir em https://www.pexels.com/api/documentation/). Cada cena do roteiro faz 2 requisições (busca + download), então um vídeo de 8 cenas consome cerca de 16.

## Testes automatizados
Os testes de falhas (chave inválida, limite, timeout e código de saída) usam respostas simuladas, então não precisam de internet nem de chaves:
```bash
python -m pytest
```

## De onde vêm os dados

| Fonte | Órgão | Endereço | Data do dado |
| :---- | :---- | :---- | :---- |
| *Síntese de Voz* | Microsoft Edge TTS (via edge-tts) | https://pypi.org/project/edge-tts/ | Tempo real (sob demanda) |
| *Mídias de Fundo* | Pexels API | https://www.pexels.com/api/ | Acervo atualizado continuamente |
| *Geração de Roteiros* | Google Gemini API (via google-genai) | https://ai.google.dev/ | Tempo real (IA Generativa) |

## Licença

- *Dados e Mídias:* Licença Pexels (Royalty-Free gratuita para uso pessoal e comercial via chave de API). Permite busca automatizada de fotos e vídeos em HD. Exige/recomenda a atribuição do criador (créditos ao fotógrafo e link de origem), os créditos sao gerados na produção do vídeo no main.py e salvo no arquivo créditos.txt em temp_media.
- *Código e material desta equipe:* A biblioteca Python possui licença MIT (código aberto). O serviço subjacente consome a API do Microsoft Edge gratuitamente (sem necessidade de chave). Como o serviço em si não possui termos comerciais 100% explícitos da Microsoft, o uso é recomendado para fins educacionais, pessoais e de prototipagem.

## O que este produto não faz

- Não realiza edições com **efeitos visuais avançados** (transições complexas, legendas animadas 3D). Ele foca na automatização do fluxo base (gerar script -> TTS -> baixar vídeos -> montagem e renderização básica automatizada).
- Exige chaves de API próprias (Pexels e Google Gemini) configuradas no arquivo `.env`.

## Contato
Equipe do Projeto (UFC - CC0464):
- Matheus Bernardino de Sousa (422628)
- Joab da Silva Rocha (495920)
- Repositório: https://github.com/MatheusBernardino/API/

---

## Onde está publicado
- Repositório público no GitHub: https://github.com/MatheusBernardino/API/
- Guia, tutoriais práticos na pasta src/ e documentação nos arquivos Markdown.

## Procedência dos números

| Número que aparece no material | Fonte | Como foi calculado |
| :-- | :-- | :-- |
| per_page: 2 (vídeos) / 4 (fotos) | API do Pexels | Parâmetro de requisição HTTP configurado nos scripts de teste |
| Tempo limite (timeout de 10s) | httpx | Parâmetro de tolerância máxima definido nas chamadas de rede |

## Como adaptar para outro contexto
Para adaptar o projeto para outro nicho de conteúdo ou canal:
1. *Alterar o nicho visual/tema:* Modifique o parâmetro no script iterativo `src/gerador_roteiro.py` ou os termos de busca no `src/teste_pipeline.py`.
2. *Alterar a voz ou idioma:* Modifique o parâmetro `nome_voz` no arquivo `src/fala.py` (você pode alternar entre vozes do Edge TTS como `pt-BR-FranciscaNeural`, `pt-BR-AntonioNeural`, etc.).
3. *Pipeline de Edição:* A montagem básica já ocorre via `MoviePy` no `src/video.py`. Você pode modificar esse arquivo para plugar lógicas adicionais ou usar o conteúdo bruto baixado no `temp_media/` em editores profissionais (CapCut, Premiere).
