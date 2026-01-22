# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  generator.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/22 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/01/22 15:19:18 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Dict, Optional, Tuple
from colorama import Fore, Style

from ..utils.config import Config


class MazeGenerator():

    def __init__(self, width: int, height: int, entry_coord: Tuple[int, int],
                 exit_coord: Tuple[int, int], output_file: str, perfect: bool,
                 seed: Optional[str | int] = None) -> None:
        self.width = width
        self.height = height
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        if self.seed is None:
            pass

        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord

        self.entry_x = entry_x
        self.entry_y = entry_y
        self.exit_x = exit_x
        self.exit_y = exit_y

        self.maze = {}
        self.empty = ' '
        self.border = f'{Fore.WHITE}\u2588\u2588'
        self.wall = f'{Fore.WHITE}\u2588\u2588'
        self.entry = f'{Fore.MAGENTA}\u2588\u2588'
        self.exit = f'{Fore.RED}\u2588\u2588'

    @classmethod
    def import_config(cls, config: Config) -> 'MazeGenerator':
        return cls(
            width=config.width,
            height=config.height,
            entry_coord=config.entry,
            exit_coord=config.exit,
            output_file=config.output_file,
            perfect=config.perfect,
            seed=config.seed
        )

    def get_maze_parameters(self) -> Dict[str, Any]:
        return {
            'Width': self.width,
            'Height': self.height,
            'Entry Coordinates': self.entry_coord,
            'Exit Coordinates': self.exit_coord,
            'Output file': self.output_file,
            'Perfect Maze?': self.perfect,
            'Seed': self.seed
        }

    def generated_maze(self):
        for x in range(self.width):
            for y in range(self.height):
                self.maze[(x, y)] = self.wall

                if self.entry_x == x and self.entry_y == y:
                    self.maze[(x, y)] = self.entry
                if self.exit_x == x and self.exit_y == y:
                    self.maze[(x, y)] = self.exit

    def print_maze(self):

        print(self.border * (self.width + 2))
        for y in range(self.height):
            print(self.border, end='')
            for x in range(self.width):
                print(self.maze[(x, y)], end='')
            print(self.border)
        print(self.border * (self.width + 2))
        print(Style.RESET_ALL)
