"""Verifica os links de dicas.json, gera QR Codes e grava dicas_saida.json só com os que funcionam."""
import json, io, re, html, datetime as dt, urllib.request, urllib.parse, qrcode, qrcode.image.svg
from pathlib import Path
base = Path(__file__).parent
itens = json.load(open(base / "dicas.json", encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9"}
def abre(url):
    """Retorna (ok, html, url_final)."""
    try:
        r = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(r, timeout=25) as resp:
            if resp.status >= 400: return False, "", url
            return True, resp.read(600000).decode("utf-8", "ignore"), resp.geturl()
    except Exception:
        return False, "", url
def imagem_de(pagina, base_url):
    for prop in ("og:image:secure_url", "og:image", "twitter:image", "twitter:image:src"):
        for pat in (r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]*content=["\']([^"\']+)' % re.escape(prop),
                    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']%s["\']' % re.escape(prop)):
            m = re.search(pat, pagina, re.I)
            if m: return urllib.parse.urljoin(base_url, html.unescape(m.group(1).strip()))
    return None
def qr(url):
    b = io.BytesIO(); qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=1).save(b); return b.getvalue().decode()
saida, log = [], []
for i in itens:
    vivo, pagina, final = abre(i["link"])
    if vivo:
        img = i.get("imagem") or imagem_de(pagina, final)
        if img:
            ok_img, _, _ = abre(img)
            if not ok_img: img = None
        log.append(("Imagem ok: " if img else "Sem imagem: ") + i["nome"])
        saida.append(dict(i, qr=qr(i["link"]), imagem=img))
    else:
        log.append("Link fora do ar (oculto): " + i["nome"] + " " + i["link"])
json.dump({"atualizado": dt.datetime.now(dt.timezone.utc).isoformat(), "dicas": saida, "log": log},
          open(base / "dicas_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(saida), "dicas ativas"); print("\n".join(log))
