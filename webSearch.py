import os
import re
from dotenv import load_dotenv
from google import genai
from Skill.web_search import tool_schema, web_search

logged_web_search = web_search.with_prehook("web_search", web_search)

load_dotenv("Config/.env")

gemini_key = os.getenv("GEMINI_API_KEY")
serp_key = os.getenv("SERP_API_KEY")

if not gemini_key:
    raise RuntimeError("GEMINI_API_KEY not found. Check Config/.env")
if not serp_key:
    raise RuntimeError("SERP_API_KEY not found. Check Config/.env")

client = genai.Client(api_key=gemini_key)
registered_tools = [tool_schema]


def extract_session_facts(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    triggers = [
        "i am",
        "i'm",
        "i've",
        "i have",
        "my",
        "we are",
        "we're",
        "our",
        "the user is",
        "the user has",
        "the user lives",
        "the user works",
        "they are",
        "he is",
        "she is",
        "it is",
        "this is",
        "that is",
        "as a",
        "born",
        "from",
        "located in",
        "based in",
        "interested in",
    ]
    facts = []

    for sentence in sentences:
        cleaned = sentence.strip()
        if not cleaned or cleaned.endswith("?") or len(cleaned) < 15:
            continue

        lower = cleaned.lower()
        if any(trigger in lower for trigger in triggers):
            facts.append(cleaned)

    return facts


def build_prompt(user_query: str, search_results: dict, memory_facts: list[str], conversation_history: list[str]) -> str:
    memory_section = ""
    if memory_facts:
        memory_lines = "\n".join(f"- {fact}" for fact in memory_facts)
        memory_section = f"Session memory:\n{memory_lines}\n\n"

    history_section = ""
    if conversation_history:
        history_lines = "\n".join(conversation_history)
        history_section = f"Conversation history:\n{history_lines}\n\n"

    return (
        "You are a helpful research assistant. Use the web search results below to answer the user's question.\n"
        f"{memory_section}"
        f"{history_section}"
        f"User question: {user_query}\n\n"
        f"Search results: {search_results}\n\n"
        "Give a concise answer and include source links if available."
    )


def main() -> None:
    print("Research agent started. Type 'exit' to quit.\n")

    session_memory: list[str] = []
    conversation_history: list[str] = []

    while True:
        user_query = input("You: ").strip()

        if not user_query:
            continue

        if user_query.lower() in {"exit", "quit", "stop"}:
            print("Agent: Goodbye!")
            break

        conversation_history.append(f"User: {user_query}")
        session_memory.extend(
            fact for fact in extract_session_facts(user_query)
            if fact not in session_memory
        )
        conversation_history = conversation_history[-8:]

        print("Agent: Searching the web...")
        search_results = logged_web_search(user_query, serp_key)

        if "error" in search_results:
            print(f"Agent: I could not retrieve web results. Error: {search_results['error']}")
            continue

        prompt = build_prompt(user_query, search_results, session_memory, conversation_history)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        answer = getattr(response, "text", None)
        if not answer:
            answer = str(response)

        conversation_history.append(f"Agent: {answer}")
        conversation_history = conversation_history[-8:]
        session_memory.extend(
            fact for fact in extract_session_facts(answer)
            if fact not in session_memory
        )

        print("Agent:", answer)
        print()


if __name__ == "__main__":
    main()

