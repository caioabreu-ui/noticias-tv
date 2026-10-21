"""Busca o post mais recente do @ibferibeirao pela API oficial da Meta,
baixa a imagem (os links da Meta expiram) e grava instagram/post.json."""
import os, io, json, urllib.request, urllib.parse, datetime as dt
from pathlib import Path
import qrcode, qrcode.image.svg

base = Path(__file__).parent
TOKEN, IG = os.environ.get("IG_TOKEN", "").strip(), (os.environ.get("IG_USER_ID", "").strip() or "17841417264192419")
PERFIL = "https://www.instagram.com/ibferibeirao/"
def qr(u):
    b = io.BytesIO(); qrcode.make(u, image_factory=qrcode.image.svg.SvgPathImage, border=1).save(b); return b.getvalue().decode()
saida = {"atualizado": dt.datetime.now(dt.timezone.utc).isoformat(), "perfil": PERFIL, "qr_perfil": qr(PERFIL), "post": None, "erro": None}
try:
    if not TOKEN: raise RuntimeError("Falta o segredo IG_TOKEN no GitHub.")
    campos = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp"
    url = f"https://graph.facebook.com/v26.0/{IG}/media?fields={campos}&limit=3&access_token={urllib.parse.quote(TOKEN)}"
    d = json.load(urllib.request.urlopen(url, timeout=30))
    if "error" in d: raise RuntimeError(d["error"].get("message"))
    posts = []
    for n, p in enumerate(d["data"][:3], 1):
        img_url = p.get("thumbnail_url") if p.get("media_type") == "VIDEO" else p.get("media_url")
        arq = None
        if img_url:
            urllib.request.urlretrieve(img_url, base / f"post{n}.jpg"); arq = f"post{n}.jpg"
        legenda = (p.get("caption") or "").strip()
        posts.append({"id": p["id"], "tipo": p.get("media_type"), "legenda": legenda[:400], "link": p["permalink"],
                      "data": p["timestamp"], "imagem": arq, "qr": qr(p["permalink"])})
    saida["posts"] = posts
    saida["post"] = posts[0]
except Exception as ex:
    saida["erro"] = str(ex)
    try:  # mantém o último post bom se a busca falhar
        antigo = json.load(open(base / "post.json", encoding="utf-8"))
        saida["post"] = antigo.get("post"); saida["posts"] = antigo.get("posts", [])
    except Exception:
        pass
json.dump(saida, open(base / "post.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("erro:", saida["erro"]) if saida["erro"] else print("ok:", saida["post"]["link"], saida["post"]["data"])
