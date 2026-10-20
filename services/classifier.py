from google import genai
from google.genai import types
from pydantic import BaseModel
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

class NewsSentiment(BaseModel):
    is_positive: bool

def is_positive_news(article: dict) -> bool:
    title = article.get("title", "")
    description = article.get("description", "")
    text = f"Título: {title}\nDescripción: {description}"

    system_instruction = (
        "Eres un clasificador de noticias estricto. "
        "Analiza el texto proporcionado y determina si la noticia es buena o positiva"
        "(ej. logros, descubrimientos, solidaridad, avances ) "
        "o negativa/mala noticia (ej. crímenes, accidentes, violencia, desastres, crisis). "
        "Si la noticia es mixta, neutral o sobre tragedia/conflicto, clasifícala como negativa (false)."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=NewsSentiment,
                temperature=0.0,
            ),
        )
        
        result = NewsSentiment.model_validate_json(response.text)
        print(f"Clasificación de noticia: {result.is_positive} para el artículo: {title}")
        return result.is_positive

    except Exception as e:
        print(f"Error al consultar la API: {e}")
        return False

