"""Robô de notícias da TV IBFE.
Lê as fontes de fontes.json, mantém só notícias das últimas HORAS horas,
remove duplicadas, gera um QR Code (SVG) para cada link e grava noticias.json."""
import json, re, html, io, hashlib, datetime as dt, calendar
import feedparser, qrcode, qrcode.image.svg

HORAS = 30          # janela de notícias "do dia"
MAX_POR_FONTE = 6
MAX_TOTAL = 18

# Filtro de conteúdo: a TV é de uma escola — evita notícias policiais/trágicas e itens que não são matérias
BLOQUEIO = ["morto","morta","mortos","mortas","morre","morreu","morte","mata","matou","assassin","homicíd","tiro","baleado",
  "assalt","roub","furt","preso","presa","prisão","prende","polícia","policial","crime","criminos","tráfico","droga",
  "estupr","abuso","violência","agress","esfaque","facada","acidente","tragédia","desastre","queda de avião","réus","réu ",
  "sequestr","golpe","maus-tratos","maus tratos","jogando saco","abandon","fraude","corpo","cadáver","incêndio","suicíd","feminicíd","briga"]
IGNORAR = ["assista ao","ao vivo","vídeo:","video:","veja o vídeo","podcast","siga o","bom dia","jornal da","eptv"]
def adequada(titulo, resumo):
    t = (titulo + " " + resumo).lower()
    tl = titulo.lower()
    if len(titulo.split()) < 5: return False          # nomes de programa ("Bom Dia Cidade")
    if "vídeo" in tl.split(";")[-1] or tl.endswith("vídeo"): return False
    return not any(b in t for b in BLOQUEIO) and not any(tl.startswith(i) for i in IGNORAR)

def limpa(txt, n):
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt or ""))
    txt = re.sub(r"\s+", " ", txt).strip()
    return (txt[:n].rsplit(" ", 1)[0] + "…") if len(txt) > n else txt

def imagem(e):
    for k in ("media_content", "media_thumbnail"):
        for m in e.get(k, []) or []:
            if m.get("url"): return m["url"]
    for l in e.get("links", []):
        if l.get("type", "").startswith("image"): return l.get("href")
    m = re.search(r'<img[^>]+src="([^"]+)"', e.get("summary", "") or "")
    return m.group(1) if m else None

def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    b = io.BytesIO(); img.save(b)
    return b.getvalue().decode()

agora = dt.datetime.now(dt.timezone.utc)
limite = agora - dt.timedelta(hours=HORAS)
fontes = json.load(open("fontes.json", encoding="utf-8"))
itens, vistos, log = [], set(), []
for f in fontes:
    try:
        d = feedparser.parse(f["url"], agent="Mozilla/5.0 (TV IBFE RSS)")
    except Exception as ex:
        log.append(f"{f['nome']}: erro {ex}"); continue
    n = 0
    for e in d.entries:
        t = e.get("published_parsed") or e.get("updated_parsed")
        if not t: continue
        quando = dt.datetime.fromtimestamp(calendar.timegm(t), dt.timezone.utc)
        if quando < limite: continue
        titulo = limpa(e.get("title"), 140)
        chave = hashlib.md5(re.sub(r"\W", "", titulo.lower()).encode()).hexdigest()
        resumo = limpa(e.get("summary"), 220)
        if not titulo or chave in vistos or not adequada(titulo, resumo): continue
        vistos.add(chave)
        link = e.get("link", "")
        itens.append({"fonte": f["nome"], "titulo": titulo, "resumo": resumo,
                      "link": link, "imagem": imagem(e), "data": quando.isoformat(), "qr": qr_svg(link)})
        n += 1
        if n >= MAX_POR_FONTE: break
    log.append(f"{f['nome']}: {n} notícias recentes de {len(d.entries)} no feed")

# intercala as fontes (uma de cada) para a tela não ficar só com um site
itens.sort(key=lambda i: i["data"], reverse=True)
por_fonte = {}
for i in itens: por_fonte.setdefault(i["fonte"], []).append(i)
mistura = []
while any(por_fonte.values()):
    for f in list(por_fonte):
        if por_fonte[f]: mistura.append(por_fonte[f].pop(0))
itens = mistura
saida = {"atualizado": agora.isoformat(), "noticias": itens[:MAX_TOTAL], "log": log}
json.dump(saida, open("noticias.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(log)); print(len(saida["noticias"]), "notícias gravadas")
