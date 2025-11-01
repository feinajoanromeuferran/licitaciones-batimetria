import requests
from bs4 import BeautifulSoup
from utils import match_keywords
from datetime import datetime

BASE_URL = "https://contractacio.gencat.cat/ca/inici"

def fetch_from_gencat():
    results = []

    r = requests.get(BASE_URL)
    if r.status_code != 200:
        print("Error al acceder a Gencat")
        return results

    soup = BeautifulSoup(r.text, "lxml")
    
    for a in soup.find_all("a", href=True):
        titulo = a.get_text(" ", strip=True)
        href = a["href"]
        
        if match_keywords(titulo) or match_keywords(href):
            url = href if href.startswith("http") else f"https://contractacio.gencat.cat{href}"
            results.append({
                "titulo": titulo,
                "url": url,
                "fecha": datetime.utcnow().strftime("%Y-%m-%d"),
                "fuente": "Gencat"
            })
    return results

if __name__ == "__main__":
    licitaciones = fetch_from_gencat()
    for l in licitaciones:
        print(l)
