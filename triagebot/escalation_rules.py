from security import is_prompt_injection

def escalation_rule(analysis: dict, message: str = "") -> str:

    if is_prompt_injection(message):
        return "human_review"

    
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

