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
git clone https://github.com/Overtekk/push_swap
```
#### 2. Run the program:
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

### 🤖 Maze generation algorithm:
#### Explanation:
wip
#### Why we choose this:
wip
#### Part of the code reusable, and how to do it:
wip


### 🧑‍🏫 The Team:
#### Roles of each team member:
wip
#### Anticipated planning, and the evolution:
wip
#### What worked well, what improvement could be done:
wip


### 📂 Specific tools:
wip


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
