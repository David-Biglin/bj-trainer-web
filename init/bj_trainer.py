#!/usr/bin/env python3
"""
Blackjack Basic Strategy Trainer (CLI)
- Generates random scenarios: player 2-card hand + dealer upcard
- You input move: H (hit), S (stand), D (double), P (split), R (surrender)
- Evaluates your move vs (simplified but strong) basic strategy
Notes:
- Assumes typical rules: 4-8 decks, dealer stands on soft 17 (S17),
  double allowed on any two cards, double after split allowed, late surrender allowed.
- Strategy is for the FIRST decision only.
"""

import random
from dataclasses import dataclass

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def card_value(rank: str) -> int:
    if rank == "A":
        return 11
    if rank in ["J", "Q", "K"]:
        return 10
    return int(rank)

def is_ten_value(rank: str) -> bool:
    return rank in ["10", "J", "Q", "K"]

@dataclass(frozen=True)
class HandInfo:
    cards: tuple[str, str]
    total: int              # best total <=21 if possible else minimal total
    is_soft: bool
    is_pair: bool
    pair_rank: str | None   # e.g. "8" or "A" or "K"

def evaluate_two_card_hand(c1: str, c2: str) -> HandInfo:
    is_pair = (c1 == c2) or (is_ten_value(c1) and is_ten_value(c2))
    pair_rank = None
    if is_pair:
        # treat any ten-value pair as "10" for strategy split rules
        if is_ten_value(c1) and is_ten_value(c2):
            pair_rank = "10"
        else:
            pair_rank = c1

    v1, v2 = card_value(c1), card_value(c2)
    total = v1 + v2
    is_soft = False

    # Handle aces
    if c1 == "A" or c2 == "A":
        # total currently counts ace as 11
        if total <= 21:
            is_soft = True
        else:
            # convert one ace from 11 to 1
            total -= 10
            is_soft = False

    # If both are aces => total 12 soft, but you can only count one as 11
    if c1 == "A" and c2 == "A":
        total = 12
        is_soft = True

    return HandInfo(cards=(c1, c2), total=total, is_soft=is_soft, is_pair=is_pair, pair_rank=pair_rank)

def normalize_dealer_upcard(rank: str) -> str:
    return "10" if is_ten_value(rank) else rank

def basic_strategy_move(hand: HandInfo, dealer_up: str, allow_surrender=True) -> str:
    """
    Returns one of: "H","S","D","P","R"
    This is a solid, commonly used basic strategy for S17, DAS, LS.
    """
    d = normalize_dealer_upcard(dealer_up)

    # 1) Pairs (Split decisions)
    if hand.is_pair and hand.pair_rank is not None:
        p = hand.pair_rank
        if p == "A":
            return "P"
        if p == "8":
            return "P"
        if p == "10":
            return "S"
        if p == "5":
            # treat as hard 10
            # fall through to hard logic by faking a non-pair
            pass
        elif p == "9":
            return "P" if d in ["2","3","4","5","6","8","9"] else "S"
        elif p == "7":
            return "P" if d in ["2","3","4","5","6","7"] else "H"
        elif p == "6":
            return "P" if d in ["2","3","4","5","6"] else "H"
        elif p == "4":
            return "P" if d in ["5","6"] else "H"
        elif p in ["2","3"]:
            return "P" if d in ["2","3","4","5","6","7"] else "H"

        # if 5s, we'll handle below as hard total

    # 2) Surrender (Late surrender)
    if allow_surrender and not hand.is_soft:
        # Classic LS spots (S17):
        # Hard 16 vs 9/10/A (but not if it's a pair of 8s - already handled)
        # Hard 15 vs 10
        if hand.total == 16 and d in ["9","10","A"] and not (hand.is_pair and hand.pair_rank == "8"):
            return "R"
        if hand.total == 15 and d == "10":
            return "R"

    # 3) Soft hands (A counted as 11)
    if hand.is_soft:
        # soft totals are 13-20 typical for 2 cards (A,2 -> 13, etc)
        t = hand.total
        if t in [13, 14]:  # A2, A3
            return "D" if d in ["5","6"] else "H"
        if t in [15, 16]:  # A4, A5
            return "D" if d in ["4","5","6"] else "H"
        if t == 17:        # A6
            return "D" if d in ["3","4","5","6"] else "H"
        if t == 18:        # A7
            if d in ["3","4","5","6"]:
                return "D"
            if d in ["2","7","8"]:
                return "S"
            return "H"  # vs 9,10,A
        if t >= 19:        # A8, A9
            return "S"

    # 4) Hard hands (including pair of 5s treated as hard 10)
    t = hand.total

    # Doubling (2-card only – in our trainer, always 2-card)
    if t == 9:
        return "D" if d in ["3","4","5","6"] else "H"
    if t == 10:
        return "D" if d in ["2","3","4","5","6","7","8","9"] else "H"
    if t == 11:
        return "D" if d in ["2","3","4","5","6","7","8","9","10"] else "H"  # vs A is H in many charts; keep simple
    # Stand/hit thresholds
    if t <= 8:
        return "H"
    if t == 12:
        return "S" if d in ["4","5","6"] else "H"
    if t in [13,14,15,16]:
        return "S" if d in ["2","3","4","5","6"] else "H"
    if t >= 17:
        return "S"

    # fallback
    return "H"

def random_card() -> str:
    return random.choice(RANKS)

def format_hand(hand: HandInfo) -> str:
    c1, c2 = hand.cards
    tag = "SOFT" if hand.is_soft else "HARD"
    if hand.is_pair:
        tag += " / PAIR"
    return f"{c1},{c2}  ({tag} {hand.total})"

def main():
    print("Blackjack Basic Strategy Trainer")
    print("Moves: H=Hit, S=Stand, D=Double, P=Split, R=Surrender, Q=Quit")
    print("Assumes: S17, DAS, LS, double any two. First-decision trainer.\n")

    correct = 0
    total = 0

    while True:
        # Generate a realistic-ish 2-card hand and dealer upcard
        c1, c2 = random_card(), random_card()
        dealer = random_card()

        hand = evaluate_two_card_hand(c1, c2)
        dealer_norm = normalize_dealer_upcard(dealer)

        # Avoid super-rare impossible feeling hands like 2 aces too often? (keep as-is; it's fine)
        recommended = basic_strategy_move(hand, dealer_norm, allow_surrender=True)

        print(f"\nYour hand: {format_hand(hand)}")
        print(f"Dealer shows: {dealer_norm}")

        user = input("Your move (H/S/D/P/R/Q): ").strip().upper()
        if user == "Q":
            break
        if user not in ["H","S","D","P","R"]:
            print("Invalid move. Use H/S/D/P/R/Q.")
            continue

        total += 1
        if user == recommended:
            correct += 1
            print("✅ Correct.")
        else:
            print(f"❌ Not quite. Correct play: {recommended}")

        # quick explanation nugget
        if recommended == "S":
            print("Why: standing is best here based on dealer strength and bust risk.")
        elif recommended == "H":
            print("Why: you need to improve your total vs this dealer up-card.")
        elif recommended == "D":
            print("Why: doubling has the best expected value in this spot.")
        elif recommended == "P":
            print("Why: splitting increases EV compared to playing as one hand.")
        elif recommended == "R":
            print("Why: surrender saves money in a negative-EV spot.")

        pct = (correct / total) * 100
        print(f"Score: {correct}/{total} ({pct:.1f}%)")

    if total:
        pct = (correct / total) * 100
        print(f"\nFinal score: {correct}/{total} ({pct:.1f}%)")
    print("Done.")

if __name__ == "__main__":
    main()
