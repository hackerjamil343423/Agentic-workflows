"""
Research tool using Tavily API.
Fetches structured research on a given topic.

Usage:
    python tools/research_tavily.py "your topic here"
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_SEARCH_URL = "https://api.tavily.com/search"

TMP_DIR = Path(__file__).resolve().parent.parent / ".tmp"
TMP_DIR.mkdir(exist_ok=True)


def sanitize_filename(text: str) -> str:
    """Convert a topic string to a safe filename."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text[:60].strip("_")


def research(topic: str, max_results: int = 5) -> dict:
    """
    Research a topic using Tavily Search API.

    Returns a dict with: topic, date, results (list of {title, url, content, score}).
    """
    if not TAVILY_API_KEY:
        print("ERROR: TAVILY_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": topic,
        "max_results": max_results,
        "include_answer": True,
        "search_depth": "advanced",
    }

    response = requests.post(TAVILY_SEARCH_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0),
        })

    output = {
        "topic": topic,
        "date": datetime.now().isoformat(),
        "answer": data.get("answer", ""),
        "results": results,
    }

    # Save to .tmp
    filename = f"research_{sanitize_filename(topic)}.json"
    filepath = TMP_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Research saved to {filepath}")
    print(f"Found {len(results)} results")
    if output["answer"]:
        print(f"\nSummary:\n{output['answer']}")

    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/research_tavily.py \"your topic\"")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    research(topic)
