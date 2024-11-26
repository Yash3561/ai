import pygame
import time
from config import wumpus_position, glitter_position, agent_position
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
        print(f"No path found using {algorithm_name}!")
        return

    ai_path = []
    for move in path:
        agent_position = move
        ai_path.append(agent_position)  # Add move to the AI's path
        draw_grid(screen, agent_position, font, ai_path)  # Pass the path to the grid drawing
        pygame.display.flip()
        time.sleep(0.5)  # Pause to visualize AI movement

        # Check if agent reaches glitter
        if agent_position == glitter_position:
            print(f"{algorithm_name} found the glitter!")
            return len(path)  # Return the path length
        elif agent_position == wumpus_position:
            print(f"{algorithm_name}: Wumpus killed you! Try again!")
            return None
    return len(path)

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
    results["DFS"] = execute_algorithm(dfs, start, goal, "DFS")
    results["BFS"] = execute_algorithm(bfs, start, goal, "BFS")
    results["A*"] = execute_algorithm(a_star, start, goal, "A*")
    results["Dijkstra"] = execute_algorithm(dijkstra, start, goal, "Dijkstra")

    # Check if any algorithm found a path
    valid_results = {algo: length for algo, length in results.items() if length is not None}
    if not valid_results:
        print("No valid path found by any algorithm.")
        return

    # Find the best algorithm
    best_algo = min(valid_results, key=valid_results.get)
    print("Comparison Complete!")
    print("Results:")
    for algo, length in results.items():
        if length is not None:
            print(f"{algo}: Path Length = {length}")
        else:
            print(f"{algo}: No Path Found")
    print(f"Best Algorithm: {best_algo} (Shortest Path)")


# Function to handle manual input for movement
def handle_manual_input():
    global agent_position
    path = [agent_position]  # Start the path with the agent's initial position
    running = True
    while running:
        draw_grid(screen, agent_position, font, path)  # Pass the path to the grid drawing
        pygame.display.flip()

        # Check if agent reaches glitter
        if agent_position == glitter_position:
            print("You found the glitter! Congratulations!")
            running = False
        elif agent_position == wumpus_position:
            print("Wumpus Killed You! Try Again!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    agent_position = move_agent(agent_position[0], agent_position[1], "up")
                if event.key == pygame.K_DOWN:
                    agent_position = move_agent(agent_position[0], agent_position[1], "down")
                if event.key == pygame.K_LEFT:
                    agent_position = move_agent(agent_position[0], agent_position[1], "left")
                if event.key == pygame.K_RIGHT:
                    agent_position = move_agent(agent_position[0], agent_position[1], "right")
                
                path.append(agent_position)  # Add new position to the path
                time.sleep(0.1)  # Small delay for smooth movement

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

if __name__ == "__main__":
    main()
