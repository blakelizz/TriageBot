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

def dashboard(results: list[dict]):
    valid = [r["analysis"] for r in results if "category" in r["analysis"]]

    # un nombre de tickets par catégorie
    counts = {}
    for a in valid:
        cat = a["category"]
        counts[cat] = counts.get(cat, 0) + 1

    # Une urgence moyenne
    if valid:
        avg_severity = sum(a["severity"] for a in valid) / len(valid)
    else:
        avg_severity = 0

    top3 = sorted(valid, key=lambda x: x["severity"], reverse=True)[:3]

    print("\n=== Dashboard ===")
    print("Tickets par catégorie :", counts)
    print("Urgence moyenne :", round(avg_severity, 2))
    print("Top 3 des tickets les plus urgents :")
    for t in top3:
        print(f"- {t['category']} (urgence {t['severity']}) : {t['summary']}")


async def process_tickets():
    tickets = load_tickets("tickets.json")
    seen = set()
    results = []

    for ticket in tickets:
        message = ticket.get("message", "").strip()
        player = ticket.get("player", "").strip()

        key = (player, message) # Détection des doublons
        if key in seen:
            results.append({**ticket, "analysis": {"status": "duplicate"}})
            continue
        seen.add(key)

        if len(message) < 3:  # ici gestion d'un message trop court pour être analysé
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
    dashboard(results)

def main():
    asyncio.run(process_tickets())


if __name__ == "__main__":
    main()



