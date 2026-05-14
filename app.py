#!/usr/bin/env python3

import os

from flask import Flask, redirect, render_template, request, session, url_for

from strategy import MOVE_LABELS, Scenario, evaluate_move, generate_scenario, hand_kind_label

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")


def build_hand_payload() -> dict:
    scenario = generate_scenario()
    hand = scenario.hand
    return {
        "player_cards": list(scenario.player_cards),
        "dealer_upcard": scenario.dealer_display,
        "total": hand.total,
        "hand_kind": hand_kind_label(hand),
    }


def get_score() -> dict:
    return session.setdefault("score", {"correct": 0, "total": 0})


def get_current_hand() -> dict:
    hand = session.get("current_hand")
    if hand is None:
        hand = build_hand_payload()
        session["current_hand"] = hand
        session["feedback"] = None
        session["answered"] = False
    return hand


def scenario_from_session() -> dict:
    hand = get_current_hand()
    return {
        "player_cards": tuple(hand["player_cards"]),
        "dealer_upcard": hand["dealer_upcard"],
    }


@app.route("/", methods=["GET"])
def index():
    hand = get_current_hand()
    score = get_score()
    feedback = session.get("feedback")
    return render_template(
        "index.html",
        hand=hand,
        score=score,
        feedback=feedback,
        move_labels=MOVE_LABELS,
        answered=session.get("answered", False),
        percentage=(score["correct"] / score["total"] * 100) if score["total"] else 0,
    )


@app.route("/answer", methods=["POST"])
def answer():
    chosen_move = request.form.get("move", "").upper()
    if chosen_move not in MOVE_LABELS:
        return redirect(url_for("index"))

    if session.get("answered", False):
        return redirect(url_for("index"))

    data = scenario_from_session()
    result = evaluate_move(
        Scenario(player_cards=data["player_cards"], dealer_upcard=data["dealer_upcard"]),
        chosen_move,
    )

    score = get_score()
    score["total"] += 1
    if result["is_correct"]:
        score["correct"] += 1
    session["score"] = score
    session["feedback"] = result
    session["answered"] = True
    return redirect(url_for("index"))


@app.route("/next", methods=["POST"])
def next_hand():
    session["current_hand"] = build_hand_payload()
    session["feedback"] = None
    session["answered"] = False
    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset_score():
    session["score"] = {"correct": 0, "total": 0}
    session["feedback"] = None
    session["answered"] = False
    session["current_hand"] = build_hand_payload()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
