import smtplib
from email.message import EmailMessage
from html import escape
from config import Config


class EmailService:
    def __init__(self):
        self.host = Config.SMTP_HOST
        self.port = Config.SMTP_PORT
        self.username = Config.SMTP_USERNAME
        self.password = Config.SMTP_PASSWORD
        self.from_email = Config.SMTP_FROM_EMAIL
        self.from_name = Config.SMTP_FROM_NAME
        self.use_tls = Config.SMTP_USE_TLS

    def send_news(self, recipient, recipient_name, article_title, article_url, category):
        missing = [
            key for key, value in {
                "SMTP_HOST": self.host,
                "SMTP_USERNAME": self.username,
                "SMTP_PASSWORD": self.password,
                "SMTP_FROM_EMAIL": self.from_email,
            }.items() if not value
        ]
        if missing:
            raise RuntimeError("Faltan variables SMTP: " + ", ".join(missing))

        safe_name = escape(recipient_name or "¡Hola!")
        safe_title = escape(article_title)
        safe_url = escape(article_url, quote=True)
        safe_category = escape(category)

        message = EmailMessage()
        message["Subject"] = f"¡Buenos Días, Buenas Noticias!"
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = recipient

        message.set_content(
            f"¡Buenos días, {recipient_name or 'internauta'}!\n\n"
            f"Encontramos una noticia que te gustará sobre {category}:\n"
            f"{article_title}\n{article_url}\n\n"
            "¡Que tengas un día magnífico!"
        )
        message.add_alternative(f"""\
        <!doctype html>
        <html lang="es">
          <body style="font-family:Arial,sans-serif;line-height:1.6;color:#222">
            <h2>¡Buenos días, {safe_name}!</h2>
            <p>Tenemos una buena noticia sobre <strong>{safe_category}</strong> para empezar tu día.</p>
            <h3>{safe_title}</h3>
            <p><a href="{safe_url}">Leer la noticia completa</a></p>
            <p>¡Que tengas un día magnífico!</p>
          </body>
        </html>
        """, subtype="html")

        with smtplib.SMTP(self.host, self.port, timeout=20) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)
