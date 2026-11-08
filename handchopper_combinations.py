def get_unique_states_raw(current_states):
    """
    Generates all valid next-state transitions from a given set of input states.
    It returns a raw list that deliberately preserves duplicate pathways so 
    we can accurately track how many duplicate states that needs to be removed.
    """
    next_states_list = []
    
    # Iterate through every game configuration present in the current layer
    for state in current_states:
        # Unpack the three-element state layout structure
        p1, p2, turn = state
        
        # Determine active turn order logic (True if Player 1's turn, False if Player 2's)
        is_p1_turn = (turn == 1)
        
        # Assign pointer roles based on whose turn it currently is to act
        active_player = list(p1) if is_p1_turn else list(p2)
        opponent = list(p2) if is_p1_turn else list(p1)
        
        # --- ATTACK MOVES GENERATION ---
        # Outer Loop: Loop through the active player's hands
        for i, active_hand in enumerate(active_player):
            if active_hand == 0: 
                continue  # Bug Fix: A dead hand (0 fingers) cannot execute an attack
                
            # Inner Loop: Loop through the opponent's hands to select a target
            for j, opp_hand in enumerate(opponent):
                if opp_hand == 0: 
                    continue  # Bug Fix: You cannot attack an opponent's already dead hand
                
                # Chopsticks Attack Math: Add values and apply modular rollover limit of 5.
                # (e.g., 3 + 4 = 7 -> 7 % 5 = 2. If it reaches exactly 5 -> 5 % 5 = 0, killing the hand)
                new_opp_hand = (opp_hand + active_hand) % 5
                
                # Clone the opponent's hand setup and write the new value into the targeted hand index
                new_opp = opponent.copy()
                new_opp[j] = new_opp_hand
                
                # Hand Symmetrical Standardization: Sort the hands min-to-max.
                # This ensures a layout like (4, 1) is immediately read as (1, 4),
                # eliminating left/right hand tracking duplication.
                active_sorted = tuple(sorted(active_player))
                opp_sorted = tuple(sorted(new_opp))
                
                # --- ACTIVE GAMEPLAY LOSS FILTER ---
                # Calculate the sum of the opponent's fingers. If it equals 0, both hands are dead (0, 0).
                # We can skip adding this to the state engine because terminal end-game states are not ongoing play but we are leaving it for now.
                #if sum(opp_sorted) == 0:
                #    continue
                
                # Appending 1 for Player 1's turn and 2 for Player 2's turn to indicate the player's current turn
                if is_p1_turn:
                    # Player 1 attacked. The next state belongs to Player 2 (turn index 2)
                    next_states_list.append((active_sorted, opp_sorted, 2))
                else:
                    # Player 2 attacked. The next state belongs to Player 1 (turn index 1)
                    next_states_list.append((opp_sorted, active_sorted, 1))
                        
    return next_states_list

# ==========================================
#          SIMULATION ENGINE SETUP
# ==========================================

# Input the number of turns
turns = int(input("Enter number of turns to simulate: "))

# Initialize the root tree pointer: Format is ((P1_Left, P1_Right), (P2_Left, P2_Right), Active_Turn)
# Game starts at standard ((1, 1), (1, 1)) with Player 1 set to move first (1)
current_layer = {((1, 1), (1, 1), 1)}

# Maintain a master hash set keeping track of every single unique state discovered across history
all_discovered_states = set(current_layer)

# Metric Accumulation Counters
total_raw_generated = 0
total_layer_duplicates = 0
total_historical_duplicates = 0

print(f"\nStarting position initialized: {len(current_layer)} state\n")

# Main simulation loop processing one step/turn at a time
for t in range(1, turns + 1):
    # Performance Safety Check: If the tree runs completely dry of valid active states, break early
    if not current_layer:
        print(f"Game tree fully exhausted at turn {t-1}. No more active states left to process.")
        break
        
    # Set display string label for clear tracking output metrics
    player_label = "P1" if t % 2 != 0 else "P2"
    
    # Step 1: Run the attack engine to compute ALL raw possible moving vectors from the active layer
    raw_next_list = get_unique_states_raw(current_layer)
    raw_count = len(raw_next_list)
    total_raw_generated += raw_count
    
    # Step 2: Calculate Intra-Turn Duplicates
    # Forcing the raw list into a set automatically collapses identical states generated on this exact turn.
    unique_next_set = set(raw_next_list)
    layer_duplicates = raw_count - len(unique_next_set)
    total_layer_duplicates += layer_duplicates
    
    # Step 3: Calculate Historical Duplicates
    # Using set difference subtraction (-) removes any states we have already visited in earlier turns.
    new_states_isolated = unique_next_set - all_discovered_states
    historical_duplicates = len(unique_next_set) - len(new_states_isolated)
    total_historical_duplicates += historical_duplicates
    
    # Master Record Ledger Updates:
    # Use .update() to quickly push the brand-new states into our historical tracking log
    all_discovered_states.update(new_states_isolated)
    
    # Shift the current engine layer forward to become the seed state pool for the next turn loop iteration
    current_layer = unique_next_set  
    
    # Display the breakdown metrics for the completed turn phase
    print(f"Turn {t} ({player_label}):")
    print(f"  -> Generated {raw_count} raw paths")
    print(f"  -> Removed {layer_duplicates} intra-turn duplicates")
    print(f"  -> Removed {historical_duplicates} already-seen historical states")
    print(f"  -> New unique configurations discovered this turn: {len(new_states_isolated)}")
    print(f"  -> Cumulative unique states discovered overall so far: {len(all_discovered_states)}\n")

# Print the final compiled structural report metrics summary
print("==================================================")
print(f"Total Raw Game Transitions Generated : {total_raw_generated}")
print(f"Total Intra-Turn Duplicates Removed  : {total_layer_duplicates}")
print(f"Total Historical Duplicates Removed  : {total_historical_duplicates}")
print(f"Total Deduplicated Elements Removed  : {total_layer_duplicates + total_historical_duplicates}")
print(f"Total Unique Game Tree Configurations Discovered : {len(all_discovered_states)}")
print("==================================================")
