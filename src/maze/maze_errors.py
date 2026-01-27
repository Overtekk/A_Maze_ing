# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_errors.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/01/27 14:13:47 by roandrie        #+#    #+#               #
#  Updated: 2026/01/27 14:14:36 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

class MazeError(Exception):
    pass


class MazeConfigError(MazeError):
    pass


class MazeGenerationError(MazeError):
    pass
