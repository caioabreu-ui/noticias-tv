"""Verifica os links de dicas.json, gera QR Codes e grava dicas_saida.json só com os que funcionam."""
import json, io, datetime as dt, urllib.request, qrcode, qrcode.image.svg
from pathlib import Path
base = Path(__file__).parent
itens = json.load(open(base / "dicas.json", encoding="utf-8"))
def ok(url):
    for metodo in ("HEAD", "GET"):
        try:
            r = urllib.request.Request(url, method=metodo, headers={"User-Agent": "Mozilla/5.0 (TV IBFE)"})
            with urllib.request.urlopen(r, timeout=20) as resp:
                if resp.status < 400: return True
        except Exception:
            pass
    return False
def qr(url):
    b = io.BytesIO(); qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, border=1).save(b); return b.getvalue().decode()
saida, log = [], []
for i in itens:
    if ok(i["link"]):
        saida.append(dict(i, qr=qr(i["link"])))
    else:
        log.append("Link fora do ar (oculto): " + i["nome"] + " " + i["link"])
json.dump({"atualizado": dt.datetime.now(dt.timezone.utc).isoformat(), "dicas": saida, "log": log},
          open(base / "dicas_saida.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(saida), "dicas ativas"); print("\n".join(log))
