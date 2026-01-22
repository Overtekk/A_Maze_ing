# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  generator.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/22 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/01/22 17:00:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import string

from typing import Any, Dict, Optional, Set, Tuple
from colorama import Fore, Style

from ..utils.config import Config


def get_42_pattern(width: int, height: int) -> Set[Tuple[int, int]]:
    center_x = width // 2
    center_y = height // 2

    pattern = {
        (center_x - 3, center_y), (center_x - 3, center_y - 1),
        (center_x - 3, center_y - 2), (center_x - 1, center_y),
        (center_x - 2, center_y), (center_x - 1, center_y + 1),
        (center_x - 1, center_y + 2), (center_x + 3, center_y + 2),
        (center_x + 2, center_y + 2), (center_x + 1, center_y + 2),
        (center_x + 1, center_y), (center_x + 1, center_y + 1),
        (center_x + 2, center_y), (center_x + 3, center_y),
        (center_x + 3, center_y - 1), (center_x + 3, center_y - 2),
        (center_x + 2, center_y - 2), (center_x + 1, center_y - 2)
    }
    return pattern


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
            self.generate_random_seed()

        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord

        self.entry_x = entry_x
        self.entry_y = entry_y
        self.exit_x = exit_x
        self.exit_y = exit_y

        self.maze: Dict[Tuple[int, int], str] = {}
        self.empty = ' '
        self.border = f'{Fore.WHITE}\u2588\u2588'
        self.wall = f'{Fore.GREEN}\u2588\u2588'
        self.entry = f'{Fore.MAGENTA}\u2588\u2588'
        self.exit = f'{Fore.RED}\u2588\u2588'
        self.fourty_two = f'{Fore.LIGHTWHITE_EX}\u2588\u2588'

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

    def generate_random_seed(self) -> None:
        random_n = random.randint(0, 50)
        if random_n == 25:
            str = 'roandrie'
        elif random_n == 35:
            str = 'rruiz'
        else:
            str = ''
        length = random.randint(1, 1000)
        random_seed = ''.join(random.choices(string.ascii_letters +
                                             string.digits, k=length))
        random_seed += str
        self.seed = random_seed

    def generated_maze(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.maze[(x, y)] = self.wall

                if self.entry_x == x and self.entry_y == y:
                    self.maze[(x, y)] = self.entry
                if self.exit_x == x and self.exit_y == y:
                    self.maze[(x, y)] = self.exit

    def print_maze(self) -> None:

        print(self.border * (self.width + 2))
        for y in range(self.height):
            print(self.border, end='')
            for x in range(self.width):
                print(self.maze[(x, y)], end='')
            print(self.border)
        print(self.border * (self.width + 2))
        print(Style.RESET_ALL)

    def print_42(self) -> None:
        pattern_coords = get_42_pattern(self.width, self.height)

        for coord in pattern_coords:
            if coord in self.maze:
                self.maze[coord] = self.fourty_two
