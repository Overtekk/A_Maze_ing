# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/20 16:25:20 by roandrie        #+#    #+#               #
#  Updated: 2026/02/03 12:47:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Main script for the Maze Generator.

First, we check if all dependencies are installed. If no error have been found,
we can import everything and start to check the config file.
Then, construct the maze, output it and launch the 'game'.
"""

import sys
import time
import random

from src.utils import module_checker, ArgumentsError


def main() -> int:
    """"Programm main entry point.

    Returns:
        int: 0 if no error occured, 1 or 2 otherwise.

    """
    try:
        try:
            module_checker()
        except ModuleNotFoundError as e:
            print(f"{type(e).__name__}: {e}", file=sys.stderr)
            return 2

        from colorama import Cursor

        from src.maze import (MazeConfig, MazeConfigError, MazeGenerationError,
                              MazeGenerator, MazeSolver)
        from src.maze.maze_customization import ANIM, COLORS

        if len(sys.argv) == 2:
            config = MazeConfig.from_config_file("config.txt")

            # config = MazeConfig(width=50, height=50, entry=(0,0),
            #                     exit=(18,12), output_file="maze.txt",
            #                     perfect=False)
        else:
            raise ArgumentsError("ERROR: Use 'make run' or check if "
                                 "'config.txt' file exist.")

        generator = MazeGenerator(config)

        generator.maze_generator(rendering=True)

        # print(generator.get_maze_parameters())

        choice2 = True

        while True:
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            if choice2:
                print("2. Show path from entry to exit")
            else:
                print("2. Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Show seed")
            print("5. Quit")

            while True:
                user_choice = input("Choice? (1-5): ")
                try:
                    choice = int(user_choice)
                    if 1 <= choice <= 5:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print(f"{COLORS.red}Error!{COLORS.reset}", end="",
                          flush=True)
                    time.sleep(0.5)
                    print(Cursor.UP(1) + "\r" + ANIM.clear, end="")

            if choice == 1:
                generator.maze_generator(rendering=True, regen=True)
                choice2 = True

            elif choice == 2:
                print(ANIM.clear_screen, end="")
                if choice2:
                    solver = MazeSolver(generator)
                    solver.find_path()
                    generator.y_offset = 0
                    generator.print_maze()
                    solver.print_path()
                    choice2 = False
                else:
                    generator.y_offset = 0
                    generator.print_maze()
                    choice2 = True
                print(Cursor.POS(1, generator.height + 1))

            elif choice == 3:
                generator._apply_wall_color(random.randint(1, 9), True)
                print(ANIM.clear_screen)
                if choice2:
                    generator.print_maze()
                else:
                    solver.print_maze_solver()

            elif choice == 4:
                while True:
                    print("Seed: ", end="")
                    print(Cursor.UP(6) + "\r" + ANIM.clear, end="", flush=True)
                    print(f"{generator.seed}", end="", flush=True)
                    print("")
                    k = input("Press anything to show the menu: ")
                    if k is not None:
                        print(Cursor.UP(4) + "\r" + ANIM.clear, end="")
                        break

            elif choice == 5:
                print("\n\nGoodbye and so long!")
                break

    except (MazeConfigError, MazeGenerationError, FileNotFoundError,
            ValueError) as e:

        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 2

    # except Exception as e:
    #     print(f"Unexpected error of type - {type(e).__name__}: {e}",
    #           file=sys.stderr)
    #     return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
