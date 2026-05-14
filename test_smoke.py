from app import app
from strategy import HandInfo, Scenario, basic_strategy_move, evaluate_move


def test_strategy_logic_still_works():
    hand = HandInfo(cards=("8", "8"), total=16, is_soft=False, is_pair=True, pair_rank="8")
    assert basic_strategy_move(hand, "10") == "P"


def test_homepage_and_score_flow():
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Blackjack Basic Strategy Trainer" in response.data

        with client.session_transaction() as session:
            session["current_hand"] = {
                "player_cards": ["8", "8"],
                "dealer_upcard": "10",
                "total": 16,
                "hand_kind": "Pair",
            }
            session["score"] = {"correct": 0, "total": 0}
            session["feedback"] = None
            session["answered"] = False

        response = client.post("/answer", data={"move": "P"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Correct." in response.data
        assert b"Split" in response.data

        with client.session_transaction() as session:
            assert session["score"] == {"correct": 1, "total": 1}

        response = client.post("/reset", follow_redirects=True)
        assert response.status_code == 200

        with client.session_transaction() as session:
            assert session["score"] == {"correct": 0, "total": 0}


def test_move_evaluation_exposes_feedback():
    scenario = Scenario(player_cards=("A", "7"), dealer_upcard="9")
    result = evaluate_move(scenario, "S")

    assert result["is_correct"] is False
    assert result["recommended_move"] == "H"
    assert "needs improvement" in result["explanation"]
