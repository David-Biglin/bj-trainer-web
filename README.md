# Blackjack Basic Strategy Trainer Web Demo

This project turns a working Python blackjack basic strategy CLI into a very lightweight Flask web app. It presents one first-decision training scenario at a time, checks the user's move against the shared strategy logic, explains the correct play in plain English, and keeps score in the browser session.

## What The App Does

- Shows a two-card player hand and dealer upcard
- Labels the hand as hard, soft, or pair
- Lets the user choose Hit, Stand, Double, Split, or Surrender
- Compares the choice against the existing basic strategy rules
- Gives immediate feedback, the correct move, and a short explanation
- Tracks score until the browser session ends or the score is reset

Rules assumed throughout the trainer:

- Dealer stands on soft 17
- Double after split allowed
- Late surrender enabled
- Double any two cards
- First-decision trainer only

## How To Run It

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Start the web app:

```bash
python3 app.py
```

3. Open the local URL shown by Flask, usually `http://127.0.0.1:5000`.

Optional: run the smoke test with:

```bash
pytest
```

## Demo Talking Points

- The original blackjack strategy logic is still the source of truth and now powers both the CLI and the web app.
- The web layer is intentionally thin: Flask routes, one template, one stylesheet, and session-backed score.
- This is a good example of AI speeding up the move from proof of concept to usable prototype without changing the core domain rules.
- The app is easy to explain to non-technical stakeholders because each answer gets immediate feedback and a short explanation.
- The codebase stays local-first and demo-friendly: no database, no auth, no frontend framework, no deployment setup.

## Future Enhancement Ideas

- Add rule toggles for H17 vs S17 or surrender on/off
- Add streak tracking and harder scenario weighting
- Show a compact history of recent answers
- Add a printable basic strategy reference view
- Add more tests around edge-case hands and explanations
