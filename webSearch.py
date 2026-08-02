import os
from dotenv import load_dotenv
from google import genai
from Skill.web_search import tool_schema, web_search

load_dotenv("Config/.env")

gemini_key = os.getenv("GEMINI_API_KEY")
serp_key = os.getenv("SERP_API_KEY")

if not gemini_key:
    raise RuntimeError("GEMINI_API_KEY not found. Check Config/.env")
if not serp_key:
    raise RuntimeError("SERP_API_KEY not found. Check Config/.env")

client = genai.Client(api_key=gemini_key)
registered_tools = [tool_schema]


def build_prompt(user_query: str, search_results: dict) -> str:
    return (
        "You are a helpful research assistant. Use the web search results below to answer the user's question.\n"
        f"User question: {user_query}\n\n"
        f"Search results: {search_results}\n\n"
        "Give a concise answer and include source links if available."
    )


def main() -> None:
    print("Research agent started. Type 'exit' to quit.\n")

    while True:
        user_query = input("You: ").strip()

        if not user_query:
            continue

        if user_query.lower() in {"exit", "quit", "stop"}:
            print("Agent: Goodbye!")
            break

        print("Agent: Searching the web...")
        search_results = web_search(user_query, serp_key)

        if "error" in search_results:
            print(f"Agent: I could not retrieve web results. Error: {search_results['error']}")
            continue

        prompt = build_prompt(user_query, search_results)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        answer = getattr(response, "text", None)
        if not answer:
            answer = str(response)

        print("Agent:", answer)
        print()


if __name__ == "__main__":
    main()

