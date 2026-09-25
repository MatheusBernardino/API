# Guia de Automação para Canais Dark (Edge TTS + Pexels API)

Um guia e conjunto de scripts em Python para automatizar a criação de conteúdo para canais dark, realizando síntese de voz gratuita e busca automatizada de mídias de fundo via API.

## Para quem é
Criadores de conteúdo, estudantes de Ciência de Dados e entusiastas que desejam aprender a consumir APIs web para produção automatizada de vídeos e mídias curtas.

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
Copie o arquivo .env.example para .env e insira sua chave do Pexels:
```env
PEXELS_API_KEY=sua_chave_aqui
```

5. Execute os scripts de teste:
```bash
python src/teste_edge_tts.py
python src/teste_pexels.py
```


## De onde vêm os dados

| Fonte | Órgão / Plataforma | Endereço | Data do dado / Periodicidade |
| :-- | :-- | :-- | :-- |
| *Síntese de Voz* | Microsoft Edge TTS (via biblioteca edge-tts) | https://pypi.org/project/edge-tts/ | Tempo real (sob demanda) |
| *Mídias de Fundo* | Pexels API | https://www.pexels.com/api/ | Acervo atualizado continuamente (2026) |

## Licença

- *Dados e Mídias:* Licença Pexels (Royalty-Free / Livre para uso pessoal e comercial).
- *Código e material desta equipe:* Licença MIT (livre para reuso e modificação).

## O que este produto não faz

- Não realiza a edição final nem a renderização completa do vídeo com efeitos visuais avançados (foca no consumo automatizado das APIs e download dos assets).
- Exige uma chave de API própria do Pexels configurada no arquivo .env.

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
1. *Alterar o nicho visual:* Modifique o parâmetro query no arquivo src/teste_pexels.py para buscar temas específicos (ex: "natureza", "finanças", "espaço").
2. *Alterar a voz ou idioma:* Modifique o texto do roteiro e a voz no arquivo src/teste_edge_tts.py (você pode alternar entre vozes como pt-BR-FranciscaNeural, pt-BR-AntonioNeural, etc.).
3. *Pipeline de Edição:* Conecte as mídias geradas (áudios .mp3 e vídeos .mp4) a ferramentas como FFmpeg, MoviePy, CapCut ou DaVinci Resolve para renderização automatizada.