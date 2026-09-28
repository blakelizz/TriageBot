import json
import asyncio
from pathlib import Path

from llm_client import analyze_ticket


def load_tickets(path: str) -> list[dict]:
    """Charge le fichier tickets.json."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur : fichier tickets.json introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur : JSON mal formé dans tickets.json.")
        return []


def save_results(results: list[dict], path: str) -> None:
    """Sauvegarde les résultats dans results.json."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


async def process_tickets():
    tickets = load_tickets("tickets.json")
    results = []

    for ticket in tickets:
        message = ticket.get("message", "").strip()

        if not message:
            results.append({**ticket, "analysis": {"status": "to_check"}})
            continue

        try:
            analysis = await analyze_ticket(message)
        except Exception as e:
            print(f"Erreur LLM pour le ticket {ticket.get('id')} : {e}")
            analysis = {"status": "to_check"}

        results.append({**ticket, "analysis": analysis})

    save_results(results, "results.json")
    print("Analyse terminée. Résultats dans results.json.")


def main():
    asyncio.run(process_tickets())


if __name__ == "__main__":
    main()



