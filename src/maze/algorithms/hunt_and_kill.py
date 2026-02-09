# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  hunt_and_kill.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/31 10:55:56 by rruiz           #+#    #+#               #
#  Updated: 2026/02/09 09:31:55 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Hunt-and-kill maze generation algorithm implementation.

This module provides a function to generate mazes using the Hunt-and-Kill
algorithm. This method alternates between two phases:
1.  Kill (Random Walk): Carves a random path until it hits a dead end
    or an existing path.
2.  Hunt (Scan): Scans the grid for an unvisited cell adjacent to
    a visited one, connects it, and restarts the Kill phase from there.

This implementation also handles the "imperfect" maze logic (creating loops)
directly within the scanning phase if configured.
"""

from random import choice, randrange

from typing import Any

from maze.maze_customization import MAZE


def hunt_and_kill(generator: Any, rendering: bool) -> None:
    """Executes the Hunt-and-Kill algorithm on the provided generator.

    The function modifies the `generator.maze` grid in-place. It respects
    the reserved '42' pattern coordinates by checking
    `generator.fourtytwo_coord` before carving walls.

    Args:
        generator: The `MazeGenerator` instance containing the grid state,
                  dimensions, and configuration (perfect/imperfect).
        rendering: If True, calls `generator.break_wall` with visualization
                   enabled to animate the process in the terminal.
    """
    targets = (MAZE.wall, MAZE.entry, MAZE.exit)
    while True:
        x = randrange(1, generator.width, 2)
        y = randrange(1, generator.height, 2)
        if (x, y) not in generator.fourtytwo_coord:
            break
    generator.break_wall(x, y, rendering)
    while True:
        # Kill phase #
        while True:
            directions = []
            if y - 2 > 0:
                directions.append("N")
            if x < generator.width - 2:
                directions.append("E")
            if y < generator.height - 2:
                directions.append("S")
            if x - 2 > 0:
                directions.append("W")
            neighbors = {}
            if "N" in directions and generator.maze[(x, y - 2)] in targets:
                if ((x, y - 2) not in generator.fourtytwo_coord
                        and (x, y - 1) not in generator.fourtytwo_coord):
                    neighbors["N"] = (x, y - 2)
            if "E" in directions and generator.maze[(x + 2, y)] in targets:
                if ((x + 2, y) not in generator.fourtytwo_coord
                        and (x + 1, y) not in generator.fourtytwo_coord):
                    neighbors["E"] = (x + 2, y)
            if "S" in directions and generator.maze[(x, y + 2)] in targets:
                if ((x, y + 2) not in generator.fourtytwo_coord
                        and (x, y + 1) not in generator.fourtytwo_coord):
                    neighbors["S"] = (x, y + 2)
            if "W" in directions and generator.maze[(x - 2, y)] in targets:
                if ((x - 2, y) not in generator.fourtytwo_coord
                        and (x - 1, y) not in generator.fourtytwo_coord):
                    neighbors["W"] = (x - 2, y)
            if len(neighbors) == 0:
                break
            dir = choice(list(neighbors.keys()))
            target_x, target_y = neighbors[dir]
            mid_x = (x + target_x) // 2
            mid_y = (y + target_y) // 2
            generator.break_wall(mid_x, mid_y, rendering)
            generator.break_wall(target_x, target_y, rendering)
            x, y = target_x, target_y
        # Hunt phase #
        found = False
        for ty in range(1, generator.height - 1, 2):
            for tx in range(1, generator.width - 1, 2):
                if (generator.maze[(tx, ty)] in targets
                        and (tx, ty) not in generator.fourtytwo_coord):
                    potential_neighbors = []
                    if (generator.maze.get((tx, ty - 2)) == MAZE.empty
                            and generator.maze.get((tx, ty - 2)) is not None
                            and (tx, ty - 1) not in generator.fourtytwo_coord):
                        potential_neighbors.append((tx, ty - 1))
                    if (generator.maze.get((tx + 2, ty)) == MAZE.empty
                            and generator.maze.get((tx + 2, ty)) is not None
                            and (tx + 1, ty) not in generator.fourtytwo_coord):
                        potential_neighbors.append((tx + 1, ty))
                    if (generator.maze.get((tx, ty + 2)) == MAZE.empty
                            and generator.maze.get((tx, ty + 2)) is not None
                            and (tx, ty + 1) not in generator.fourtytwo_coord):
                        potential_neighbors.append((tx, ty + 1))
                    if (generator.maze.get((tx - 2, ty)) == MAZE.empty
                            and generator.maze.get((tx - 2, ty)) is not None
                            and (tx - 1, ty) not in generator.fourtytwo_coord):
                        potential_neighbors.append((tx - 1, ty))

                    if potential_neighbors:
                        mid_x, mid_y = choice(potential_neighbors)
                        generator.break_wall(mid_x, mid_y, rendering)
                        generator.break_wall(tx, ty, rendering)

                        if (not generator.perfect
                                and len(potential_neighbors) > 1):
                            if randrange(100) < 66:
                                potential_neighbors.remove((mid_x, mid_y))
                                extra_mid_x, extra_mid_y = (
                                                choice(potential_neighbors))
                                generator.break_wall(extra_mid_x, extra_mid_y,
                                                     rendering)

                        x, y = tx, ty
                        found = True
                        break
            if found:
                break
        if not found:
            break
