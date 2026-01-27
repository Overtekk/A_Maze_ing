# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  backtracking.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/27 16:16:22 by roandrie        #+#    #+#               #
#  Updated: 2026/01/27 16:28:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import sys

from typing import Any


def recursive_backtracking(generator: Any, rendering: bool) -> None:
    sys.setrecursionlimit(100000)

    def visit(x: int, y: int):
        walls_list = {}
        walls_random = []
        if 0 <= x - 2 < generator.width:
            if (generator.maze[(x - 2, y)] == generator.wall and
                generator.maze[(x - 1, y)] == generator.wall and
                (x - 2, y) not in generator.fourtytwo_coord and
                (x - 1, y) not in generator.fourtytwo_coord):
                walls_list.update({"west": x - 2})

        if x + 2 < generator.width:
            if (generator.maze[(x + 2, y)] == generator.wall and
                generator.maze[(x + 1, y)] == generator.wall and
                (x + 2, y) not in generator.fourtytwo_coord and
                (x + 1, y) not in generator.fourtytwo_coord):
                walls_list.update({"east": x + 2})

        if 0 <= y - 2 < generator.height:
            if (generator.maze[(x, y - 2)] == generator.wall and
                generator.maze[(x, y - 1)] == generator.wall and
                (x, y - 2) not in generator.fourtytwo_coord and
                (x, y - 1) not in generator.fourtytwo_coord):
                walls_list.update({"south" : y - 2})

        if y + 2 < generator.height:
            if (generator.maze[(x, y + 2)] == generator.wall and
                generator.maze[(x, y + 1)] == generator.wall and
                (x, y + 2) not in generator.fourtytwo_coord and
                (x, y + 1) not in generator.fourtytwo_coord):
                walls_list.update({"north": y + 2})

        if len(walls_list) > 0:
            walls_random = list(walls_list)
            random.shuffle(walls_random)

            for item in walls_random:
                if item == "north" or item == "south":
                    if generator.maze[x, (walls_list[item])] == generator.wall:
                        generator.break_wall(x, walls_list[item], rendering)
                        mid_y = (y + walls_list[item]) // 2
                        generator.break_wall(x, mid_y, rendering)
                        visit(x, walls_list[item])
                else:
                    if generator.maze[walls_list[item], y] == generator.wall:
                        generator.break_wall(walls_list[item], y, rendering)
                        mid_x = (x + walls_list[item]) // 2
                        generator.break_wall(mid_x, y, rendering)
                        visit(walls_list[item], y)

    visit(generator.exit_x, generator.exit_y)
