def escalation_rule(analysis: dict) -> str:
    category = analysis.get("category")
    severity = analysis.get("severity")
    status = analysis.get("status")

    if status == "to_check":
        return "human_review"

    if category == "toxicity":
        return "moderation_team"

    if category == "payment" and severity is not None and severity >= 4:
        return "support_manager"

    return "standard"

