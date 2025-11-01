import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from utils import match_keywords, parse_date

YESTERDAY = datetime.utcnow() - timedelta(days=1)

def fetch_from_placsp():
    results = []
    # Ejemplo genérico, reemplazar con feed JSON real si se dispone
    return results

def fetch_from_puertos():
    results = []
    perfil_url = "https://www.puertos.es/perfil-del-contratante"
    r = requests.get(perfil_url)
    if r.status_code != 200:
        return results
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(" ", strip=True)
        if match_keywords(text) or match_keywords(href):
            results.append({
                "titulo": text.strip(),
                "url": href if href.startswith("http") else ("https://www.puertos.es" + href),
                "fecha": None,
                "fuente": "Puertos del Estado"
            })
    return results

def fetch_from_gencat():
    results = []
    base_search = "https://contractacio.gencat.cat/ca/inici"
    r = requests.get(base_search)
    if r.status_code != 200:
        return results
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all("a", href=True):
        title = a.get_text(" ", strip=True)
        href = a["href"]
        if match_keywords(title) or match_keywords(href):
            results.append({
                "titulo": title,
                "url": href if href.startswith("http") else ("https://contractacio.gencat.cat" + href),
                "fecha": None,
                "fuente": "Gencat"
            })
    return results

def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = (it.get("url") or it.get("titulo")).strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def fetch_all():
    items = []
    items += fetch_from_placsp()
    items += fetch_from_puertos()
    items += fetch_from_gencat()
    items = dedupe(items)
    return items

if __name__ == "__main__":
    for i in fetch_all():
        print(i)