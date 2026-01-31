# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_generator.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/22 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/01/31 12:52:48 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import string
import time

from typing import Any, Dict, Tuple
from colorama import Cursor

from .maze_config import MazeConfig
from .maze_fortytwo_pattern import get_fortytwo_pattern as ft_patt
from .maze_customization import (COLORS, STYLE, ANIM, DISPLAY_MODE, ALGO_MODE,
                                 MAZE, VISUAL)
from .algorithms import recursive_backtracking


class MazeGenerator():

    txt_white = f"{COLORS.white}{STYLE.bright}"

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

        self.color_wall = COLORS.white
        self.color_ft = COLORS.yellow
        self.color_entry = COLORS.magenta
        self.color_exit = COLORS.red

        if self.display == DISPLAY_MODE.ascii:
            self.visual_empty = VISUAL.empty_block
            self.visual_wall = VISUAL.block
            self.step_x = 2
        else:
            self.visual_empty = VISUAL.empty
            self.visual_wall = "#"
            self.step_x = 1

    def maze_generator(self, rendering: bool = False) -> None:
        if rendering:
            if self.display == DISPLAY_MODE.ascii:
                print(ANIM.clear, end="")
                while True:
                    user_choice = self._customize_maze_walls_color()
                    if user_choice == "ok":
                        break

        loading = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        text_generating = " Generating Maze..."
        text_generated = "-Maze Generated-"
        text_algo_display = f"Mode: {self.algorithm}"
        if rendering:
            text_algo_display += f" | Display: {self.display}"

        # Align cursor based of lines of texts writted
        self.y_offset = 3

        # Clear screen to render the maze if rendering is True
        if rendering:
            print(ANIM.clear_screen, end="")

        # Calculate based on the width to center the text
        if rendering:
            if self.display == DISPLAY_MODE.ascii:
                visual_width = self.width
            else:
                visual_width = self.width // 2
            filling = " " * max(0, ((visual_width - (len(text_generating) // 2))))

        # Print the loading text
        for _ in range(2):
            for char in loading:
                print(f"\r{filling}{self.txt_white}{char}{text_generating}",
                      end="", flush=True)
                time.sleep(0.1)

        filling = " " * max(0, ((visual_width - (len(text_generated) // 2))))
        print(f"\r{filling}{text_generated}    ")

        filling = " " * max(0, ((visual_width - (len(text_algo_display) // 2))))
        print(f"\r{filling}{text_algo_display}{STYLE.reset}")

        # Start the random sequence based on the seed given/generated
        random.seed(self.seed)
        self._fill_maze()

        if rendering:
            self._print_maze()

        if self.algorithm == ALGO_MODE.rb:
            pass

        recursive_backtracking(self, True)

        # Put the cursor at the bottom of the screen
        if rendering:
            print(Cursor.POS(1, self.height + self.y_offset))
        print(f"{self.txt_white}Seed: {self.seed}")

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
            self.maze[(x, y)] = MAZE.empty

            if rendering:
                curs_x = (x * self.step_x) + 1
                curs_y = y + self.y_offset

                symbol = self.visual_empty
                color = COLORS.reset

                if x == self.entry_x and y == self.entry_y:
                    symbol = self.visual_wall
                    color = self.color_entry
                elif x == self.exit_x and y == self.exit_y:
                    symbol = self.visual_wall
                    color = self.color_exit

                print(Cursor.POS(curs_x, curs_y) + f"{color}{symbol}{COLORS.reset}", end="", flush=True)
                time.sleep(0.001)

    def _fill_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if x == self.entry_x and y == self.entry_y:
                    self.maze[(x, y)] = MAZE.entry
                elif x == self.exit_x and y == self.exit_y:
                    self.maze[(x, y)] = MAZE.exit
                elif (x, y) in self.fourtytwo_coord:
                    self.maze[(x, y)] = MAZE.fortytwo
                else:
                    self.maze[(x, y)] = MAZE.wall

    def _print_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[(x, y)]
                current_color = COLORS.reset
                symbol_to_print = self.visual_empty

                if x == self.entry_x and y == self.entry_y:
                    current_color = self.color_entry
                    symbol_to_print = self.visual_wall
                elif x == self.exit_x and y == self.exit_y:
                    current_color = self.color_exit
                    symbol_to_print = self.visual_wall
                elif cell == MAZE.fortytwo:
                    current_color = self.color_ft
                    symbol_to_print = self.visual_wall
                elif cell == MAZE.wall:
                    current_color = self.color_wall
                    symbol_to_print = self.visual_wall

                print(f"{current_color}{symbol_to_print}{COLORS.reset}", end="")
            print()

    def _customize_maze_walls_color(self) -> str:
        print(f"{self.txt_white}Choose walls color:")
        print(f"{COLORS.white}1. White\t {COLORS.blue}3. Blue\t "
              f"{COLORS.lightyellow}5. Yellow")
        print(f"{COLORS.magenta}2. Magenta\t {COLORS.cyan}4. Cyan\t "
              f"{COLORS.green}6. Green")

        user_choice = input(f"{self.txt_white}Enter choice: ")
        try:
            choice = int(user_choice)

            if choice >= 1 and choice <= 6:
                print(Cursor.UP(4) + ANIM.clear, end="")
                self._apply_wall_color(choice)
                return "ok"
            else:
                raise ValueError

        except ValueError:
            print(f"{COLORS.red}Invalid choice. Choose between 1 and 6.", end="",
                  flush=True)
            time.sleep(1)
            print(Cursor.UP(5) + "\r" + ANIM.clear, end="")
        return ""

    def _generate_random_seed(self) -> None:
        random_seed = ''.join(random.choices(string.ascii_letters +
                                             string.digits,
                                             k=random.randint(1, 101)))
        self.seed = random_seed

    def _apply_wall_color(self, choice: int) -> None:
        color = {
            1: COLORS.white,
            2: COLORS.magenta,
            3: COLORS.blue,
            4: COLORS.cyan,
            5: COLORS.yellow,
            6: COLORS.green
        }
        self.color_wall = color.get(choice)
