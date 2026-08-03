import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from dotenv import load_dotenv
import serpapi

load_dotenv("Config/.env")

tool_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Perform a web search to find current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web."
                }
            },
            "required": ["query"]
        }
    }
}


def _log_tool_call(tool_name: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Prehook: calling tool '{tool_name}'")


def with_prehook(tool_name: str, target_func: Callable[..., dict]) -> Callable[..., dict]:
    @wraps(target_func)
    def wrapper(*args: Any, **kwargs: Any) -> dict:
        _log_tool_call(tool_name)
        return target_func(*args, **kwargs)

    return wrapper


def web_search(query: str, serp_key: str | None = None) -> dict:
    if not serp_key:
        serp_key = os.getenv("SERP_API_KEY")

    if not serp_key:
        return {"error": "SERP_API_KEY is missing."}

    try:
        client = serpapi.Client(api_key=serp_key)

        results = client.search(
            {
                "engine": "google",
                "q": query,
                "hl": "en",
                "gl": "us",
            }
        )

        organic_results = results.get("organic_results", [])
        formatted_results = []

        for item in organic_results[:3]:
            formatted_results.append(
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
            )

        return {"results": formatted_results}

    except Exception as e:
        return {"error": str(e)}


web_search.with_prehook = with_prehook