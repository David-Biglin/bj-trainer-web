#!/usr/bin/env python3
"""Blackjack Basic Strategy Trainer (CLI)."""

from strategy import MOVE_LABELS, evaluate_move, format_hand, generate_scenario

def main():
    print("Blackjack Basic Strategy Trainer")
    print("Moves: H=Hit, S=Stand, D=Double, P=Split, R=Surrender, Q=Quit")
    print("Assumes: S17, DAS, LS, double any two. First-decision trainer.\n")

    correct = 0
    total = 0

    while True:
        scenario = generate_scenario()
        hand = scenario.hand

        print(f"\nYour hand: {format_hand(hand)}")
        print(f"Dealer shows: {scenario.dealer_display}")

        user = input("Your move (H/S/D/P/R/Q): ").strip().upper()
        if user == "Q":
            break
        if user not in MOVE_LABELS:
            print("Invalid move. Use H/S/D/P/R/Q.")
            continue

        result = evaluate_move(scenario, user)
        total += 1
        if result["is_correct"]:
            correct += 1
            print("✅ Correct.")
        else:
            print(f"❌ Not quite. Correct play: {result['recommended_move']}")

        print(f"Why: {result['explanation']}")

        pct = (correct / total) * 100
        print(f"Score: {correct}/{total} ({pct:.1f}%)")

    if total:
        pct = (correct / total) * 100
        print(f"\nFinal score: {correct}/{total} ({pct:.1f}%)")
    print("Done.")

if __name__ == "__main__":
    main()
