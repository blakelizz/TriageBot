def generate_report(results: list[dict], path: str = "report.md") -> None:
    total = len(results)
    escalated_ids = set()
    escalated = []
    to_check = []

    for r in results:
        analysis = r["analysis"]
        status = analysis.get("status")
        category = analysis.get("category")
        severity = analysis.get("severity", 0)

        if status == "to_check":
            to_check.append(r)
        elif category == "toxicity":
            if r["id"] not in escalated_ids:
                escalated.append(r)
                escalated_ids.add(r["id"])
        elif category == "payment" and severity >= 4:
            if r["id"] not in escalated_ids:
                escalated.append(r)
                escalated_ids.add(r["id"])

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Rapport d'analyse des tickets\n\n")
        f.write(f"Total des tickets analysés : **{total}**\n\n")

        f.write("## Tickets à escalader\n")
        if not escalated:
            f.write("Aucun ticket à escalader.\n\n")
        else:
            for t in escalated:
                f.write(f"- ID {t['id']} — {t['player']} — {t['message']}\n")
            f.write("\n")

        f.write("## Tickets à vérifier (to_check)\n")
        if not to_check:
            f.write("Aucun ticket à vérifier.\n")
        else:
            for t in to_check:
                f.write(f"- ID {t['id']} — {t['player']} — {t['message']}\n")


