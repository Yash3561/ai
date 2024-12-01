import random

def get_user_input():
    """Function to take user input for the number of Wumpus, pits, and glitter."""
    global GRID_SIZE 
    try:
            
        print("\n\nWECLOME TO THE WUMPUS WORLD PROGRAM !")
        print("\nPlease enter details as asked to have no issues.")
        GRID_SIZE = int(input(f"\nEnter the size of Grid (for N x N enter only N): "))
        num_wumpus = int(input(f"\nEnter the number of Wumpus (max {GRID_SIZE * GRID_SIZE - 1}): "))
        num_pits = int(input(f"\nEnter the number of Pits (max {GRID_SIZE * GRID_SIZE - 1}): "))
        num_glitter = 1

        # Ensure user doesn't input too many objects
        if num_wumpus + num_pits + num_glitter > GRID_SIZE * GRID_SIZE - 1:
            print("\nToo many objects for the grid. Reducing the number of objects.")
            return GRID_SIZE * GRID_SIZE - 1, 0, 1  # Default to max grid capacity, only 1 glitter allowed

        return GRID_SIZE, num_wumpus, num_pits, num_glitter
    
    except ValueError:
        print("Invalid input. Please enter integer values.")
        return get_user_input()  # Retry if input is invalid

# Function to generate random positions for Wumpus, pits, and glitter
def generate_random_positions(num_wumpus, num_pits, num_glitter):
    # Generate all possible grid positions
    positions = random.sample([(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)], num_wumpus + num_pits + num_glitter)
    
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

