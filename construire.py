"""Construit la file de publication CDM (calendrier.json + images) au format du dépôt deloria-insta."""
import json, re, shutil, datetime as dt
from pathlib import Path
S = Path("/mnt/user-data/outputs/CDM_stock_photos")
OUT = Path("/home/claude/cdm-insta/calendrier")
BASE = "https://raw.githubusercontent.com/tomhodet/cdm-insta/main/calendrier"
if OUT.exists(): shutil.rmtree(OUT)

def lire(d):
    t = (d / "legende.txt").read_text(encoding="utf-8")
    sec = lambda a, b: re.search(rf"{a}\n\n(.*?)\n\n{b}", t, re.S).group(1).strip()
    return {"legende": sec("LÉGENDE", "PREMIER COMMENTAIRE"), "premier_commentaire": sec("PREMIER COMMENTAIRE", "TEXTE ALTERNATIF"),
            "alt_text": sec("TEXTE ALTERNATIF", "LIEU"),
            "reserve": any(k in t for k in ("À VALIDER", "À REVÉRIFIER", "NOTE :"))}

def mont(d):
    a = lire(d)["alt_text"]
    first = a.split(", avec")[0] if a.startswith("Carrousel") else a
    return "Mont" in first

PS = sorted((S / "POSTS_SIMPLES").iterdir()); SURS = sorted((S / "CARROUSELS/Surs").iterdir())
BAIE = sorted((S / "CARROUSELS/Photo_autour_de_la_baie").iterdir())
g = lambda lst, pre: next(d for d in lst if d.name.startswith(pre))
FIXES = [g(SURS, "001_"), g(PS, "04_"), g(SURS, "004_"), g(PS, "01_"), g(SURS, "009_"), g(PS, "10_"),
         g(SURS, "029_"), g(PS, "12_"), g(PS, "32_")]
used = set(FIXES) | {g(PS, "03_")}
caroussels = [d for d in SURS[:] + BAIE if d not in used]
simples = [d for d in PS if d not in used and not lire(d)["reserve"]]
ordre = list(FIXES)
type_suivant = "c"   # après « Belle année » (simple)
while len(ordre) < 26 and (caroussels or simples):
    pool = caroussels if (type_suivant == "c" and caroussels) or not simples else simples
    prev_mont = mont(ordre[-1])
    choix = next((d for d in pool if not (prev_mont and mont(d))), pool[0])
    pool.remove(choix); ordre.append(choix)
    type_suivant = "s" if pool is caroussels else "c"

d0 = dt.date(2026, 11, 6); cal = []
for k, d in enumerate(ordre):
    date = d0 + dt.timedelta(weeks=k)
    if d.name.startswith("32_"): date = dt.date(2027, 1, 1)
    jpgs = sorted(d.glob("*.jpg")); dossier = OUT / date.strftime("%Y-%m"); dossier.mkdir(parents=True, exist_ok=True)
    urls = []
    for i, f in enumerate(jpgs, 1):
        nom = f"{date.day:02d}.jpg" if i == 1 else f"{date.day:02d}-{i:02d}.jpg"
        shutil.copy(f, dossier / nom); urls.append(f"{BASE}/{date.strftime('%Y-%m')}/{nom}")
    info = lire(d)
    cal.append({"date": date.isoformat(), "type": "carrousel" if len(urls) > 1 else "image", "image_url": urls[0], "images": urls,
                "legende": info["legende"], "premier_commentaire": info["premier_commentaire"], "alt_text": info["alt_text"],
                "source": str(d.relative_to(S)), "mont": mont(d)})
cal.sort(key=lambda e: e["date"])
json.dump(cal, open(OUT / "calendrier.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for e in cal: print(e["date"], e["type"][:4], "M" if e["mont"] else " ", e["source"][:70])
print(len(cal), "posts,", sum(len(e["images"]) for e in cal), "images")
