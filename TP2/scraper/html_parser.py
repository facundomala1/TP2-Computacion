
import asyncio
import aiohttp
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

async def scrape_page_content(session: aiohttp.ClientSession, url: str) -> dict:

    try:
        async with session.get(url, timeout=30, headers=HEADERS) as response:
            response.raise_for_status()
            
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            title = soup.title.string.strip() if soup.title else "No Title Found"
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            headers = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
            images_count = len(soup.find_all('img'))
            
            return {
                "title": title,
                "links_count": len(links),
                "links": links[:20],
                "structure": headers,
                "images_count": images_count,
            }

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

    test_url = "https://es.wikipedia.org/wiki/Python"
    print(f"🧪 Probando el scraper con la URL: {test_url}")
    
    async with aiohttp.ClientSession() as session:
        data = await scrape_page_content(session, test_url)
        
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())