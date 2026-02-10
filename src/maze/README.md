# mazegen - Maze Generation Library
*by roandrie, rruiz*

Reusable Python library for maze generation and solving.\
This module contains the maze generation logic, and the solving part. You can choose to render it, or keep it simple.

###### Github: https://github.com/Overtekk/A_Maze_ing

---
## 🔑 Public API

```python
from maze import MazeConfig, MazeGenerator, MazeSolver, MazeConfigError, MazeGenerationError
from maze.maze_customization import MAZE, DISPLAY_MODE
```

- MazeConfig — base model class checking configuration and creating the config object.
- MazeGenerator — factory used to instantiate maze and print it.
- MazeSolver — class to check if a maze is solvable.
- MazeConfigError — custom error inherited from MazeError, and Exception to catch config error.
- MazeGenerationError — custom error inherited from MazeError, and Exception to catch generation error.

---

## 🚨 MazeGenerator

- Create unique maze based on a seed (can be reproduce).
- Seed is generated automatically if user doesn't provide it.
- Render the maze based on user choice.
- Solve the maze to provide a fully functionnal maze.
- Generated **perfect** and **imperfect** mazes.
- Generated walls around the maze to keep it simple.
- Provides multiples display and algorithms.

## 🗒️ Functions
|MazeConfig|MazeGenerator|MazeSolver|MazeError|
|:--------:|:-----------:|:--------|:--------:|
|from_config_file(path): Validate config and return an MazeConfig object|maze_generator(rendering:bool (False default)): Generate the maze, solve it and render it|find_path(): Find the shortest path in your generated maze|MazeError: Base exception class for all maze-related errors|
| |print_maze(): Print the maze on the terminal|path_checker(): Counts the total number of distinct paths from entry to exit|MazeConfigError: Exception raised for configuration and parameter errors|
| | |print_maze_solver(): Render the maze with the solution|MazeGenerationError: Exception raised for runtime errors during maze generation|
| |get_maze_parameters(): Print the maze parameters|print_path(): Animate the solution path over a printed maze|
| | | |

---

## 🌚 Quick example

```python
#!/usr/bin/env python3

import sys
from maze import MazeConfig, MazeGenerator, MazeSolver, MazeConfigError, MazeGenerationError

# Generate the config object with custom parameters.
try:
	config = MazeConfig(width=20, height=20, entry=(0,0), exit=(18,12), output_file="maze.txt", perfect=False, display="emoji", algorithm="rb")

	# Instanciate a new maze.
	generator = MazeGenerator(config)

	# Generate a new maze and display it.
	generator.maze_generator(rendering=True)

	# Display the maze parameters.
	generator.get_maze_parameters()

	# Create new config from file.
	cool_config = MazeConfig.from_config_file("config.txt")

	# Instanciate another maze and do not render it.
	my_super_maze = MazeGenerator(cool_config)
	my_super_maze.maze_generator(rendering=False)

	# Solve a maze and print the result
	solver = MazeSolver(my_super_maze)
	solver.find_path()
	solver.print_maze_solver()

except (FileNotFoundError, ValueError, MazeConfigError, MazeGenerationError) as e:
    print(f"{type(e).__name__}: {e}", file=sys.stderr)
```

<br>

#### For maze_customization:

Our maze use Enum class type to customize the maze:
- **MAZE**: is used to check each cell. For example: `MAZE.empty` is an empty cell. So you can do something like

```python
# Check if coords are of type empty.
if generator.maze[(x, y)] == MAZE.empty:
	# do something
```

|Name|Value|
|:---:|:--:|
|EMPTY|0|
|WALL|1|
|EXIT|2|
|ENTRY|3|
|FORTYTWO|4|

- **DISPLAY_MODE**: is used to check the display mode.
```python
# Check if display is of type emoji.
if generator.display == DISPLAY_MODE.emoji:
	# do something
```

|Name|Value|
|:---:|:--:|
|ASCII|ascii|
|EMOJI|emoji|
|SIMPLE|simple|

> [!NOTE]
> "simple" is used for the debug mode, so things may not works like usual.

---

### 🔮 Deep explanation:

All the files in the `src/maze/` folder are a part of the package.

Install the package using `pip`
```bash
pip install ~/mazegen-1.0.0-py3-none-any.whl
```

Import the generator using
```python
from maze.maze_generator import MazeGenerator
```

In your code, you can use the `MazeGenerator()` function to generate a Maze and store it a variable.\
To import your configs, you can use two methods:

- Using the `MazeConfig` import (`from maze.maze_config import MazeConfig`). Then:
```python
config = MazeConfig.from_config_file("config.txt")
```

Make sur that your config match the format above (or copy-paste the file in the repo).
- Alternatively, past your config directly in the function call:
```python
config = MazeConfig(width=50, height=50, entry=(0,0), exit=(18,12),output_file="maze.txt", perfect=False)
```
<br>

Then you can create your `MazeGenerator` object using:
```python
generator = MazeGenerator(config)
```

To generate the maze, use:
```python
generator.maze_generator(rendering=True)
```
- rendering: True to print the maze in the terminal.

<br>

Other functions:

You can print the maze parameters by using:
```python
print(generator.get_maze_parameters())
```

You can print the maze using:
```python
generator.print_maze()
```

<br>

The generator use the `MazeSolver` class itself to check if the Maze can be solved. You can import this package `from maze.maze_solver import MazeSolver` and use this function to create the `MazeSolver` object.
```python
solver = MazeSolver(generator)
```

Then, check if a path exist using:
```python
solver.find_path()
```

and print it using:
```python
solver.print_maze_solver()
```

---

## 📑 Configuration file format
You can configure your maze by using those keys:

|Key|Description|Example|
|:---|:---:|:---:|
|WIDTH| Maze width (number of cells)|WIDTH=20
|HEIGHT| Maze height| HEIGHT=15
|ENTRY| Entry coordinates (x,y)|ENTRY=0,0
|EXIT| Exit coordinates (x,y)|EXIT=19,14
|OUTPUT_FILE| Output filename|OUTPUT_FILE=maze.txt
|PERFECT| Is the maze perfect?|PERFECT=True
|SEED| (Optional) Seed to use|SEED=42|
|DISPLAY| (Optional) Display for rendering|DISPLAY=ascii|
|ALGORITHM| (Optional) Algorithm to use|ALGORITHM=rb|

**Display** : `emoji` *(default)* | `ascii`\
**Algorithm**: `rb` *(default)* | `huntandkill`

---
