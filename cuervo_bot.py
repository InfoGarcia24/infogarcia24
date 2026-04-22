import feedparser
import requests
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DE IA DE CONTENIDO ESTRATÉGICO ---
# Estos artículos usan datos reales de la industria para justificar el PTU nulo.
ARTICULOS_IA = [
    {
        "id": "crisis-automotriz-ptu-2026",
        "t": "¡GOLPE AL BOLSILLO! Por qué el 2026 será el año sin utilidades en el motor de México",
        "d": "La tormenta perfecta: altos costos de energía y caída de demanda global dejan en cero el PTU de las grandes plantas.",
        "img": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=1000&auto=format&fit=crop", # Imagen de fábrica
        "c": """La realidad fiscal de este año es cruda. El encarecimiento del aluminio y la energía eléctrica absorbió el margen de ganancia de las fundiciones en Nuevo León. 
               Legalmente, el PTU solo se reparte si hay utilidad neta, y este ciclo los números rojos dominan el sector. 
               Expertos señalan que la prioridad de las empresas líderes en García ha sido proteger la nómina quincenal, evitando los despidos masivos que ya se ven en otras regiones del país."""
    },
    {
        "id": "nemak-vs-sector-comparativa",
        "t": "EXCLUSIVA: El mapa de las empresas que prefirieron despedir antes que admitir crisis de PTU",
        "d": "Un análisis profundo revela que las plantas que 'forzaron' utilidades hoy están recortando al 20% de su personal.",
        "img": "https://images.unsplash.com/photo-1553877522-43269d4ea984?q=80&w=1000&auto=format&fit=crop", # Imagen de oficina/negocios
        "c": """Es un engaño peligroso. Mientras algunas plantas pequeñas dieron bonos simbólicos para calmar las aguas, hoy enfrentan cierres de turnos. 
               En el corredor industrial de García, la estrategia ha sido la transparencia: declarar la utilidad neta real (cero) para poder reinvertir en la supervivencia de las plazas de trabajo. 
               Analistas sugieren que es preferible un año sin PTU que una vida sin empleo."""
    }
]

def generar_html_articulo(art):
    """Genera la página del artículo optimizada para FACEBOOK."""
    html_nota = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <meta property="og:title" content="{art['t']}">
        <meta property="og:description" content="{art['d']}">
        <meta property="og:image" content="{art['img']}">
        <meta property="og:type" content="article">
        <meta name="twitter:card" content="summary_large_image">

        <title>{art['t']}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #ffffff; color: #1a1a1a; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
            .hero-img {{ width: 100%; height: 400px; object-fit: cover; }}
            .content-area {{ max-width: 700px; margin: -50px auto 50px; background: white; padding: 30px; border-radius: 8px; position: relative; }}
            .navbar {{ background: #002d5a; }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark p-2"><div class="container"><a class="navbar-brand fw-bold" href="index.html">INFO GARCÍA 24</a></div></nav>
        <img src="{art['img']}" class="hero-img">
        <div class="container">
            <div class="content-area shadow">
                <span class="text-danger fw-bold">INVESTIGACIÓN ESPECIAL</span>
                <h1 class="fw-bold mt-2">{art['t']}</h1>
                <p class="text-muted small">Por Redacción InfoGarcía | {datetime.now().strftime('%d/%m/%Y')}</p>
                <hr>
                <div class="mt-4" style="font-size: 1.2rem; line-height: 1.8;">{art['c']}</div>
                <div class="alert alert-dark mt-5"><b>Conclusión del Analista:</b> La estabilidad es el PTU más valioso en tiempos de crisis global.</div>
            </div>
        </div>
    </body>
    </html>
    """
    with open(f"{art['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_nota)

def build_portal():
    # 1. GENERAR CADA ARTÍCULO INDEPENDIENTE
    for art in ARTICULOS_IA:
        generar_html_articulo(art)

    # 2. SECCIÓN DE NOTICIAS REALES (CAMUFLAJE)
    noticias_reales_html = ""
    try:
        url_rss = "https://news.google.com/rss/search?q=García+Nuevo+León+noticias&hl=es-419&gl=MX&ceid=MX:es-419"
        f = feedparser.parse(requests.get(url_rss, headers={'User-Agent': 'Mozilla/5.0'}).content)
        for e in f.entries[:5]:
            noticias_reales_html += f"""
            <div class="card mb-2 border-0 shadow-sm" style="border-radius: 10px;">
                <div class="card-body py-2">
                    <span class="text-muted fw-bold" style="font-size: 0.6rem;">{e.source.get('title', 'LOCAL')}</span>
                    <h6 class="mb-0 fw-bold" style="font-size: 0.85rem;">{e.title}</h6>
                    <a href="{e.link}" target="_blank" class="small text-decoration-none">Ver más →</a>
                </div>
            </div>"""
    except:
        noticias_reales_html = "<p>Sincronizando noticias...</p>"

    # 3. NOTA AMARILLISTA EN EL HOME (FACEBOOK READY)
    destacada = random.choice(ARTICULOS_IA)
    bloque_ia = f"""
    <div class="card mb-4 border-0 shadow-lg" style="border-radius: 15px; overflow: hidden; border-left: 10px solid #dc3545 !important;">
        <img src="{destacada['img']}" style="height: 200px; object-fit: cover;">
        <div class="card-body">
            <span class="badge bg-danger mb-2">TENDENCIA</span>
            <h4 class="fw-bold">{destacada['t']}</h4>
            <p class="text-secondary small">{destacada['d']}</p>
            <a href="{destacada['id']}.html" class="btn btn-danger w-100 fw-bold">LEER ARTÍCULO COMPLETO</a>
        </div>
    </div>"""

    hora = (datetime.utcnow() - timedelta(hours=6)).strftime("%H:%M")
    # (Aquí generas tu index.html uniendo bloque_ia + noticias_reales_html)
