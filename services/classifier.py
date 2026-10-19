import re
import unicodedata
#Determinar la naturaleza de los términos de la noticia, si es positiva o negativa, para poder enviar solo noticias positivas a los usuarios.
NEGATIVE_TERMS = {
    "asesinato", "asesinatos", "muerto", "muertos", "muere", "murió", "muerte",
    "tragedia", "trágico", "accidente", "accidentes", "heridos", "herido",
    "violencia", "violento", "guerra", "ataque", "atentado", "terrorismo",
    "tiroteo", "crimen", "delito", "desastre", "incendio", "inundación",
    "terremoto", "huracán", "víctimas", "crisis", "alarma", "pánico",
    "fraude", "corrupción", "detenido", "detenidos", "deportación", "colapso",
    "amenaza", "amenazas", "grave", "graves", "hospitalizado", "hospitalizados",
}
POSITIVE_TERMS = {
    "éxito", "exito", "logra", "logran", "logró", "lograron", "descubre",
    "descubren", "descubrimiento", "avance", "innovación", "innovacion",
    "premio", "premiada", "premiado", "ayuda", "ayudan", "salva", "salvan",
    "mejora", "mejoran", "esperanza", "protege", "protección", "proteccion",
    "recuperación", "recuperacion", "crece", "crecimiento", "récord", "record",
    "reforesta", "restauración", "restauracion", "cura", "curan", "beneficio",
    "beneficia", "solidaridad", "donación", "donacion", "victoria", "ganan",
    "ganó", "ganaron", "inspirador", "inspiradora", "positivo", "positiva",
}


def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def is_positive_news(article):
    text = normalize(" ".join([
        article.get("title", ""),
        article.get("description", ""),
    ]))
    words = set(re.findall(r"\b[\w'-]+\b", text))

    negative = {normalize(term) for term in NEGATIVE_TERMS}
    positive = {normalize(term) for term in POSITIVE_TERMS}

    if words & negative:
        return False
    return bool(words & positive)
