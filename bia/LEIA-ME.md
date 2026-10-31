# BIA · Teaser para a TV (`/bia/`)

Versão HTML5 do teaser aprovado, feita para o plugin **Website** do TVPlayer.
É o mesmo motor de animação do teaser, sem botões nem barra de tempo.

- Começa sozinha e repete a cada 30 s, sem som e sem interação.
- Ocupa a tela inteira em 16:9 sem distorcer. Em telas de outra proporção, a sobra fica no mesmo azul do fundo.
- Não precisa de servidor, Node, Playwright nem ffmpeg: são só arquivos estáticos.
- Recarrega sozinha quando o `versao.txt` da raiz do site mudar (mesmo padrão das outras telas) e a cada 12 h, na virada do ciclo.

## Arquivos

```
bia/
├── index.html          página (logotipo B.I.A. oficial embutido)
├── tv.css              estilos (fonte Lexend embutida)
├── config.js           textos, cores e tempos (o mesmo do teaser)
├── teaser-tv.js        motor da animação, compatível com navegadores antigos
├── LEIA-ME.md
└── assets/
    ├── telas/          5 telas reais da BIA V2
    ├── marca/          símbolo E (provisório) e nome EnvolveLabs
    └── fontes/         licença OFL da Lexend
```

Todos os caminhos são relativos, então funcionam dentro de `noticias-tv/bia/`.

## Testar no computador

- **Mais rápido:** dê dois cliques no `index.html`. Abre no navegador e já toca.
- **Igual ao GitHub Pages:** na pasta que contém `bia/`, rode `python3 -m http.server 8000` e abra `http://localhost:8000/bia/`.
- Aperte F11 para ver em tela cheia e redimensione a janela para conferir o encaixe.

## Publicar (só quando autorizado)

1. Copie a pasta `bia/` inteira para a raiz do repositório `noticias-tv`, ao lado de `dicas/`, `tempo/` e `instagram/`.
2. Atualize o número do `versao.txt` da raiz para as telas abertas recarregarem.
3. Depois que o GitHub Pages publicar (1 a 2 min), abra https://caioabreu-ui.github.io/noticias-tv/bia/
4. No TVPlayer: Plugins → Tela Inteira → **Website** → cole o endereço acima. Duração sugerida no playlist: 30 s ou múltiplos de 30.
