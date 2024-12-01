import pygame
import time
from config import GRID_SIZE, wumpus_position, glitter_position, agent_position, pit_position
from agent import move_agent
from ai import bfs, dfs, dijkstra, a_star
from grid import draw_grid

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus World Game")

# Font for text
font = pygame.font.SysFont(None, 30)

# Function to execute AI algorithm and visualize path
def execute_algorithm(algorithm, start, goal, algorithm_name):
    global agent_position
    path = algorithm(start, goal)
    
    if not path:
        print(f"\n - No path found using {algorithm_name}!")
        return None

    ai_path = []
    for move in path:
        agent_position = move
        ai_path.append(agent_position)  # Add move to the AI's path
        draw_grid(screen, agent_position, font, ai_path)  # Pass the path to the grid drawing
        pygame.display.flip()
        time.sleep(0.5)

        if agent_position == glitter_position:
            print(f"\n  - {algorithm_name} found the glitter and grabbed the gold!")
            grab_gold(ai_path)  # Call the function to grab gold and return to (0, 0)
            return len(path)  # Return the length of the path instead of the path

    return len(path)  # Return path length


def grab_gold(path_to_gold):
    global agent_position
    print("\n - Gold Grabbed! Now returning to the start...")

    # Reverse the path to return to (0, 0)
    path_to_start = path_to_gold[::-1]  # Reverse the path

    # Move agent back to start following the reversed path
    for move in path_to_start:
        agent_position = move
        draw_grid(screen, agent_position, font, path_to_start)  # Visualize path to start
        pygame.display.flip()
        time.sleep(0.5)

        # Check if agent reaches the start position again
        if agent_position == (0, 0):
            print("\n - Agent has returned to the start!")
            break

# AI mode with algorithm selection
def ai_mode():
    global agent_position
    agent_position = (0, 0)  # Reset agent's starting position
    start = (0, 0)
    goal = glitter_position

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Display algorithm options
        options = [
            "Press D for DFS",
            "Press B for BFS",
            "Press A for A*",
            "Press K for Dijkstra",
            "Press C to Compare All",
            "Press ESC to go back"
        ]
        for idx, option in enumerate(options):
            text = font.render(option, True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, 50 + idx * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:  # DFS
                    execute_algorithm(dfs, start, goal, "DFS")
                elif event.key == pygame.K_b:  # BFS
                    execute_algorithm(bfs, start, goal, "BFS")
                elif event.key == pygame.K_a:  # A*
                    execute_algorithm(a_star, start, goal, "A*")
                elif event.key == pygame.K_k:  # Dijkstra
                    execute_algorithm(dijkstra, start, goal, "Dijkstra")
                elif event.key == pygame.K_c:  # Compare All
                    compare_algorithms(start, goal)
                elif event.key == pygame.K_ESCAPE:  # Back to main menu
                    running = False
                    
def compare_algorithms(start, goal):
    results = {}

    # Execute each algorithm and record results
    print("Comparing algorithms...")
    start_time_dfs = time.time()
    results["DFS"] = execute_algorithm(dfs, start, goal, "DFS")
    end_time_dfs = time.time()
    
    start_time_bfs = time.time()
    results["BFS"] = execute_algorithm(bfs, start, goal, "BFS")
    end_time_bfs = time.time()
    
    start_time_astar = time.time()
    results["A*"] = execute_algorithm(a_star, start, goal, "A*")
    end_time_astar = time.time()
    
    start_time_dij = time.time()
    results["Dijkstra"] = execute_algorithm(dijkstra, start, goal, "Dijkstra")
    end_time_dij = time.time()

    # Remove None results (no path found)
    valid_results = {algo: length for algo, length in results.items() if length is not None}
    
    if not valid_results:
        print("\n - No valid path found by any algorithm.")
        return

    # # Find the best algorithm by comparing the lengths of the paths
    # best_algo = min(valid_results, key=valid_results.get)
    
    # Print comparison results
    print("\n\nExecution Complete!")
    print("\n\nResults:")
    print("\nEXECUTION TIME: ")
    print(f"\n    - DFS Execution Time: {end_time_dfs - start_time_dfs:.4f} seconds")
    print(f"\n    - BFS Execution Time: {end_time_bfs - start_time_bfs:.4f} seconds")
    print(f"\n    - A* Execution Time: {end_time_astar - start_time_astar:.4f} seconds")
    print(f"\n    - Dijkstra Execution Time: {end_time_dij - start_time_dij:.4f} seconds")
    
    print("\nSEARCH COST: ")
    for algo, length in results.items():
        if length is not None:
            print(f"\n  -{algo}: Path Length = {length}")
        else:
            print(f"\n  -{algo}: No Path Found")
    
    # print(f"Best Algorithm: {best_algo} (Shortest Path)")

def handle_manual_input():
    global agent_position
    agent_position = (0, 0)  # Reset the agent's position to the start (0, 0)
    path = [agent_position]  # Start the path with the agent's initial position
    visited_feedback = set()  # Track positions for which feedback is already shown
    running = True
    print("\n\n USING A*, to show you best optimal solution in case you didn't find:")
    optimal_path = a_star((0, 0), glitter_position)
    
    print("\n\n YOUR PATH:")
    while running:
        # Draw the grid with the path and agent's current position
        draw_grid(screen, agent_position, font, path)  
        pygame.display.flip()

        # Agent's current position
        agent_x, agent_y = agent_position

        # Check adjacent cells for Breeze (pit) and Stench (Wumpus)
        breeze = []
        stench = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = agent_x + dx, agent_y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (nx, ny) in pit_position:  # Check if pit is near
                    breeze.append((nx, ny))
                if (nx, ny) in wumpus_position:  # Check if Wumpus is near
                    stench.append((nx, ny))

        # Provide feedback only if it's a new position
        if (agent_position not in visited_feedback):
            if breeze:
                print("\n - Feeling Breeze!")
            if stench:
                print("\n - Smelling Stench!")
            visited_feedback.add(agent_position)  # Mark the position as visited for feedback

        # Check if agent reaches glitter
        if agent_position == glitter_position:
            print("\n - You found the glitter! Congratulations!")
            grab_gold_manually(path)  # Use the recorded path for backtracking
            check_optimality(path, optimal_path)
            running = False
            continue

        # Check if agent falls into a pit or encounters Wumpus
        if agent_position in pit_position:
            print("\n - You fell into a pit! Game over!")
            running = False
            continue
        elif agent_position in wumpus_position:
            print("\n - The Wumpus killed you! Game over!")
            running = False
            continue

        # Handle key events for movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_position = move_agent(agent_position[0], agent_position[1], "up")
                elif event.key == pygame.K_DOWN:
                    new_position = move_agent(agent_position[0], agent_position[1], "down")
                elif event.key == pygame.K_LEFT:
                    new_position = move_agent(agent_position[0], agent_position[1], "left")
                elif event.key == pygame.K_RIGHT:
                    new_position = move_agent(agent_position[0], agent_position[1], "right")
                else:
                    continue

                # Add to path only if it's a valid move
                if new_position != agent_position:
                    agent_position = new_position
                    path.append(agent_position)  # Add the new position to the path
                time.sleep(0.1)  # Small delay for smoother movement
                


def grab_gold_manually(path_to_gold):
    print("\n - Gold Grabbed! Returning to the start...")

    # Reverse the path to return to (0, 0)
    path_to_start = path_to_gold[::-1]  # Reverse the path

    for move in path_to_start:
        global agent_position
        agent_position = move
        draw_grid(screen, agent_position, font, path_to_start)  # Pass only the path to draw_grid
        pygame.display.flip()
        time.sleep(0.5)

    print("\n - Agent has successfully returned to the start!")
    
def check_optimality(user_path, optimal_path):
    # Compare lengths of the user path and the optimal path
    user_path_length = len(user_path)
    optimal_path_length = len(optimal_path)

    # Feedback based on comparison
    if user_path_length < optimal_path_length:
        print("\n - Your path was optimal! Great job!")
    else:
        print(f"\n - Your path was not optimal. The optimal path was {optimal_path_length} steps.")
        print(f"\n - Suggestions: Try to avoid unnecessary detours. Consider using a more direct route.")
        print(f"\n - Here's the optimal path: {optimal_path}")

    # Optionally, display the paths for comparison
    print(f"\n - Your path: {user_path}")
    print(f"\n - Optimal path: {optimal_path}")


# Main function to choose between manual and AI mode
def main():
    global agent_position
    agent_position = (0, 0)  # Reset agent's starting position

    # Main loop
    running = True
    while running:
        screen.fill((0, 0, 0))

        # Display options for manual or AI mode
        text = font.render("Press M for Manual, A for AI, ESC to Exit", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Manual mode
                    handle_manual_input()
                elif event.key == pygame.K_a:  # AI mode
                    ai_mode()
                elif event.key == pygame.K_ESCAPE:  # Exit
                    running = False

    pygame.quit()
    print("THANKYOU FOR USING THIS PROGRAM! HAVE A GOOD DAY! :)")

if __name__ == "__main__":
    main()
