def get_unique_states(current_states, is_p1_turn):
    next_states = set()
    
    for state in current_states:
        p1, p2 = state
        # Safety check: skip processing if an existing invalid state somehow slipped through
        if sum(p1) == 0 or sum(p2) == 0:
            continue
            
        active_player = list(p1) if is_p1_turn else list(p2)
        opponent = list(p2) if is_p1_turn else list(p1)
        
        # --- ATTACK MOVES ---
        for i, active_hand in enumerate(active_player):
            if active_hand == 0: 
                continue  # A dead hand cannot attack
                
            for j, opp_hand in enumerate(opponent):
                if opp_hand == 0: 
                    continue  # Cannot attack an already dead hand
                
                # Calculate attack
                new_opp_hand = (opp_hand + active_hand) % 5
                new_opp = opponent.copy()
                new_opp[j] = new_opp_hand
                
                # Standardize state by sorting hand pairs
                active_sorted = tuple(sorted(active_player))
                opp_sorted = tuple(sorted(new_opp))
                
                # --- LOSS CONDITION FILTER ---
                # Check if this move completely wiped out the opponent's hands (0, 0)
                if sum(opp_sorted) == 0:
                    continue  # Skip adding this state since the game is over
                
                if is_p1_turn:
                    next_states.add((active_sorted, opp_sorted))
                else:
                    next_states.add((opp_sorted, active_sorted))
                        
    return next_states

# Simulation Setup
rounds = int(input("Number of rounds: "))
round_states = {((1, 1), (1, 1))}

print(f"Starting position: {len(round_states)} state")
for r in range(1, rounds + 1):
    # Player 1's Turn (Odd Turn)
    round_states = get_unique_states(round_states, is_p1_turn=True)
    print(f"Turn {(r*2)-1} (P1): {len(round_states)} ongoing unique states")
    
    # Player 2's Turn (Even Turn)
    round_states = get_unique_states(round_states, is_p1_turn=False)
    print(f"Turn {r*2} (P2): {len(round_states)} ongoing unique states")
