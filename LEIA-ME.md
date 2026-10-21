# Notícias do dia — TV IBFE

## O que tem aqui
- `index.html` — a tela de notícias (design IBFE, troca a cada 12 s, QR Code por notícia).
- `gerar_feed.py` — robô que lê as fontes e gera `noticias.json` só com notícias recentes.
- `fontes.json` — lista de sites (edite para incluir/remover fontes).
- `.github/workflows/atualizar.yml` — faz o robô rodar sozinho a cada 30 minutos.

## Colocar no ar (uma vez só)
1. Crie uma conta gratuita em github.com.
2. Crie um repositório público chamado `noticias-tv` e envie todos estes arquivos (botão "Add file → Upload files").
3. Em **Settings → Pages**, escolha "Deploy from a branch", branch `main`, pasta `/ (root)` e salve.
4. Em **Actions**, abra "Atualizar notícias da TV" e clique em **Run workflow** para gerar a primeira lista.
5. O endereço da tela será `https://SEU-USUARIO.github.io/noticias-tv/`.
6. No TVPlayer: Plugins → Tela Inteira → **Website**, cole esse endereço.
