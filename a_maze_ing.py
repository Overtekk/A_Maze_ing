# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/20 16:25:20 by roandrie        #+#    #+#               #
#  Updated: 2026/01/27 16:24:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Main script for the Maze Generator.

First, we check if all dependencies are installed. If no error have been found,
we can import everything and start to check the config file.
Then, construct the maze, output it and launch the 'game'.
"""

import sys

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

        from src.maze import MazeConfig, MazeConfigError, MazeGenerator

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

    except (MazeConfigError, FileNotFoundError, ValueError) as e:

        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        return 2

    # except Exception as e:
    #     print(f"Unexpected error of type - {type(e).__name__}: {e}",
    #           file=sys.stderr)
    #     return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
