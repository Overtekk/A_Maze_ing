# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  backtracking.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/27 16:16:22 by roandrie        #+#    #+#               #
#  Updated: 2026/01/31 13:11:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import sys

from typing import Any

from ..maze_customization import MAZE


def recursive_backtracking(generator: Any, rendering: bool) -> None:
    sys.setrecursionlimit(100000)

    def visit(x: int, y: int):
        walls_list = {}
        walls_random = []
        if 0 <= x - 2 < generator.width:
            if (generator.maze[(x - 2, y)] == MAZE.wall and
                generator.maze[(x - 1, y)] == MAZE.wall):
                walls_list.update({"west": x - 2})

        if x + 2 < generator.width:
            if (generator.maze[(x + 2, y)] == MAZE.wall and
                generator.maze[(x + 1, y)] == MAZE.wall):
                walls_list.update({"east": x + 2})

        if 0 <= y - 2 < generator.height:
            if (generator.maze[(x, y - 2)] == MAZE.wall and
                generator.maze[(x, y - 1)] == MAZE.wall):
                walls_list.update({"south" : y - 2})

        if y + 2 < generator.height:
            if (generator.maze[(x, y + 2)] == MAZE.wall and
                generator.maze[(x, y + 1)] == MAZE.wall):
                walls_list.update({"north": y + 2})

        if len(walls_list) > 0:
            walls_random = list(walls_list)
            random.shuffle(walls_random)

            for item in walls_random:
                target_x, target_y = x, y
                mid_x, mid_y = x, y

                if item == "north":
                    target_y = walls_list[item]
                    mid_y = (y + target_y) // 2
                elif item == "south":
                    target_y = walls_list[item]
                    mid_y = (y + target_y) // 2
                elif item == "east":
                    target_x = walls_list[item]
                    mid_x = (x + target_x) // 2
                elif item == "west":
                    target_x = walls_list[item]
                    mid_x = (x + target_x) // 2

                if generator.maze[(target_x, target_y)] == MAZE.wall:
                    generator.break_wall(target_x, target_y, rendering)
                    generator.break_wall(mid_x, mid_y, rendering)

                    visit(target_x, target_y)

    visit(generator.exit_x, generator.exit_y)
