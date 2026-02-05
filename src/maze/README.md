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
To import your configs, you can use two methods:\
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
