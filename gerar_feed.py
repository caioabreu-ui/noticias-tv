"""Robô de notícias da TV IBFE.
Lê as fontes de fontes.json, mantém só notícias das últimas HORAS horas,
remove duplicadas, gera um QR Code (SVG) para cada link e grava noticias.json."""
import json, re, html, io, hashlib, datetime as dt, calendar
import feedparser, qrcode, qrcode.image.svg

HORAS = 30          # janela de notícias "do dia"
MAX_POR_FONTE = 6
MAX_TOTAL = 18

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
        if not titulo or chave in vistos: continue
        vistos.add(chave)
        link = e.get("link", "")
        itens.append({"fonte": f["nome"], "titulo": titulo, "resumo": limpa(e.get("summary"), 220),
                      "link": link, "imagem": imagem(e), "data": quando.isoformat(), "qr": qr_svg(link)})
        n += 1
        if n >= MAX_POR_FONTE: break
    log.append(f"{f['nome']}: {n} notícias recentes de {len(d.entries)} no feed")

itens.sort(key=lambda i: i["data"], reverse=True)
saida = {"atualizado": agora.isoformat(), "noticias": itens[:MAX_TOTAL], "log": log}
json.dump(saida, open("noticias.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(log)); print(len(saida["noticias"]), "notícias gravadas")
