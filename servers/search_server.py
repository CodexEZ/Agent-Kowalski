from fastmcp import FastMCP, Client
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import asyncio
import uvicorn
from dotenv import load_dotenv
import sys
import os
load_dotenv()

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastMCP()
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AI-ResearchBot/1.0)"}
TIMEOUT = 10


@app.tool(
    description="""
    📌 [USE CASE] Retrieve ONLY **titles + URLs** from DuckDuckGo.  
    👉 Use this when you need a reference list of sources (links) but do NOT need summaries or content.  
    ❌ Do NOT use if the user asks for explanations, summaries, or detailed info.  
    Example: "Find top 5 articles about quantum computing"
    """
)
def get_links(query: str, max_results: int = 3) -> dict:
    try:
        ddgs = DDGS()
        results = []
        for r in ddgs.text(query, max_results=max_results, region="us-en"):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", "")
            })
        return {"results": results}
    except Exception as e:
        return {"error": f"get_links failed: {str(e)}"}


@app.tool(
    description="""
    📌 [USE CASE] Perform a **deep web search** and return short **summaries/snippets** + some page content.  
    👉 Use this when the user asks for actual information, facts, news, weather, person info, etc.  
    ❌ Do NOT use if you only need links.  
    Example: "Summarize latest AI news" or "What's the weather in Paris?"
    
    PARAMETERS:  
    - `query`: What to search for.  
    - `max_results`: How many results to fetch.  
    - `character_lookup`: Approx. number of characters from each page to return (higher = deeper scan).
    """
)
def search(query: str, max_results: int = 1, character_lookup: int = 1000) -> dict:
    try:
        ddgs = DDGS()
        results = []

        for r in ddgs.text(query, max_results=max_results, region="us-en"):
            url = r.get("href", "")
            entry = {
                "title": r.get("title", ""),
                "url": url,
                "snippet": r.get("body", ""),
            }
            try:
                page = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                soup = BeautifulSoup(page.text, "html.parser")
                cleaned = " ".join(soup.text.split())
                entry["content"] = cleaned[:character_lookup]
            except Exception as e:
                entry["error"] = f"Failed to fetch page: {str(e)}"

            results.append(entry)

        return {"results": results}
    except Exception as e:
        return {"error": f"search failed: {str(e)}"}


@app.tool(
    description="""
    📌 [USE CASE] Fetch the **FULL cleaned text** of a webpage you already have.  
    👉 Use this when you already know the URL and need detailed text (e.g., academic paper, documentation, long article).  
    ❌ Do NOT use if you just need a list of links or a short summary.  
    Example: "Get full text from https://arxiv.org/abs/2405.12345"
    """
)
def get_page_content(link: str) -> dict:
    try:
        page = requests.get(link, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(page.text, "html.parser")
        cleaned = " ".join(soup.text.split())
        return {"url": link, "data": cleaned}
    except Exception as e:
        return {"url": link, "error": f"get_page_content failed: {str(e)}"}

@app.tool(description="Get current weather for a city using OpenWeather API.")
def get_weather(city: str) -> dict:
    """
    Returns the current weather conditions for a given city using OpenWeather API.
    """
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        res = requests.get(url, timeout=10).json()

        if res.get("cod") != 200:
            return {"error": res.get("message", "Failed to fetch weather")}

        return {
            "city": res["name"],
            "temperature": res["main"]["temp"],
            "feels_like": res["main"]["feels_like"],
            "humidity": res["main"]["humidity"],
            "weather": res["weather"][0]["description"],
            "wind_speed": res["wind"]["speed"],
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.prompt(
    description="""
    📌 [USE CASE] Research about any topic, person, or entity.  
    👉 Steps:  
      1. Use `get_links` to gather top reference URLs.  
      2. For each link, use `get_page_content` to extract full text.  
      3. Return the collected content so the model can summarize or analyze.  
    
    Example: "Research about quantum entanglement" or "Find information about Nikola Tesla"
    """,
    name="research_topic"
)
def research_topic() -> str:
    return """
    Task: Research about a given topic.

    Steps for the model:
    1. Call `get_links` with query="<TOPIC>", max_results=3.
    2. For each returned link, call `get_page_content` to extract cleaned text.
    3. Use the gathered content to generate a factual summary of "<TOPIC>".

    IMPORTANT:
    - Always provide the summary + the list of source URLs.
    - If some pages fail, use whatever data is available.
    """

    
test_server = Client(app)

async def run_tests():
    async with test_server:
        print("🔍 Running MCP tool tests...\n")

        await test_server.ping()
        tools = await test_server.list_tools()
        
        print(f"Discovered tools: {[t.name for t in tools]}")

        # Test get_links
        res = await test_server.call_tool("get_links", {"query": "General Theory of Relativity", "max_results": 3})
        assert "results" in res.content[0].text, "get_links failed"
        print("✅ get_links passed")

        # Test search
        res = await test_server.call_tool("search", {"query": "latest AI news", "max_results": 1})
        assert "results" in res.content[0].text, "search failed"
        print("✅ search passed")

        # Test get_page_content
        res = await test_server.call_tool("get_page_content", {"link": "https://www.example.com"})
        assert "data" in res.content[0].text, "get_page_content failed"
        print("✅ get_page_content passed")

        # Test get_weather
        res = await test_server.call_tool("get_weather", {"city": "Cuttack"})
        assert "temperature" in res.content[0].text, f"get_weather failed: {res}"
        print("✅ get_weather passed")

        print("\n🎉 All tests passed! Starting server locally 🚀\n")
if __name__ == "__main__":
    print("Running test cases 🏃‍♂️....")
    asyncio.run(run_tests())
    app.run(transport="streamable-http",host="127.0.0.1", port=8000)# host="127.0.0.1", port=8000
