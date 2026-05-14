/goal
Turn this Python CLI Blackjack Basic Strategy Trainer into a very lightweight web app.

Context:
- This is currently a working Python command-line proof of concept.
- Keep the existing blackjack strategy logic as the source of truth.
- The aim is to demonstrate how AI can quickly convert working logic into a usable web interface.
- Keep the app simple, demo-friendly, and easy to run locally.
- Follow the guidance in AGENT.md.

Requirements:
1. Build a small web app using Flask.
2. Move the existing blackjack logic into reusable functions/modules where sensible.
3. Create a homepage that shows:
   - Player hand
   - Dealer upcard
   - Whether the hand is hard, soft, or pair
   - Buttons for Hit, Stand, Double, Split, Surrender
   - Current score
4. When the user chooses a move:
   - Compare it against the recommended basic strategy move.
   - Show whether the answer was correct.
   - Show the correct move.
   - Show a short plain-English explanation.
5. Add a Next Hand button to generate a new scenario.
6. Use simple clean HTML/CSS. No complex frontend framework.
7. Store score in Flask session so the score persists during the browser session.
8. Add a reset score option.
9. Keep the app runnable locally with:
   python3 app.py
10. Add or update README.md with:
   - What the app does
   - How to run it
   - Demo talking points
   - Future enhancement ideas
11. Add a simple smoke test if sensible.

Constraints:
- Do not over-engineer this.
- Do not add a database.
- Do not add authentication.
- Do not add cloud deployment.
- Preserve the existing rules assumptions:
  S17, DAS, late surrender, double any two cards, first-decision trainer.

Acceptance criteria:
- The app runs locally.
- A non-technical user can use it in a browser.
- The original blackjack strategy logic still works.
- The UI gives clear feedback after each answer.
- The repo is clean and easy to explain in a short demo.