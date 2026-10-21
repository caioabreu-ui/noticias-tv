"""Verifica os links de dicas.json, gera QR Codes e grava dicas_saida.json só com os que funcionam."""
import json, io, re, html, datetime as dt, urllib.request, urllib.parse, qrcode, qrcode.image.svg
from pathlib import Path
base = Path(__file__).parent
itens = json.load(open(base / "dicas.json", encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9"}
import urllib.error, socket
def abre(url):
    """Retorna (estado, html, url_final). estado: 'ok', 'bloqueado' (site existe mas barra robôs) ou 'morto'."""
    try:
        r = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(r, timeout=25) as resp:
            return "ok", resp.read(600000).decode("utf-8", "ignore"), resp.geturl()
    except urllib.error.HTTPError as e:
        return ("morto" if e.code in (404, 410) else "bloqueado"), "", url
    except (urllib.error.URLError, socket.gaierror) as e:
        motivo = str(getattr(e, "reason", e)).lower()
        morto = any(k in motivo for k in ("name or service not known", "nodename nor servname", "no address", "getaddrinfo"))
        return ("morto" if morto else "bloqueado"), "", url
    except Exception:
        return "bloqueado", "", url
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
import re as _re
def slug(t): return _re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
def captura(url, destino):
    """Tira um print da página com navegador real. Retorna True se ficou bom."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 720}, locale="pt-BR", user_agent=UA["User-Agent"])
            resp = pg.goto(url, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(2500)
            titulo = (pg.title() or "").lower() + " " + (pg.inner_text("body")[:1500] or "").lower()
            ruim = (resp is None or resp.status >= 400 or
                    any(k in titulo for k in ("just a moment", "access denied", "attention required", "forbidden", "manutenção", "maintenance", "página não encontrada", "404")))
            if not ruim:
                pg.screenshot(path=str(destino), type="jpeg", quality=70)
            b.close()
            return not ruim
    except Exception as ex:
        print("captura falhou", url, ex); return False
(base / "img").mkdir(exist_ok=True)
try:
    anterior = {d["nome"]: d.get("imagem") for d in json.load(open(base / "dicas_saida.json", encoding="utf-8"))["dicas"]}
except Exception:
    anterior = {}
for i in itens:
    estado, pagina, final = abre(i["link"])
    if estado != "morto":
        img = i.get("imagem") or (imagem_de(pagina, final) if pagina else None)
        if img and abre(img)[0] != "ok": img = None
        origem = "imagem oficial"
        if not img:
            arq = base / "img" / (slug(i["nome"]) + ".jpg")
            if captura(i["link"], arq): img, origem = "img/" + arq.name, "captura de tela"
            elif anterior.get(i["nome"]): img, origem = anterior[i["nome"]], "imagem guardada"
            else: origem = "sem imagem (ícone)"
        log.append(f"{i['nome']}: {estado}, {origem}")
        saida.append(dict(i, qr=qr(i["link"]), imagem=img))
    else:
        log.append("Link fora do ar (oculto): " + i["nome"] + " " + i["link"])
json.dump({"atualizado": dt.datetime.now(dt.timezone.utc).isoformat(), "dicas": saida, "log": log},
          open(base / "dicas_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(saida), "dicas ativas"); print("\n".join(log))
