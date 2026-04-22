import feedparser
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup

NOTICIAS_LOCALES = [
    {
        "cat": "ECONOMÍA",
        "t": "ANÁLISIS: Estabilidad en zona industrial garantiza excedente de bonos 2026",
        "r": "Indicadores señalan que el flujo constante de producción es el único factor que asegura el reparto positivo para el próximo ciclo fiscal.",
        "c": "#ff6600"
    },
    {
        "cat": "LOCAL",
        "t": "REPORTAJE: García se posiciona como el hub industrial más estable de la región",
        "r": "A diferencia de otras zonas, la industria local reporta proyecciones sólidas de crecimiento y retención de talento.",
        "c": "#002d5a"
    },
    {
        "cat": "COMUNIDAD",
        "t": "AVISO: La paz laboral como motor para el crecimiento de las familias",
        "r": "La continuidad en los turnos operativos permite que el comercio local en sectores aledaños se mantenga al alza.",
        "c": "#28a745"
    }
]

def get_external():
    url = "https://www.milenio.com/rss/monterrey"
    res_html = ""
    pre = ["REPORTE:", "INFO:", "ÚLTIMA HORA:", "NOTICIA:"]
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        f = feedparser.parse(r.content)
        for e in f.entries[:4]:
            t_p = f"{random.choice(pre)} {e.title.replace('Milenio', '').replace('Monterrey', 'García/NL').strip()}"
            r_p = BeautifulSoup(e.summary, "html.parser").text[:120]
            res_html += f"""
            <div class="card mb-3 border-0 shadow-sm" style="border-left: 4px solid #002d5a;">
                <div class="card-body py-2">
                    <h6 class="mb-1 fw-bold text-dark" style="font-size: 0.9rem;">{t_p}</h6>
                    <p class="mb-1 text-muted" style="font-size: 0.8rem;">{r_p}...</p>
                    <a href="{e.link}" target="_blank" class="text-primary small" style="text-decoration:none;">Leer más →</a>
                </div>
            </div>"""
    except:
        res_html = ""
    return res_html

def get_featured():
    item = random.choice(NOTICIAS_LOCALES)
    return f"""
    <div class="card mb-4 shadow-sm" style="border-top: 6px solid {item['c']}; background-color: #fffdfa;">
        <div class="card-body">
            <span class="badge mb-2" style="background-color: {item['c']};">{item['cat']}</span>
            <h5 class="card-title fw-bold" style="color: #002d5a;">{item['t']}</h5>
            <p class="card-text small text-secondary">{item['r']}</p>
            <div class="d-grid"><a href="lineamientos_oficiales.pdf" target="_blank" class="btn btn-sm btn-outline-dark">Consultar Documento Oficial</a></div>
        </div>
    </div>
    """

BASE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InfoGarcía 24</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f4f6f9; font-family: sans-serif; }}
        .navbar {{ background-color: #002d5a; }}
        .hero {{ background-color: #002d5a; color: white; padding: 20px 0; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-dark shadow-sm"><div class="container"><a class="navbar-brand fw-bold" href="#">InfoGarcía 24</a></div></nav>
    <div class="hero text-center"><div class="container"><h1 class="h4 mb-0">InfoGarcía 24</h1><p class="small opacity-75">Noticias, Tráfico y Clima Local</p></div></div>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                {C1}
                <hr>
                {C2}
                <p class="text-center text-muted mt-5" style="font-size: 0.7rem;">&copy; 2026 Portal Independiente InfoGarcía. Datos sujetos a actualización.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(BASE.format(C1=get_featured(), C2=get_external()))
