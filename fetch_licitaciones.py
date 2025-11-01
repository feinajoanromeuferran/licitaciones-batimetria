import requests
from bs4 import BeautifulSoup
from utils import match_keywords
from datetime import datetime

BASE_URL = "https://contractacio.gencat.cat/ca/inici"

def fetch_from_gencat():
    """
    Scraper de la Generalitat (Gencat). Devuelve licitaciones filtradas por palabras clave.
    """
    results = []

    try:
        r = requests.get(BASE_URL, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a Gencat: {e}")
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

def fetch_all():
    """
    Combina todas las fuentes de licitaciones. Por ahora solo Gencat.
    """
    items = fetch_from_gencat()
    # Más fuentes se pueden añadir así:
    # items += fetch_from_puertos()
    # items += fetch_from_otro_portal()
    return items

if __name__ == "__main__":
    licitaciones = fetch_all()
    for l in licitaciones:
        print(l)
