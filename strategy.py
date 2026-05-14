from __future__ import annotations

import random
from dataclasses import dataclass

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
MOVE_LABELS = {
    "H": "Hit",
    "S": "Stand",
    "D": "Double",
    "P": "Split",
    "R": "Surrender",
}


@dataclass(frozen=True)
class HandInfo:
    cards: tuple[str, str]
    total: int
    is_soft: bool
    is_pair: bool
    pair_rank: str | None


@dataclass(frozen=True)
class Scenario:
    player_cards: tuple[str, str]
    dealer_upcard: str

    @property
    def hand(self) -> HandInfo:
        return evaluate_two_card_hand(*self.player_cards)

    @property
    def dealer_display(self) -> str:
        return normalize_dealer_upcard(self.dealer_upcard)

    @property
    def recommended_move(self) -> str:
        return basic_strategy_move(self.hand, self.dealer_upcard, allow_surrender=True)


def card_value(rank: str) -> int:
    if rank == "A":
        return 11
    if rank in ["J", "Q", "K"]:
        return 10
    return int(rank)


def is_ten_value(rank: str) -> bool:
    return rank in ["10", "J", "Q", "K"]


def evaluate_two_card_hand(c1: str, c2: str) -> HandInfo:
    is_pair = (c1 == c2) or (is_ten_value(c1) and is_ten_value(c2))
    pair_rank = None
    if is_pair:
        if is_ten_value(c1) and is_ten_value(c2):
            pair_rank = "10"
        else:
            pair_rank = c1

    v1, v2 = card_value(c1), card_value(c2)
    total = v1 + v2
    is_soft = False

    if c1 == "A" or c2 == "A":
        if total <= 21:
            is_soft = True
        else:
            total -= 10

    if c1 == "A" and c2 == "A":
        total = 12
        is_soft = True

    return HandInfo(
        cards=(c1, c2),
        total=total,
        is_soft=is_soft,
        is_pair=is_pair,
        pair_rank=pair_rank,
    )


def normalize_dealer_upcard(rank: str) -> str:
    return "10" if is_ten_value(rank) else rank


def basic_strategy_move(hand: HandInfo, dealer_up: str, allow_surrender: bool = True) -> str:
    d = normalize_dealer_upcard(dealer_up)

    if hand.is_pair and hand.pair_rank is not None:
        p = hand.pair_rank
        if p == "A":
            return "P"
        if p == "8":
            return "P"
        if p == "10":
            return "S"
        if p == "5":
            pass
        elif p == "9":
            return "P" if d in ["2", "3", "4", "5", "6", "8", "9"] else "S"
        elif p == "7":
            return "P" if d in ["2", "3", "4", "5", "6", "7"] else "H"
        elif p == "6":
            return "P" if d in ["2", "3", "4", "5", "6"] else "H"
        elif p == "4":
            return "P" if d in ["5", "6"] else "H"
        elif p in ["2", "3"]:
            return "P" if d in ["2", "3", "4", "5", "6", "7"] else "H"

    if allow_surrender and not hand.is_soft:
        if hand.total == 16 and d in ["9", "10", "A"] and not (hand.is_pair and hand.pair_rank == "8"):
            return "R"
        if hand.total == 15 and d == "10":
            return "R"

    if hand.is_soft:
        t = hand.total
        if t in [13, 14]:
            return "D" if d in ["5", "6"] else "H"
        if t in [15, 16]:
            return "D" if d in ["4", "5", "6"] else "H"
        if t == 17:
            return "D" if d in ["3", "4", "5", "6"] else "H"
        if t == 18:
            if d in ["3", "4", "5", "6"]:
                return "D"
            if d in ["2", "7", "8"]:
                return "S"
            return "H"
        if t >= 19:
            return "S"

    t = hand.total
    if t == 9:
        return "D" if d in ["3", "4", "5", "6"] else "H"
    if t == 10:
        return "D" if d in ["2", "3", "4", "5", "6", "7", "8", "9"] else "H"
    if t == 11:
        return "D" if d in ["2", "3", "4", "5", "6", "7", "8", "9", "10"] else "H"
    if t <= 8:
        return "H"
    if t == 12:
        return "S" if d in ["4", "5", "6"] else "H"
    if t in [13, 14, 15, 16]:
        return "S" if d in ["2", "3", "4", "5", "6"] else "H"
    if t >= 17:
        return "S"
    return "H"


def random_card() -> str:
    return random.choice(RANKS)


def generate_scenario() -> Scenario:
    return Scenario(
        player_cards=(random_card(), random_card()),
        dealer_upcard=random_card(),
    )


def hand_kind_label(hand: HandInfo) -> str:
    if hand.is_pair:
        return "Pair"
    if hand.is_soft:
        return "Soft"
    return "Hard"


def format_hand(hand: HandInfo) -> str:
    c1, c2 = hand.cards
    return f"{c1}, {c2} ({hand_kind_label(hand)} {hand.total})"


def explain_move(hand: HandInfo, dealer_up: str, recommended_move: str) -> str:
    dealer = normalize_dealer_upcard(dealer_up)
    if recommended_move == "P":
        return f"Split here because a {hand.pair_rank},{hand.pair_rank} hand plays better as two separate hands against a dealer {dealer}."
    if recommended_move == "D":
        return f"Double here because your {hand_kind_label(hand).lower()} {hand.total} is strong enough to press the edge against a dealer {dealer}."
    if recommended_move == "R":
        return f"Surrender here because {hand_kind_label(hand).lower()} {hand.total} is a poor spot against a dealer {dealer}, so limiting the loss is best."
    if recommended_move == "S":
        return f"Stand here because {hand_kind_label(hand).lower()} {hand.total} is strong enough relative to a dealer {dealer}, and drawing creates more risk than value."
    return f"Hit here because {hand_kind_label(hand).lower()} {hand.total} needs improvement against a dealer {dealer}."


def evaluate_move(scenario: Scenario, chosen_move: str) -> dict:
    recommended_move = scenario.recommended_move
    hand = scenario.hand
    return {
        "chosen_move": chosen_move,
        "chosen_label": MOVE_LABELS[chosen_move],
        "recommended_move": recommended_move,
        "recommended_label": MOVE_LABELS[recommended_move],
        "is_correct": chosen_move == recommended_move,
        "explanation": explain_move(hand, scenario.dealer_upcard, recommended_move),
    }
