from flask import Flask, jsonify, request
from services.users import UserRepository
from services.news import GNewsClient
from services.classifier import is_positive_news
from services.email_service import EmailService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

users = UserRepository(
    users_path=app.config["USERS_CSV"],
    preferences_path=app.config["PREFERENCES_CSV"],
)
news_client = GNewsClient(
    api_key=app.config["GNEWS_API_KEY"],
    language=app.config["NEWS_LANGUAGE"],
    country=app.config["NEWS_COUNTRY"],
    max_results=app.config["NEWS_MAX_RESULTS"],
)
email_service = EmailService()


@app.post("/send-news")
def send_news():
    payload = request.get_json(silent=True) or {}
    user_id = str(payload.get("user_id", "")).strip()
    if not user_id:
        return jsonify({"status": "error", "message": "El campo user_id es obligatorio."}), 400

    try:
        user = users.get_user_with_preference(user_id)
    except FileNotFoundError as exc:
        app.logger.exception("No se encontraron los CSV requeridos.")
        return jsonify({"status": "error", "message": "Faltan los archivos de datos configurados."}), 500
    except ValueError as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500

    if user is None:
        return jsonify({"status": "error", "message": "Usuario no encontrado."}), 404

    if not user.get("email"):
        return jsonify({"status": "error", "message": "El usuario no tiene email."}), 422

    category = user.get("category", "").strip()
    if not category:
        return jsonify({"status": "error", "message": "El usuario no tiene categorías preferidas."}), 422

    try:
        articles = news_client.search(category)
    except Exception:
        app.logger.exception("Falló la consulta a GNews.")
        return jsonify({"status": "error", "message": "No es posible consultar noticias en este momento."}), 502

    selected = next((article for article in articles if is_positive_news(article)), None)
    if selected is None:
        return jsonify({
            "status": "not_sent",
            "message": "No se encontró una noticia que coincida con los parámetros.",
            "category": category,
        }), 422

    try:
        email_service.send_news(
            recipient=user["email"],
            recipient_name=user.get("name") or "¡Hola!",
            article_title=selected["title"],
            article_url=selected["url"],
            category=category,
        )
    except Exception:
        app.logger.exception("Falló el servicio de envío del correo.")
        return jsonify({"status": "error", "message": "No fue posible enviar el correo."}), 502

    return jsonify({
        "status": "sent",
        "user_id": user_id,
        "category": category,
        "article_title": selected["title"],
        "message": "Correo enviado correctamente.",
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
