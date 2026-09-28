# TriageBot — Analyse automatique de tickets joueurs (LLM + Python)

TriageBot analyse automatiquement les tickets envoyés par des joueurs grâce à un modèle LLM qui tourne **en local** avec [Ollama](https://ollama.com). Aucune clé d'API ni connexion à un service payant n'est nécessaire.

À la fin, il affiche un tableau de bord dans le terminal et génère deux fichiers : `results.json` et `report.md`.

---

## 1. Prérequis

| Outil | Version | Vérification |
|-------|---------|--------------|
| Python | 3.10 ou plus | `python --version` |
| Git | n'importe laquelle | `git --version` |
| Ollama | dernière version | `ollama --version` |

### Installer Ollama

1. Téléchargez et installez Ollama : <https://ollama.com/download>
2. Téléchargez le modèle utilisé par le projet  :

   ```bash
   ollama pull gemma3:4b
   ```

3. Vérifiez que le modèle est bien présent :

   ```bash
   ollama list
   ```

**Ollama doit être lancé avant d'exécuter TriageBot.**
- Sous Windows et macOS, l'application Ollama démarre le serveur automatiquement (icône dans la barre des tâches).
- Sous Linux, ou si le serveur n'est pas lancé, exécutez `ollama serve` dans un terminal séparé et laissez-le ouvert.

---

## 2. Installation

### Cloner le dépôt

```bash
git clone https://github.com/blakelizz/TriageBot.git
cd TriageBot
```

### Créer un environnement virtuel (recommandé)

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Une fois activé, `(.venv)` apparaît au début de la ligne du terminal.

### Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 3. Lancer le projet

Depuis la **racine du dépôt** (le dossier `TriageBot/`, là où se trouve `tickets.json`) :

```bash
python triagebot/cli.py
```

La commande doit être lancée depuis la racine : le programme lit `tickets.json` et écrit ses résultats dans le dossier courant.


### Ce qui se passe

1. Les tickets sont lus depuis `tickets.json`.
2. Chaque ticket est envoyé au modèle `gemma3:4b` via Ollama (compter quelques secondes par ticket).
3. Le tableau de bord s'affiche dans le terminal :

   ```
   Analyse terminée. Résultats dans results.json.

   === Dashboard ===
   Tickets par catégorie : {'bug': 3, 'payment': 2, 'suggestion': 2, ...}
   Urgence moyenne : 3.1
   Top 3 des tickets les plus urgents :
   - bug (urgence 5) : Le jeu plante lors de l'ouverture de l'inventaire...
   ...
   Rapport généré : report.md
   ```

4. Deux fichiers sont créés (ou écrasés) à la racine :
   - **`results.json`** : chaque ticket enrichi de son analyse, de son brouillon de réponse et de sa décision d'escalade ;
   - **`report.md`** : un rapport lisible listant les tickets à escalader et ceux à vérifier manuellement.

### Analyser vos propres tickets

Remplacez le contenu de `tickets.json` en respectant ce format :

```json
[
  {
    "id": 1,
    "player": "DragonSlayer42",
    "message": "Le jeu crash à chaque fois que j'ouvre l'inventaire."
  }
]
```

---

## 4. Lancer les tests

Les tests unitaires ne nécessitent pas Ollama.

```bash
pip install pytest
pytest
```

Résultat attendu :

........                                                  [100%]
8 passed

---

## 5. Structure du projet

```
TriageBot/
├── tickets.json              # Tickets d'entrée à analyser
├── results.json              # Résultats générés (sortie)
├── report.md                 # Rapport généré (sortie)
├── requirements.txt          # Dépendances Python
├── pytest.ini                # Configuration des tests
├── triagebot/
│   ├── cli.py                # Point d'entrée : lecture, analyse, dashboard, export
│   ├── llm_client.py         # Appel au LLM via Ollama + validation du JSON renvoyé
│   ├── system_prompt.txt     # Instructions données au modèle
│   ├── draft.py              # Brouillons de réponse (FR / EN / DE)
│   ├── escalation_rules.py   # Règles d'escalade
│   ├── security.py           # Détection des injections de prompt
│   └── report.py             # Génération de report.md
└── tests/                    # Tests
    ├── test_draft.py
    └── test_escalation.py
```

### Règles d'escalade

| Condition | Décision |
|-----------|----------|
| Tentative d'injection de prompt détectée | `human_review` |
| Analyse impossible, invalide ou message trop court | `human_review` |
| Catégorie `toxicity` | `moderation_team` |
| Catégorie `payment` avec urgence ≥ 4 | `support_manager` |
| Tous les autres cas | `standard` |

---
