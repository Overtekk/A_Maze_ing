# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_generator.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/22 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/01/26 12:06:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import string
import time

from typing import Any, Dict, Optional, Set, Tuple
from colorama import Fore, Style, Cursor


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

    # Walls ASCII
    wall_ASCII = "\u2588\u2588"

    def __init__(self, width: int, height: int, entry: Tuple[int, int],
                 exit: Tuple[int, int], output_file: str, perfect: bool,
                 seed: Optional[str | int] = None) -> None:
        # Check arguments first
        self._check_arg(width, 'width')
        self._check_arg(height, 'height')
        self._check_arg(entry, 'entry')
        self._check_arg(exit, 'exit')
        self._check_arg(output_file, 'output_file')
        self._check_arg(perfect, 'perfect')

        # Maze parameters
        self.width = width
        self.height = height
        self.entry_coord = entry
        self.exit_coord = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        # Generate seed if user didn't give it.
        if self.seed is None:
            self._generate_random_seed()

        # Unpacking coords.
        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord
        self.entry_x, self.entry_y = entry_x, entry_y
        self.exit_x, self.exit_y = exit_x, exit_y
        self.fourtytwo_coord = self._get_42_pattern(self.width, self.height)

        self.maze: Dict[Tuple[int, int], str] = {}
        # Default color
        self.wall_color = self.wall_white

        # Maze structure
        self.empty = ' '
        self.border = f'{self.wall_color}{self.wall_ASCII}'
        self.wall = f'{self.wall_color}{self.wall_ASCII}'
        self.entry = f'{Fore.MAGENTA}{self.wall_ASCII}'
        self.exit = f'{Fore.RED}{self.wall_ASCII}'
        self.fourtytwo_block = f'{Fore.LIGHTWHITE_EX}{self.wall_ASCII}'

        # Check is parameters are valid
        self._validate_parameters()

    def maze_generator(self, rendering: bool = False) -> None:
        if rendering:
            print(self.CLEAR_All, end="")
            while True:
                user_choice = self._customize_maze_walls_color()
                if user_choice == "ok":
                    break

        loading = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        text_generating = " Generating Maze..."
        text_generated = "-Maze Generated-"

        if rendering:
            print(self.CLEAR_All, end="")

        visual_width = (self.width * 2) // 2
        filling = " " * max(0, ((visual_width - len(text_generating) // 2)))

        for _ in range(2):
            for char in loading:
                print(f"\r{filling}{self.txt_white}{char}{text_generating}",
                      end="", flush=True)
                time.sleep(0.1)

        filling = " " * max(0, ((visual_width - len(text_generated) // 2)))
        print(f"\r{filling}  {text_generated}    {Style.RESET_ALL}")

        random.seed(self.seed)
        self._construct_base_maze()
        self._print_42()
        if rendering:
            self._print_maze()
        if self.perfect:
            self._generate_perfect_maze()
        else:
            self._generate_maze(rendering)
        if rendering:
            print(Cursor.POS(1, self.height + 3 + 2))

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

    def _generate_maze(self, rendering: bool) -> None:
        visited_cells = [(self.exit_x, self.exit_y)]
        def visit(x: int, y: int):
            walls_list = {}
            if 0 <= x - 1 < self.width:
                if self.maze[(x - 1, y)] is self.wall:
                    walls_list.update({"west": x - 1})

            if x + 1 < self.width:
                if self.maze[(x + 1, y)] is self.wall:
                    walls_list.update({"east": x + 1})

            if 0 <= y - 1 < self.height:
                if self.maze[(x, y - 1)] is self.wall:
                    walls_list.update({"south" : y - 1})

            if y + 1 < self.width:
                if self.maze[(x, y + 1)] is self.wall:
                    walls_list.update({"north": y + 1})

            if len(walls_list) > 0:
                direction = random.choice(list(walls_list))

                if direction == "north" or direction == "south":
                    self._break_wall(x, walls_list[direction], rendering)
                    visited_cells.append([x, walls_list[direction]])
                    visit(x, walls_list[direction])
                else:
                    self._break_wall(walls_list[direction], y, rendering)
                    visited_cells.append([walls_list[direction], y])
                    visit(walls_list[direction], y)
        visit(self.exit_x, self.exit_y)

    def _break_wall(self, x: int, y: int, rendering: bool) -> None:
        self.maze[(x, y)] = self.empty

        if rendering:
            curs_x = (x * 2) + 3
            curs_y = y + 2 + 2
            print(Cursor.POS(curs_x, curs_y) + self.empty, end="", flush=True)
            time.sleep(0.05)

    def _generate_perfect_maze(self) -> None:
        pass

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

    def _check_arg(self, value: Any, name: str) -> None:
        rules: Dict[str, Any] = {
                'width': int,
                'height': int,
                'entry': tuple,
                'exit': tuple,
                'output_file': str,
                'perfect': bool,
                'seed': (str, int, type(None))
            }
        if name in rules:
            required_type = rules[name]
            if not isinstance(value, required_type):
                raise ValueError(f"'{name}' has wrong type. Expected "
                                 f"{required_type}")

    def _validate_parameters(self) -> None:
        if not (0 <= self.entry_x < self.width and 0 <= self.entry_y <
                self.height):
            raise ValueError("Entry cannot be outside walls.")
        if not (0 <= self.exit_x < self.width and 0 <= self.exit_y <
                self.height):
            raise ValueError("Exit cannot be outside walls.")

        if self.entry_coord == self.exit_coord:
            raise ValueError("Entry and Exit cannot be at the exact same "
                             "position.")

        if self.width < 7 or self.height < 5:
            raise ValueError("Dimensions too small for the '42' pattern.")

        if self.entry_coord in self.fourtytwo_coord:
            raise ValueError("Can't place Entry here. Reserved to '42'")
        if self.exit_coord in self.fourtytwo_coord:
            raise ValueError("Can't place Exit here. Reserved to '42'")

    def _generate_random_seed(self) -> None:
        random_n = random.randint(0, 50)
        if random_n == 25:
            suffix = 'roandrie'
        elif random_n == 35:
            suffix = 'rruiz'
        else:
            suffix = ''
        length = random.randint(1, 101)
        random_seed = ''.join(random.choices(string.ascii_letters +
                                             string.digits, k=length))
        random_seed += suffix
        self.seed = random_seed

    @staticmethod
    def _get_42_pattern(width: int, height: int) -> Set[Tuple[int, int]]:
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

    def _print_42(self) -> None:
        for coord in self.fourtytwo_coord:
            if coord in self.maze:
                self.maze[coord] = self.fourtytwo_block

    def _construct_base_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.maze[(x, y)] = self.wall

                if self.entry_x == x and self.entry_y == y:
                    self.maze[(x, y)] = self.entry
                if self.exit_x == x and self.exit_y == y:
                    self.maze[(x, y)] = self.exit
