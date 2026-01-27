# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_customization.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie, rruiz                           +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/27 16:35:27 by roandrie        #+#    #+#               #
#  Updated: 2026/01/27 18:31:04 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum

from colorama import Fore, Style


class MAZE(str, Enum):
    empty = " "
    entry = "\u2588"
    exit = "\u2588"
    wall = "\u2588"
    fortytwo = "\u2588"

    def __str__(self):
        return self.value


class COLORS(Enum):
    green = Fore.GREEN
    black = Fore.BLACK
    blue = Fore.BLUE
    cyan = Fore.CYAN
    white = Fore.WHITE
    lightblack = Fore.LIGHTBLACK_EX
    lightblue = Fore.LIGHTBLUE_EX
    lightcyan = Fore.LIGHTCYAN_EX
    lightgreen = Fore.LIGHTGREEN_EX
    lightmagenta = Fore.LIGHTMAGENTA_EX
    lightred = Fore.LIGHTRED_EX
    lightwhite = Fore.LIGHTWHITE_EX
    lightyellow = Fore.LIGHTYELLOW_EX
    magenta = Fore.MAGENTA
    red = Fore.RED
    reset = Fore.RESET
    yellow = Fore.YELLOW

    def __str__(self):
        return self.value


class STYLE(Enum):
    bright = Style.BRIGHT
    dim = Style.DIM
    reset = Style.RESET_ALL

    def __str__(self):
        return self.value


class ANIM(str, Enum):
    clear = "\033[J"
    clear_screen = "\033[2J\033[H"

    def __str__(self):
        return self.value


class DISPLAY_MODE(str, Enum):
    ascii = "ascii"
    better_ascii = "betterascii"
    emoji = "emoji"

    def __str__(self):
        return self.value


class ALGO_MODE(str, Enum):
    rb = "rb"

    def __str__(self):
        return self.value
