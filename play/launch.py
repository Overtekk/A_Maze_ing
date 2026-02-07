# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  launch.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/07 08:05:31 by roandrie        #+#    #+#               #
#  Updated: 2026/02/07 10:51:36 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Interactive maze game launcher.

This script serves as the entry point for the "play" mode of the application.
It initializes a maze based on a configuration file, generates the layout, and
enters an interactive loop where the user can navigate the maze using keyboard
controls.
"""

import sys
import readchar
import time

from maze import (MazeConfig, MazeGenerator, MazeConfigError,
                  MazeGenerationError)
from maze.maze_customization import (MAZE, ANIM, STYLE, ALGO_MODE,
                                     DISPLAY_MODE, COLORS)


def launch_game() -> None:
    """Initialize the environment and start the game session.

    This function attempts to load the maze configuration and generate a new
    maze. If successful, it passes the generated maze to the game loop.
    Initialization errors (missing file, invalid config) are caught and
    printed to stderr.
    """
    try:
        maze_configuration = MazeConfig.from_config_file("play/config.txt")

        maze = MazeGenerator(maze_configuration)
        maze.maze_generator(rendering=True)
    except (FileNotFoundError, ValueError, MazeConfigError,
            MazeGenerationError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
    play(maze)


def play(maze: "MazeGenerator") -> None:
    """Run the main interactive game loop.

    Listens for user input via keyboard to move the player character through
    the maze. It handles collision detection with walls, updates the player's
    position, tracks the move count, and refreshes the display until the exit
    is reached or the user quits.

    Args:
        maze: The `MazeGenerator` instance containing the grid and logic to be
              played.
    """
    player_pos = [maze.entry_x, maze.entry_y]
    count = 0

    while True:
        old_x, old_y = player_pos[0], player_pos[1]
        new_x, new_y = old_x, old_y

        if (new_x == maze.exit_x and new_y == maze.exit_y):
            print(f"{COLORS.lightgreen}\n🎆🎆 GG! 🎆🎆{COLORS.reset}")
            break

        k = readchar.readkey()

        if k == 'w':
            new_y = old_y - 1
        elif k == 's':
            new_y = old_y + 1
        elif k == 'a':
            new_x = old_x - 1
        elif k == 'd':
            new_x = old_x + 1
        elif k == 'e':
            print(f"\n{COLORS.red}Goodbye 👋{COLORS.reset}")
            break

        if (new_x, new_y) != (old_x, old_y):
            if maze.maze[(new_x, new_y)] in (MAZE.wall, MAZE.fortytwo):
                new_x, new_y = old_x, old_y
                continue
            else:
                maze.maze[(old_x, old_y)] = MAZE.empty
                player_pos[0], player_pos[1] = new_x, new_y
                maze.maze[(new_x, new_y)] = MAZE.entry
                maze.entry_x, maze.entry_y = new_x, new_y
                count += 1
                print(ANIM.clear_screen)
                display_text(maze, count)
                maze.print_maze()
                time.sleep(500/1000)


def display_text(maze: "MazeGenerator", count: int) -> None:
    """Print small summary text above the rendered maze.

    The function chooses a centered title string and a brief line
    describing the current algorithm, display mode, the k to quit the
    game and the number of walks.

    Args:
        maze: The `MazeGenerator` used to derive display properties.
        count: The number of walks the player have done.
    """
    text_generated = "-Maze Generated-"
    if maze.algorithm == ALGO_MODE.rb:
        text_algo_display = "Mode: recursive backtracking"
    if maze.algorithm == ALGO_MODE.hunt_kill:
        text_algo_display = "Mode: hunt and kill"
    text_algo_display += f" | Display: {maze.display}"
    text_quit_count = "Quit: 'e'"
    if count > 0:
        text_quit_count += f"| Count: {count}"

    if maze.display in (DISPLAY_MODE.ascii, DISPLAY_MODE.emoji):
        visual_width = maze.width
    else:
        visual_width = maze.width // 2

    filling = " " * max(0, ((visual_width - (len(text_generated) // 2))))
    print(f"\r{maze.txt_white}{filling}{text_generated}    ")

    filling = " " * max(0, ((visual_width - (len(text_algo_display) // 2))))
    print(f"\r{filling}{text_algo_display}{STYLE.reset}")

    filling = " " * max(0, ((visual_width - (len(text_quit_count) // 2))))
    print(f"\r{filling}{text_quit_count}{STYLE.reset}")


if __name__ == "__main__":
    launch_game()
