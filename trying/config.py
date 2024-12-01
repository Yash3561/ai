import random

MAX_GRID_SIZE = 50
def get_user_input():
    """Function to take user input for the number of Wumpus, pits, and glitter."""
    global GRID_SIZE
    try:
        print("\n\nWELCOME TO THE WUMPUS WORLD PROGRAM!")
        print("\nPlease enter details as asked to avoid issues.")
        
        # Input for grid size with a limit
        GRID_SIZE = int(input(f"\nEnter the size of Grid (for N x N enter only N, max {MAX_GRID_SIZE}): "))
        if GRID_SIZE > MAX_GRID_SIZE:
            print(f"\nGrid size too large. Setting to maximum allowable size: {MAX_GRID_SIZE}")
            GRID_SIZE = MAX_GRID_SIZE

        max_objects = GRID_SIZE * GRID_SIZE - 2  # Reserve space for (0,0) and one empty cell
        num_wumpus = int(input(f"\nEnter the number of Wumpus (max {max_objects}): "))
        num_pits = int(input(f"\nEnter the number of Pits (max {max_objects - num_wumpus}): "))
        num_glitter = 1  # Only one gold piece is allowed

        # Validate total objects
        if num_wumpus + num_pits + num_glitter > max_objects:
            print("\nToo many objects for the grid. Adjusting numbers to fit the grid.")
            num_wumpus = min(num_wumpus, max_objects - num_pits - num_glitter)
            num_pits = min(num_pits, max_objects - num_wumpus - num_glitter)

        return GRID_SIZE, num_wumpus, num_pits, num_glitter
    
    except ValueError:
        print("Invalid input. Please enter integer values.")
        return get_user_input()  # Retry if input is invalid

def generate_random_positions(num_wumpus, num_pits, num_glitter):
    """Function to generate random positions for Wumpus, pits, and glitter."""
    # Exclude (0,0) from available positions
    available_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if (x, y) != (0, 0)]

    # Generate random positions
    positions = random.sample(available_positions, num_wumpus + num_pits + num_glitter)
    
    # Separate positions for Wumpus, pits, and glitter
    wumpus_positions = positions[:num_wumpus]
    pit_positions = positions[num_wumpus:num_wumpus + num_pits]
    glitter_position = positions[-1]  # Glitter position is the last one

    return wumpus_positions, pit_positions, glitter_position

# Get user input for number of Wumpus, pits, and glitter
GRID_SIZE, num_wumpus, num_pits, num_glitter = get_user_input()

# Generate random positions for these objects
wumpus_position, pit_position, glitter_position = generate_random_positions(num_wumpus, num_pits, num_glitter)

# Agent's starting position (fixed)
agent_position = (0, 0)  # Starting point of the agent


