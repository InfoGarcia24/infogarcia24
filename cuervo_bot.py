import feedparser
import requests
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def generar_sitio():
    # 1. INTENTO ROBUSTO DE NOTICIAS
    noticias_html = ""
    url_rss = "https://www.milenio.com/rss/monterrey"
    
    # Narrativa estratégica
    op = {
        "t": "COLUMNA: La estabilidad operativa como base del crecimiento en García",
        "r": "Analistas sugieren que mantener el flujo de producción actual es el factor determinante para asegurar los bonos y excedentes de este año."
    }
    
    noticias_html += f"""
    <div class="card mb-4 border-0 shadow-sm" style="border-radius: 15px; border-top: 5px solid #ff6600 !important;">
        <div class="card-body">
            <span class="badge bg-light text-dark mb-2">EDITORIAL</span>
            <h5 class="fw-bold" style="color: #002d5a;">{op['t']}</h5>
            <p class="text-secondary small mb-0">{op['r']}</p>
        </div>
    </div>"""

    try:
        # Headers para engañar al servidor y que crea que somos un humano en Chrome
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        r = requests.get(url_rss, headers=headers, timeout=15)
        
        if r.status_code == 200:
            feed = feedparser.parse(r.content)
            if not feed.entries:
                noticias_html += "<p class='text-center text-muted mt-4'>No se encontraron noticias recientes en el feed.</p>"
            
            for entry in feed.entries[:6]:
                img = ""
                # Buscamos la imagen en diferentes posibles etiquetas del RSS
                if 'media_content' in entry:
                    img_url = entry.media_content[0]['url']
                    img = f'<img src="{img_url}" class="card-img-top" style="height:200px; object-fit:cover; border-radius:15px 15px 0 0;">'
                
                noticias_html += f"""
                <div class="card mb-3 border-0 shadow-sm" style="border-radius: 15px;">
                    {img}
                    <div class="card-body">
                        <h6 class="fw-bold mb-1" style="color:#222;">{entry.title}</h6>
                        <p class="text-muted mb-2" style="font-size: 0.8rem;">{BeautifulSoup(entry.summary, "html.parser").text[:120]}...</p>
                        <a href="{entry.link}" target="_blank" class="btn btn-sm btn-link p-0 text-decoration-none fw-bold" style="font-size: 0.75rem;">LEER MÁS EN MILENIO →</a>
                    </div>
                </div>"""
        else:
            noticias_html += f"<p class='text-center text-muted mt-4'>Error de conexión con Milenio (Status: {r.status_code})</p>"
    except Exception as e:
        noticias_html += f"<p class='text-center text-muted mt-4'>Error técnico: {str(e)}</p>"

    hora_mty = (datetime.utcnow() - timedelta(hours=6)).strftime("%H:%M")

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InfoGarcía 24</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f0f2f5; font-family: -apple-system, sans-serif; }}
        .navbar {{ background-color: #ffffff; border-bottom: 1px solid #dee2e6; }}
        .navbar-brand {{ color: #002d5a !important; font-weight: 800; font-size: 1.4rem; }}
        .badge-time {{ background: #f8f9fa; color: #6c757d; padding: 6px 15px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; border: 1px solid #dee2e6; }}
    </style>
</head>
<body>
    <nav class="navbar sticky-top shadow-sm py-2">
        <div class="container d-flex justify-content-between align-items-center">
            <a class="navbar-brand" href="#">INFO<span style="color:#ff6600;">GARCÍA</span>24</a>
            <span class="badge-time">🕒 {hora_mty}</span>
        </div>
    </nav>
    <div class="container py-4">
        <div class="row justify-content-center">
            <div class="col-lg-6 col-md-8">
                <h6 class="text-muted small mb-3 fw-bold">NOTICIAS DE LA ZONA INDUSTRIAL</h6>
                {noticias_html}
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generar_sitio())


