import requests


class GNewsClient:
    BASE_URL = "https://gnews.io/api/v4/search"

    def __init__(self, api_key, language="es", country="mx", max_results=10, timeout=15):
        self.api_key = api_key
        self.language = language
        self.country = country
        self.max_results = max_results
        self.timeout = timeout

    def search(self, category):
        if not self.api_key:
            raise RuntimeError("Falta configurar GNEWS_API_KEY.")

        response = requests.get(
            self.BASE_URL,
            params={
                "q": category,
                "lang": self.language,
                "country": self.country,
                "max": self.max_results,
                "sortby": "publishedAt",
                "apikey": self.api_key,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()

        articles = []
        for item in payload.get("articles", []):
            title = (item.get("title") or "").strip()
            url = (item.get("url") or "").strip()
            if not title or not url or not url.startswith(("https://", "http://")):
                continue
            articles.append({
                "title": title,
                "description": (item.get("description") or "").strip(),
                "content": (item.get("content") or "").strip(),
                "url": url,
                "published_at": item.get("publishedAt"),
                "source": (item.get("source") or {}).get("name", ""),
            })
        return articles
