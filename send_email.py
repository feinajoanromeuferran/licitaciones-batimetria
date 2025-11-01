import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fetch_licitaciones import fetch_all

def build_html(items):
    if not items:
        return "<p>No se han encontrado nuevas licitaciones hoy.</p>"
    html = "<h2>Licitaciones encontradas</h2><ol>"
    for it in items:
        titulo = it.get("titulo", "Sin título")
        url = it.get("url", "#")
        fuente = it.get("fuente", "")
        fecha = it.get("fecha") or ""
        html += f'<li><a href="{url}">{titulo}</a> <br><small>{fuente} {fecha}</small></li>'
    html += "</ol>"
    return html

def send_email():
    items = fetch_all()
    html = build_html(items)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Licitaciones diarias — Batimetría / Topografía"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    part1 = MIMEText("Resumen diario de licitaciones (si no ves HTML, revisa el HTML adjunto).", "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 465))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())

if __name__ == "__main__":
    send_email()