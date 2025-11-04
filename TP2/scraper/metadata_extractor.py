
import asyncio
import aiohttp
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

async def extract_metadata(session: aiohttp.ClientSession, url: str) -> dict:
    try:
        async with session.get(url, timeout=30, headers=HEADERS) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            meta_tags = {}

            description = soup.find('meta', attrs={'name': 'description'})
            if description:
                meta_tags['description'] = description.get('content', '')

            keywords = soup.find('meta', attrs={'name': 'keywords'})
            if keywords:
                meta_tags['keywords'] = keywords.get('content', '')

            og_tags = soup.find_all('meta', property=lambda value: value and value.startswith('og:'))
            for tag in og_tags:
                # La clave será lo que está en 'property' (ej: "og:title")
                # El valor será lo que está en 'content'
                meta_tags[tag.get('property')] = tag.get('content', '')

            return meta_tags

    except aiohttp.ClientError as e:
        print(f"Error de red al intentar acceder a {url}: {e}")
        return {"error": f"Network error: {e}"}
    except asyncio.TimeoutError:
        print(f"Timeout al intentar acceder a {url}")
        return {"error": "Request timed out after 30 seconds"}
    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar {url}: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

async def main():
    test_url = "https://github.com/FacundoMala" # Probemos con tu perfil de GitHub
    print(f"🧪 Probando el extractor de metadatos con la URL: {test_url}")
    
    async with aiohttp.ClientSession() as session:
        data = await extract_metadata(session, test_url)
        
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())