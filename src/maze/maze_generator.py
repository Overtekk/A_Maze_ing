# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_generator.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/22 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/01/27 16:27:47 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import string
import time

from typing import Any, Dict, Tuple
from colorama import Fore, Style, Cursor

from .maze_config import MazeConfig
from .maze_fortytwo_pattern import get_fortytwo_pattern as ft_patt
from .algorithms import recursive_backtracking


class MazeGenerator():

    # Texte colors
    txt_white = f"{Fore.WHITE} {Style.BRIGHT}"

    # Clear screen
    CLEAR = "\033[J"
    CLEAR_All = "\033[2J\033[H"

    # Walls colors
    wall_white = Fore.WHITE
    wall_blue = Fore.BLUE
    wall_yellow = Fore.LIGHTYELLOW_EX
    wall_magenta = Fore.LIGHTMAGENTA_EX
    wall_cyan = Fore.CYAN
    wall_green = Fore.LIGHTGREEN_EX

    def __init__(self, config: MazeConfig) -> None:
        self.cfg = config

        # Maze parameters
        self.width = config.width
        self.height = config.height
        self.entry_coord = config.entry
        self.exit_coord = config.exit
        self.output_file = config.output_file
        self.perfect = config.perfect
        self.seed = config.seed
        self.display = config.display
        self.algorithm = config.algorithm
        # Generate seed if user didn't give it.

        if self.seed is None:
            self._generate_random_seed()

        # Unpacking coords.
        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord
        self.entry_x, self.entry_y = entry_x, entry_y
        self.exit_x, self.exit_y = exit_x, exit_y
        self.fourtytwo_coord = ft_patt(self.width, self.height)

        self.maze: Dict[Tuple[int, int], str] = {}
        # Default color
        self.wall_color = self.wall_white

        # Maze structure
        self.wall_ASCII = "\u2588\u2588"

        self.empty = ' '
        self.border = f'{self.wall_color}{self.wall_ASCII}'
        self.wall = f'{self.wall_color}{self.wall_ASCII}'
        self.entry = f'{Fore.MAGENTA}{self.wall_ASCII}'
        self.exit = f'{Fore.RED}{self.wall_ASCII}'
        self.fourtytwo_block = f'{Fore.LIGHTWHITE_EX}{self.wall_ASCII}'

    def maze_generator(self, rendering: bool = False) -> None:
        if rendering:
            if self.display == "ascii":
                print(self.CLEAR_All, end="")
                while True:
                    user_choice = self._customize_maze_walls_color()
                    if user_choice == "ok":
                        break
            if self.display == "emoji":
                self._update_graphics()

        loading = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        text_generating = " Generating Maze..."
        text_generated = "-Maze Generated-"
        text_algo_display = f"Mode: {self.algorithm}"
        if rendering:
            text_algo_display += f" | Display: {self.display}"

        # Align cursor based of texts writted
        self.y_offset = 3

        if rendering:
            print(self.CLEAR_All, end="")

        # Calcule the center of the maze to align text
        visual_width = (self.width * 2) // 2
        filling = " " * max(0, ((visual_width - len(text_generating) // 2)))

        # Print the loading text
        for _ in range(2):
            for char in loading:
                print(f"\r{filling}{self.txt_white}{char}{text_generating}",
                      end="", flush=True)
                time.sleep(0.1)

        filling = " " * max(0, ((visual_width - len(text_generated) // 2)))
        print(f"\r{filling}  {text_generated}    ")

        filling = " " * max(0, ((visual_width - len(text_algo_display) // 2)))
        print(f"\r{filling}{text_algo_display}{Style.RESET_ALL}")

        random.seed(self.seed)
        self._construct_base_maze()

        if rendering:
            self._print_maze()

        if self.algorithm == "rb":
                recursive_backtracking(self, rendering)

        if rendering:
            print(Cursor.POS(1, self.height + 3 + self.y_offset))

    def get_maze_parameters(self) -> Dict[str, Any]:
        return {
            'Width': self.width,
            'Height': self.height,
            'Entry Coordinates': self.entry_coord,
            'Exit Coordinates': self.exit_coord,
            'Output file': self.output_file,
            'Perfect Maze?': self.perfect,
            'Seed': self.seed,
            'Display mode': self.display,
            'Algorithm': self.algorithm
        }

    def break_wall(self, x: int, y: int, rendering: bool) -> None:
        if (x, y) not in self.fourtytwo_coord:
            self.maze[(x, y)] = self.empty

            if rendering:
                curs_x = (x * 2) + 3
                curs_y = y + 2 + self.y_offset
                print(Cursor.POS(curs_x, curs_y) + self.empty, end="", flush=True)
                time.sleep(0.001)

    def _print_maze(self) -> None:
        total_cases = self.width * self.height
        if total_cases < 600:
            animate_char_by_char = True
        else:
            animate_char_by_char = False

        if animate_char_by_char:
            delay = 1.5 / total_cases
        else:
            delay = 1.0 / self.height

        print(self.border * (self.width + 2), flush=True)

        for y in range(self.height):
            print(self.border, end='', flush=True)

            if animate_char_by_char:
                for x in range(self.width):
                    print(self.maze[(x, y)], end="", flush=True)
                    time.sleep(delay)
            else:
                raw_line = "".join([self.maze[(x, y)] for x in
                                    range(self.width)])
                print(raw_line, end='', flush=True)
                time.sleep(delay)

            print(self.border, flush=True)

        print(self.border * (self.width + 2), flush=True)
        print(Style.RESET_ALL)

    def _apply_wall_color(self, choice: int) -> None:
        colors = {
            1: self.wall_white,
            2: self.wall_magenta,
            3: self.wall_blue,
            4: self.wall_cyan,
            5: self.wall_yellow,
            6: self.wall_green
        }
        self.wall_color = colors.get(choice, self.wall_white)

        # self.border = f'{self.wall_color}{self.wall_ASCII}'
        self.wall = f'{self.wall_color}{self.wall_ASCII}'

    def _construct_base_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.maze[(x, y)] = self.wall

                if self.entry_x == x and self.entry_y == y:
                    self.maze[(x, y)] = self.entry

                if self.exit_x == x and self.exit_y == y:
                    self.maze[(x, y)] = self.exit

                if (x, y) in self.fourtytwo_coord:
                    self.maze[(x, y)] = self.fourtytwo_block

    def _generate_random_seed(self) -> None:
        random_seed = ''.join(random.choices(string.ascii_letters +
                                             string.digits,
                                             k=random.randint(1, 101)))
        self.seed = random_seed

    def _customize_maze_walls_color(self) -> str:
        print(f"{self.txt_white}Choose walls color:")
        print(f"1. {Fore.WHITE}White\t {Fore.BLUE}3. Blue\t "
              f"{Fore.LIGHTYELLOW_EX}5. Yellow")
        print(f"2. {Fore.MAGENTA}Magenta\t {Fore.CYAN}4. Cyan\t "
              f"{Fore.LIGHTGREEN_EX}6. Green")

        user_choice = input(f"{self.txt_white}Enter choice: ")
        try:
            choice = int(user_choice)

            if choice >= 1 and choice <= 6:
                print(Cursor.UP(4) + self.CLEAR, end="")
                self._apply_wall_color(choice)
                return "ok"
            else:
                raise ValueError

        except ValueError:
            print(f"{Fore.RED}Invalid choice. Choose between 1 and 6.", end="",
                  flush=True)
            time.sleep(1)
            print(Cursor.UP(5) + "\r" + self.CLEAR, end="")

        return "no"

    def _update_graphics(self):
        if self.display == "emoji":
            self.wall_ASCII = "🔲"
            self.wall = "🔲"
            self.border = "🔲"
            self.entry = "🛑"
            self.exit = "🟦"
            self.fourtytwo_block = "🟧"
            self.wall_color = ""

        else:
            self.border = f'{self.wall_color}{self.wall_ASCII}'
            self.wall = f'{self.wall_color}{self.wall_ASCII}'
            self.entry = f'{Fore.MAGENTA}{self.wall_ASCII}'
            self.exit = f'{Fore.RED}{self.wall_ASCII}'
            self.fourtytwo_block = f'{Fore.LIGHTWHITE_EX}{self.wall_ASCII}'
