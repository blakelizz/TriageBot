def is_french(message: str) -> bool:
    return any(c in message for c in "éèàùçôîï")

GERMAN_WORDS = {"ich", "nicht", "bitte", "danke", "hallo"}

def is_german(msg: str) -> bool:
    msg = msg.lower()
    return any(w in msg for w in GERMAN_WORDS)


def generate_draft(ticket: dict, analysis: dict) -> str:
    message = ticket.get("message", "")
    category = analysis.get("category")
    french = is_french(message)

    if french:
        if category == "bug":
            return "Merci pour votre message ! Nous avons bien noté le problème et allons le corriger."
        if category == "payment":
            return "Merci pour votre retour. Nous allons vérifier votre paiement rapidement."
        if category == "toxicity":
            return "Merci pour votre signalement. Nous prenons ce comportement très au sérieux."
        return "Merci pour votre message ! Nous allons analyser votre demande."
    elif is_german(message):
        if category == "bug":
            return "Danke für Ihre Nachricht! Wir haben das Problem zur Kenntnis genommen und werden es beheben."
        if category == "payment":
            return "Vielen Dank für Ihr Feedback. Wir werden Ihre Zahlung schnell überprüfen."
        if category == "toxicity":
            return "Vielen Dank für Ihre Meldung. Wir nehmen dieses Verhalten sehr ernst."
        return "Vielen Dank für Ihre Nachricht! Wir werden Ihre Anfrage prüfen."
    else:
        if category == "bug":
            return "Thanks for your report! We will investigate this issue."
        if category == "payment":
            return "Thank you. We will check your payment and get back to you soon."
        if category == "toxicity":
            return "Thank you for reporting this. We take such behavior very seriously."
        return "Thank you for your message! We will look into your request."

