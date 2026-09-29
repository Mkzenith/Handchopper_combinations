
def get_next_states(state, is_p1_turn):
    """
    Generates all valid next unique board states from the current state.
    state format: ((p1_left, p1_right), (p2_left, p2_right))
    Values are always sorted to eliminate left/right duplicates.
    """
    p1, p2 = state
    
    # Extract only active hands (hands with fingers > 0)
    p1_active = [h for h in p1 if h > 0]
    p2_active = [h for h in p2 if h > 0]
    
    # If either player has zero active hands, the game is already over
    if not p1_active or not p2_active:
        return set()
        
    next_states = set()
    
    if is_p1_turn:
        # Player 1 attacks Player 2
        for attacker in p1_active:
            for i, defender in enumerate(p2):
                if defender > 0:  # Can only attack live hands
                    new_val = (defender + attacker) % 5
                    
                    # Construct the updated hand array for P2
                    new_p2 = list(p2)
                    new_p2[i] = new_val
                    
                    # Convert to sorted tuples to ensure combination uniqueness
                    next_states.add((tuple(sorted(p1)), tuple(sorted(new_p2))))
    else:
        # Player 2 attacks Player 1
        for attacker in p2_active:
            for i, defender in enumerate(p1):
                if defender > 0:  # Can only attack live hands
                    new_val = (defender + attacker) % 5
                    
                    # Construct the updated hand array for P1
                    new_p1 = list(p1)
                    new_p1[i] = new_val
                    
                    # Convert to sorted tuples to ensure combination uniqueness
                    next_states.add((tuple(sorted(new_p1)), tuple(sorted(p2))))
                    
    return next_states


def simulate_chopsticks():
    # Prompt user for the number of rounds (1 round = 2 turns)
    try:
        rounds = int(input("Number of rounds to simulate: "))
    except ValueError:
        print("Please enter a valid integer.")
        return
        
    total_turns = rounds * 2
    
    # Starting state: both players have (1, 1)
    # Using a set to keep track of unique active states at the current depth
    current_states = {((1, 1), (1, 1))}
    
    print("\n--- Unique Combinations per Turn ---")
    
    for turn in range(1, total_turns + 1):
        next_level_states = set()
        
        # P1 moves on odd turns, P2 moves on even turns
        is_p1_turn = (turn % 2 != 0)
        
        for state in current_states:
            # Gather all branches resulting from the current board states
            next_level_states.update(get_next_states(state, is_p1_turn))
            
        current_states = next_level_states
        
        # Output the absolute number of unique combinations possible at this turn boundary
        print(f"Turn {turn:02d}: {len(current_states)} unique board combinations {current_states}")
        
        # If no states are left, everyone has lost or hit a terminal wall
        if not current_states:
            print("No further moves possible.")
            break

if __name__ == "__main__":
    simulate_chopsticks()