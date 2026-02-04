# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/20 16:25:20 by roandrie        #+#    #+#               #
#  Updated: 2026/02/03 16:20:20 by roandrie        ###   ########.fr        #
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
        from src.maze.maze_customization import ANIM, COLORS, STYLE

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

        show_menu = True
        choice2 = True
        while True and show_menu:
            print(f"\n{COLORS.magenta}=== {STYLE.bright}{COLORS.red}A-"
                  f"{COLORS.blue}Maze-{COLORS.green}ing {COLORS.reset}"
                  f"{COLORS.magenta}==={COLORS.reset}")
            print(f"{STYLE.bright}{COLORS.lightcyan}1. Re-generate a new maze"
                  f"{COLORS.reset}")

            if choice2:
                print(f"{STYLE.bright}{COLORS.lightcyan}2. Show path from "
                      f"entry to exit{COLORS.reset}")
            else:
                print(f"{STYLE.bright}{COLORS.lightcyan}2. Hide path from "
                      f"entry to exit{COLORS.reset}")
            print(f"{STYLE.bright}{COLORS.lightcyan}3. Rotate maze colors"
                  f"{COLORS.reset}")
            print(f"{STYLE.bright}{COLORS.lightcyan}4. Change algorithm"
                  f"{COLORS.reset}")
            print(f"{STYLE.bright}{COLORS.lightcyan}5. Show seed"
                  f"{COLORS.reset}")
            print(f"{STYLE.bright}{COLORS.lightcyan}6. Quit{COLORS.reset}")

            while True:
                user_choice = input(f"{COLORS.lightgreen}Choice?"
                                    f" (1-6): {COLORS.reset}")
                try:
                    choice = int(user_choice)
                    if 1 <= choice <= 6:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print(f"{COLORS.red}❌ Error!{COLORS.reset}", end="",
                          flush=True)
                    time.sleep(0.6)
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
                    print(Cursor.UP(7) + "\r" + ANIM.clear, end="", flush=True)
                    print(f"{STYLE.bright}{COLORS.lightcyan}Choose one "
                          f"algorithm: ")
                    print(f"{STYLE.bright}{COLORS.lightcyan}1. Recursive "
                          f"Backtracking | 2. Hunt and Kill")

                    while True:
                        algo_choose = input(f"{COLORS.lightgreen}Choice? (1-2)"
                                            f": {COLORS.reset}")
                        try:
                            algo_choosen = int(algo_choose)
                            if 1 <= algo_choosen <= 2:
                                generator._apply_algo_change(algo_choosen)
                                break
                            else:
                                raise ValueError
                        except ValueError:
                                print(f"{COLORS.red}❌ Error!{COLORS.reset}",
                                      end="", flush=True)
                                time.sleep(0.5)

                    print(f"{STYLE.bright}{COLORS.green}✅ Algorithm "
                          "successfuly changed!")
                    time.sleep(0.7)
                    print(Cursor.UP(6) + "\r" + ANIM.clear, end="")
                    break

            elif choice == 5:
                while True:
                    print(Cursor.UP(7) + "\r" + ANIM.clear, end="", flush=True)
                    print(f"{STYLE.bright}{COLORS.lightcyan}Seed: "
                          f"{COLORS.reset}", end="")
                    print(f"{STYLE.dim}{generator.seed}", end="", flush=True)
                    print(f"{COLORS.reset}")

                    k = input(f"{COLORS.lightgreen}Press anything to show "
                              f"the menu: {COLORS.reset}")
                    if k is not None:
                        print(Cursor.UP(4) + "\r" + ANIM.clear, end="")
                        break

            elif choice == 6:
                print(f"\n\n{STYLE.bright}{COLORS.lightred}Goodbye 👋 and "
                      f"so long! {COLORS.reset}")
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
