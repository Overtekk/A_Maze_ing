# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  hunt_and_kill.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/31 10:55:56 by rruiz           #+#    #+#               #
#  Updated: 2026/01/31 15:15:24 by rruiz           ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from random import randint

from typing import Any

from src.maze.maze_customization import MAZE

def hunt_and_kill(generator: Any, rendering: bool) -> None:
    visited_cases = []
    current_x = randint(0, generator.width + 1)
    current_y = randint(0, generator.height + 1)
    current_coord = (current_x, current_y)