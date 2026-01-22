# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/20 16:25:20 by roandrie        #+#    #+#               #
#  Updated: 2026/01/22 10:39:58 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Main script for the Maze Generator.

Call all the module to check and create everything. Then, construct the maze,
output it and launch the 'game'.
"""

import sys

from src.utils.config import check_arg, IllegalArgumentError


def main() -> None:
    """"Programm main entry point."""
    try:
        config = check_arg()
        print(config)
        if config is None:
            sys.exit(2)
    except (IllegalArgumentError, FileNotFoundError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error of type - {type(e).__name__}: {e}",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
