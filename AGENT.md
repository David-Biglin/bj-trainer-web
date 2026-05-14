# AGENT.md

## Project Overview

This project is a lightweight Blackjack Basic Strategy Trainer.

The current implementation is a Python CLI proof of concept. The goal is to evolve it into a lightweight browser-based web application while preserving the original blackjack strategy logic.

## Technical Goals

- Preserve existing strategy logic and rules
- Keep the app lightweight and easy to run locally
- Use Flask
- Use simple HTML and CSS
- Avoid unnecessary dependencies
- Prioritise readability and maintainability

## Current Rules Assumptions

- Dealer stands on soft 17
- Double after split allowed
- Late surrender enabled
- Double any two cards
- First-decision trainer only

## Web App Goals

The app should show:

- Player hand
- Dealer upcard
- Whether the hand is hard, soft, or pair
- Move buttons: Hit, Stand, Double, Split, Surrender
- Current score
- Feedback after each answer
- Correct move
- Plain-English explanation
- Next Hand button
- Reset Score button

## Non-Goals

Do not add:

- Authentication
- Database
- User accounts
- Complex frontend frameworks
- Cloud deployment
- Microservices
- Payment logic
- Advanced casino simulation

## Code Quality Expectations

- Separate blackjack strategy logic from web UI logic
- Keep functions modular
- Keep filenames simple
- Add comments where useful
- Do not over-engineer
- Ensure the app can run locally with `python3 app.py`

## Demo Intent

This project demonstrates:

- AI-assisted software evolution
- Moving from proof-of-concept to usable prototype
- Human-led AI development
- Guardrails and validation around AI-generated code