# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/27 15:52:41 by roandrie        #+#    #+#               #
#  Updated: 2026/02/03 08:27:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
Maze Generator Package.
"""

from .maze_config import MazeConfig
from .maze_errors import MazeConfigError, MazeGenerationError
from .maze_fortytwo_pattern import get_fortytwo_pattern
from .maze_generator import MazeGenerator
from .maze_solver import MazeSolver

__version__ = "1.0.0"

__all__ = [
    "MazeConfig",
    "MazeConfigError",
    "MazeGenerationError",
    "get_fortytwo_pattern",
    "MazeGenerator",
    "MazeSolver"
]
