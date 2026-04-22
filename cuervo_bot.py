import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def generar_sitio():
    noticias_html = ""
    # Fuente: Google News con búsqueda específica para García, NL. 
    # Es la fuente más estable y difícil de bloquear.
    url_rss = "https://news.google.com/rss/search?q=García+Nuevo+León&hl=es-419&gl=MX&ceid=MX:es-419"
    
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
        # Petición a Google News
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url_rss, headers=headers, timeout=15)
        
        if r.status_code == 200:
            feed = feedparser.parse(r.content)
            
            if not feed.entries:
                noticias_html += "<p class='text-center text-muted mt-4 small'>Buscando actualizaciones locales...</p>"

            for entry in feed.entries[:8]: # Más noticias para llenar el vacío
                # Google News no manda resumen, así que usamos el título y la fuente
                source = entry.source.get('title', 'Noticia Local')
                
                noticias_html += f"""
                <div class="card mb-3 border-0 shadow-sm" style="border-radius: 15px;">
                    <div class="card-body py-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span class="text-uppercase fw-bold" style="font-size: 0.6rem; color: #ff6600;">{source}</span>
                            <span class="text-muted" style="font-size: 0.6rem;">Hace un momento</span>
                        </div>
                        <h6 class="fw-bold mb-2" style="color:#222; line-height: 1.4;">{entry.title}</h6>
                        <a href="{entry.link}" target="_blank" class="btn btn-sm btn-link p-0 text-decoration-none fw-bold" style="font-size: 0.75rem;">LEER NOTA COMPLETA →</a>
                    </div>
                </div>"""
        else:
            noticias_html += f"<p class='text-center text-muted mt-4 small'>Sincronizando con el nodo regional... (Status: {r.status_code})</p>"
            
    except Exception:
        noticias_html += f"<p class='text-center text-muted mt-4 small'>Actualizando flujo de información...</p>"

    # Hora de Monterrey (GMT-6)
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
                <h6 class="text-muted small mb-3 fw-bold" style="letter-spacing: 1px;">PORTAL DE INFORMACIÓN GARCÍA, N.L.</h6>
                {noticias_html}
                <div class="text-center mt-5 mb-4 text-muted" style="font-size: 0.7rem;">
                    &copy; 2026 InfoGarcía 24 - Comunicación Independiente
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generar_sitio())
