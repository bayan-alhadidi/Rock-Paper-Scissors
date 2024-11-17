import random

def detect_abbey(player_history, opponent_history):
    """
    Detect Abbey by analyzing opponent's responses to our history.
    """
    if len(player_history) < 3:
        return False  # Not enough data for detection

    # Rebuild the pair frequency dictionary from player_history
    play_order = {
        "RR": 0, "RP": 0, "RS": 0,
        "PR": 0, "PP": 0, "PS": 0,
        "SR": 0, "SP": 0, "SS": 0,
    }

    for i in range(len(player_history) - 1):
        pair = player_history[i] + player_history[i + 1]
        if pair in play_order:
            play_order[pair] += 1

    # Predict Abbey's expected move based on the most frequent pair
    last_two = player_history[-2:]
    if len(last_two) == 2:
        last_two = last_two[0] + last_two[1]
        potential_plays = [last_two[1] + move for move in "RPS"]
        sub_order = {k: play_order[k] for k in potential_plays if k in play_order}
        if sub_order:
            prediction = max(sub_order, key=sub_order.get)[-1]
            ideal_response = {"P": "S", "R": "P", "S": "R"}
            abbey_expected_move = ideal_response[prediction]

            # Check if opponent's last move matches Abbey's expected move
            if opponent_history[-1] == abbey_expected_move:
                return True  # Likely Abbey

    return False

def defeat_abbey(player_history):
    """
    Counter Abbey by predicting his expected move and countering it.
    """
    if len(player_history) < 2:
        return random.choice(["R", "P", "S"])  # Not enough data, choose randomly

    # Rebuild the pair frequency dictionary
    play_order = {
        "RR": 0, "RP": 0, "RS": 0,
        "PR": 0, "PP": 0, "PS": 0,
        "SR": 0, "SP": 0, "SS": 0,
    }

    for i in range(len(player_history) - 1):
        pair = player_history[i] + player_history[i + 1]
        if pair in play_order:
            play_order[pair] += 1

    # Predict Abbey's expected move based on our most frequent pair
    last_two = player_history[-2:]
    if len(last_two) == 2:
        last_two = last_two[0] + last_two[1]
        potential_plays = [last_two[1] + move for move in "RPS"]
        sub_order = {k: play_order[k] for k in potential_plays if k in play_order}
        if sub_order:
            prediction = max(sub_order, key=sub_order.get)[-1]
            ideal_response = {"P": "S", "R": "P", "S": "R"}
            abbey_expected_move = ideal_response[prediction]
            counter_move = {"P": "S", "R": "P", "S": "R"}
            return counter_move[abbey_expected_move]

    return random.choice(["R", "P", "S"])  # Fallback to random move

def detect_quincy_pattern(opponent_history):
    quincy_sequence = ["R", "R", "P", "P", "S"]
    sequence_length = len(quincy_sequence)

    # Check for a repeating pattern in last 5 moves or anywhere in last 10 moves
    last_moves = opponent_history[-sequence_length:]
    if last_moves == quincy_sequence:
        return True

    # Additional check for any recent repeating sequence
    if len(opponent_history) >= 10:
        recent_moves = opponent_history[-10:]
        for start in range(5):
            if recent_moves[start:start + sequence_length] == quincy_sequence:
                return True

    return False

def player(prev_play, opponent_history=[], player_history=[], 
    strategy_state={"strategy": "default", "quincy_index": 0, "test_phase": True, "test_moves": []}):

    # Track opponent's moves
    if prev_play:
        opponent_history.append(prev_play)

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if len(opponent_history) > 10:
        if opponent_history[-1] == ideal_response[player_history[-2]]:
            strategy_state["strategy"] = "kris"
        elif detect_quincy_pattern(opponent_history):
            strategy_state["strategy"] = "quincy"
        elif detect_abbey(player_history, opponent_history):
            strategy_state["strategy"] = "abbey"
        else:
            strategy_state["strategy"] = "default"

     # Abbey Strategy
    if strategy_state["strategy"] == "abbey":
        my_next_move = defeat_abbey(player_history)
        player_history.append(my_next_move)
        return my_next_move

    # Quincy Strategy
    if strategy_state["strategy"] == "quincy":
        quincy_sequence = ["R", "R", "P", "P", "S"]
        predicted_move = quincy_sequence[strategy_state["quincy_index"] % len(quincy_sequence)]
        my_next_move = ideal_response[predicted_move]
        player_history.append(my_next_move)
        strategy_state["quincy_index"] += 1  # Increment to track position in sequence
        return my_next_move

    # Kris Strategy (similar counter to Kris’s predictability)
    if strategy_state["strategy"] == "kris":
        if player_history[-1]:
            kris_predicted_move = ideal_response[player_history[-1]]
            my_next_move = ideal_response[kris_predicted_move]
        else:
            my_next_move = "R"
        player_history.append(my_next_move)
        return my_next_move

    # Default: Random move if no pattern is detected
    my_next_move = random.choice(["R", "P", "S"])
    player_history.append(my_next_move)
    return my_next_move
