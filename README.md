<p align="center">
  <img src="assets_github/a_maze_ing.png?v=2" width="250" />
</p>
<h3 align="center">
  <em>Create your own maze generator and display its result!</em>
</h3>

---

<div align="center">
<img src="https://img.shields.io/badge/No score%20-inactive?logo=42&logoColor=ffff" />
<img src="https://img.shields.io/badge/bonus-none-inactive"/>
<img src="https://img.shields.io/badge/date completed-none-inactive"/>
</div>

## ⚠️ Disclaimer

- **Full Portfolio:** This repository focuses on this specific project. You can find my entire 42 curriculum 👉 [here](https://github.com/Overtekk/42).
- **Subject Rules:** I strictly follow the rules regarding 42 subjects; I cannot share the PDFs, but I explain the concepts in this README.
- **Archive State:** The code is preserved exactly as it was during evaluation (graded state). I do not update it, so you can see my progress and mistakes from that time.
- **Academic Integrity:** I encourage you to try the project yourself first. Use this repo only as a reference, not for copy-pasting. Be patient, you will succeed.
- **Team Project:** For this project, I' m pairing with **rruiz** (https://github.com/shadox254)

## 📂 Description

**📜 Summary:**\
Create a **maze generator** that takes a configuration file, generates a maze and writes it to a file using a hexadecimal wall representation. The maze will also have a visual representation either in ASCII, or by using the minilibx. The maze will be generate randomly but can be reproduce via a **seed**.

**📝 Requierements**
- Each cell of the maze has between 0 and 4 walls, at each cardinal point (North,
Est, South, West).
- The entry and exist exist, are unique, are different, need to be inside the maze bounds.
- The maze is fully connected and do not have isolated cells. Walls must be at the external borders.
- The maze can't have large open areas: corridors can't be wider than 2 cells.
- The maze must contain a visible `42` wehen represented.
- If the `PERFECT` flag is activated, the maze must contain exactly one path between the entry and the exit
- The maze must be written in the output file using one hexadecimal digit per cell, where
each digit encodes which walls are closed:
- The maze generation must be implement as a **unique class**, a standalone module that can be imported in a future project.

|Bit|Direction|
|---|---|
|0|North|
|1|East|
|2|South|
|3|West|

Closed walls = 1 | Open = 0

**✏️ Visual representation**
- Use either the **terminal ASCII** or the **MiniLibX** library.
- The visual should clearly show walls, entry, exit and the solution path.

#### **User can**:
- Re-generate a new maze and display it.
- Show/Hide a valid shortest path from the entrance to the exit.
- Change maze wall colours.
- Set specific colours to display the `42` pattern.

**📮 Makefile:**\
This project must include a Makefile with strict following rules:
- `install`: Install all project dependencies using **pip**, **uv**, **pipx**, or any other package manager.
- `run`: Execute the main script of the project.
- `debug`: Run the main script in debug mode using Python`s built-in-debugger.
- `clean`: Remove all temporary files or caches.
- `lint`: Execute **flake8** (norme checker) and **mypy** (hint checker)
- `lint-strict`: Same as above but with **--strict**.

**🐍 Challenge:**
- Avoid any crashes and give clear error message.
- Prevent any leaks.
- Include type hint *(def func (name:str) -> bool)*. Use **Mypy** to check any potential error `pip install mypy`, then `mypy script.py`
- Include docstrings following **PEP 257** for better understanding.

## 🔷 Instructions

#### 1. First, clone this repository:
```bash
git clone https://github.com/Overtekk/A_Maze_ing
```
#### 2. Run the program:
##### by using the Makefile
```bash
make all
source .venv/bin/activate
make run
```
##### or (make sur to create a virtual environnement and check if dependencies are installed)
```bash
python3 a_maze_ing.py config.txt
```

#### 📑 Configuration file format
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

#### 🤖 Maze generation algorithm:
1. **Explanation**:

We choose two algorithms for this project.

The first one is the **Backtracking Algorithm**.
- First, it choose a random starting point in the maze and carve a path.
- Then, it choose a random unvisited neighbor and carve a path.
- It push the current cell to the stack/history.
- If there are no unvisited neighbors (dead end), pop from the stack to return to the previous cell.
- Finally, it continue until the algorithm returns to the starting point.

The second one is the **Hunt and Kill Algorithm**.
- It choose a random starting point in the maze and carve a path.
- If it reach a dead end, then it looks for the first cell that neighbors part of the maze. It check from the left, to the right starting the first line.

2. **Why we choose this**:

We choose those algorithms for two reasons. The first one is to train on the backtracking part. The second one is just for the visual. It looks good.

3. **Part of the code reusable, and how to do it**:

All the files in the `src/maze/` folder are a part of the package.\
Import the generator using
```python
from src.maze import MazeGenerator
```
In your code, you can use the `MazeGenerator()` function to generate a Maze and store it a variable.\
To import your configs, you can use two methods:\
- Using the `MazeConfig` import (`from src.maze import MazeConfig`). Then:
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

The generator use the `MazeSolver` class itself to check if the Maze can be solved. You can import this package `from src.maze import MazeSolver` and use this function to create the `MazeSolver` object.
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

### 🧑‍🏫 The Team:
1. Roles of each team member:

- roandrie: [norme corrector, readme writer, files organizer, writing customization and parsing]
- rruiz: [math pro, debugger, writing algorithms, docstring pro]

2. Anticipated planning, and the evolution:

There was not a planning at the start. I (roandrie) started the project before rruiz because he was still on the python modules. So I started the repo, the parsing, errors managements, creating everything we need. Then, we works and what we needed : creating the maze, filling it, creating the algorithm etc...

3. What worked well, what improvement could be done:

Our team was good. Nothing can be improved apart from our coding skill.


### 📂 Specific tools:

We use 2 differents libraries:
- `pydantic` to check if the config is correct.
- `colorama` to print the maze on the terminal and add colors and style in the text.


## 💿 Resources
#### <u>For Maze Algorithm</u>:
##### General:
- https://professor-l.github.io/mazes/
- https://www.youtube.com/watch?v=sVcB8vUFlmU
- https://en.wikipedia.org/wiki/Maze_generation_algorithm

##### Recursive Backtracking:
- https://inventwithpython.com/recursion/chapter11.html

##### Hunt and kill:
- https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm
- https://www.reddit.com/r/proceduralgeneration/comments/1f7w3u7/huntandkill_maze_algorithm/

<br>

#### <u>For Maze Solver</u>:
- https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96
- https://en.wikipedia.org/wiki/Breadth-first_search
- https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
- https://medium.com/@luthfisauqi17_68455/artificial-intelligence-search-problem-solve-maze-using-breadth-first-search-bfs-algorithm-255139c6e1a3
- https://stackoverflow.com/questions/57201946/how-do-i-find-shortest-path-in-maze-with-bfs

<br>

#### <u>For Building Package</u>:
- https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

<br>

#### <u>AI Usage</u>:

AI was use to better understanding certain things in Python. And help us on some maths aspect. Also, help use optimize more part of code (because Python can be easy but also be very unclear at some part).
