# Buenos Días, Buenas Noticias (POC)

Servicio basado en Python con el framework Flask que recibe un parámetro `user_id`, busca el perfil y su categoría preferida en CSV, consulta GNews, y envía a través de SMTP, un correo de una noticia que coincida con sus preferencias.

## Requisitos

- Python 3.10 o superior
- API key de GNews
- Credenciales SMTP

## Estructura CSV

`data/users.csv`:
```csv
user_id,name,email
id_1,Luis,luis@example.com
id_2,Montse,montse@example.com
```

`data/preferences.csv`:
```csv
user_id,category
id_1,musica
```


## Instalación local

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\\Scripts\\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Instala dependencias y configura variables:
```bash
pip install -r requirements.txt
```

Ejecuta:
```bash
python app.py
```

Envía una noticia:
```bash
curl -X POST http://127.0.0.1:5000/send-news ^
  -H "Content-Type: application/json" ^
  -d "{\\"user_id\\": \\"id_1\\"}"
```

## Respuestas HTTP

- `200`: correo enviado.
- `400`: falta `user_id`.
- `404`: usuario no encontrado.
- `422`: faltan datos o no se encontró una noticia que con esa categoría.
- `502`: falló el proveedor de noticias o el envío SMTP.
- `500`: error de servidor o de CSV.
