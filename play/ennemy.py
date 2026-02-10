# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ennemy.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/02/10 08:25:43 by roandrie        #+#    #+#               #
#  Updated: 2026/02/10 08:29:22 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from maze.maze_generator import MazeGenerator
from maze.maze_customization import MAZE, DISPLAY_MODE

class Enemy():

    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze

        if maze.display == DISPLAY_MODE.emoji:
            pass

    def spawn(self):
        pass
