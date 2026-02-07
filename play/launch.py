# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  launch.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/07 08:05:31 by roandrie        #+#    #+#               #
#  Updated: 2026/02/07 14:36:11 by roandrie        ###   ########.fr        #
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

from colorama import Cursor

from maze import (MazeConfig, MazeGenerator, MazeConfigError,
                  MazeGenerationError)
from maze.maze_customization import (MAZE, STYLE, DISPLAY_MODE, COLORS)

CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"


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
    position, tracks the move steps, and refreshes the display until the exit
    is reached or the user quits.

    Args:
        maze: The `MazeGenerator` instance containing the grid and logic to be
              played.
    """
    print(CURSOR_HIDE, end="", flush=True)
    player_pos = [maze.entry_x, maze.entry_y]
    steps = 0

    display_text(maze, steps)

    while True:
        old_x, old_y = player_pos[0], player_pos[1]
        new_x, new_y = old_x, old_y

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
            print(Cursor.POS(1, maze.height + maze.y_offset + 3) +
                  f"{COLORS.red}Goodbye 👋{COLORS.reset}")
            print(CURSOR_SHOW, end="", flush=True)
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

                steps += 1
                display_text(maze, steps)

                curs_old_x = (old_x * maze.step_x) + 1
                curs_old_y = old_y + maze.y_offset
                curs_new_x = (new_x * maze.step_x) + 1
                curs_new_y = new_y + maze.y_offset

                if maze.display == DISPLAY_MODE.emoji:
                    print(Cursor.POS(curs_old_x, curs_old_y) +
                          f"{maze.visual_empty}{COLORS.reset}", end="",
                          flush=True)
                    print(Cursor.POS(curs_new_x, curs_new_y) +
                          f"{maze.visual_entry}{COLORS.reset}", end="",
                          flush=True)

                if maze.display in (DISPLAY_MODE.ascii, DISPLAY_MODE.simple):
                    print(Cursor.POS(curs_old_x, curs_old_y) +
                          f"{maze.visual_empty}{COLORS.reset}", end="",
                          flush=True)
                    print(Cursor.POS(curs_new_x, curs_new_y) +
                          f"{maze.visual_entry}{COLORS.reset}", end="",
                          flush=True)

        if (new_x == maze.exit_x and new_y == maze.exit_y):
            print(Cursor.POS(1, maze.height + maze.y_offset + 3) +
                  f"{COLORS.lightgreen}🎆🎆 GG! 🎆🎆{COLORS.reset}")
            print(CURSOR_SHOW, end="", flush=True)
            break


def display_text(maze: "MazeGenerator", steps: int) -> None:
    """Render the status text below the maze.

    Displays the quit instruction and the current step count. The text is
    centered horizontally relative to the maze width and positioned on the
    line immediately following the maze bottom margin.

    Args:
        maze: The `MazeGenerator` instance used to calculate positioning.
        steps: The current number of steps taken by the player.
    """
    if steps > 0:
        text_infos = f"Quit: 'E' | Steps: {steps}"
    else:
        text_infos = f"Quit: 'E' | Step: {steps}"
    line_y = maze.height + maze.y_offset + 1

    visual_width = maze.width // 2
    padding = " " * max(0, (visual_width - len(text_infos)) // 2)

    print(Cursor.POS(1, line_y) + f"{padding}{text_infos}{STYLE.reset}",
          end="", flush=True)


if __name__ == "__main__":
    launch_game()
