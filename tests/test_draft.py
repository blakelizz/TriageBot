from triagebot.draft import generate_draft


def test_draft_french():
    ticket = {"message": "Je suis bloqué"}
    analysis = {"category": "bug"}
    draft = generate_draft(ticket, analysis)
    assert "Merci" in draft

def test_draft_english():
    ticket = {"message": "I am stuck"}
    analysis = {"category": "bug"}
    draft = generate_draft(ticket, analysis)
    assert "Thanks" in draft

def test_draft_german():
    ticket = {"message": "Ich habe ein Problem"}
    analysis = {"category": "bug"}
    draft = generate_draft(ticket, analysis)
    assert "Danke" in draft

