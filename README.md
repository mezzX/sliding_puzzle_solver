# sliding_puzzle_solver
A sliding puzzle solver using the A* algorithm
# To do:
Write a proper README.md<br>
implement some sort of "pause" in between input from the agent so that the moves are visible<br>
### Getting Started
1. Make sure you have [Python 3.6](https://www.python.org/) installed.

2. Clone the repository

3. Use [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) to create a new environment and install dependencies

    - __Linux__ or __Mac__: 
    ```bash
    conda create --name sliding python=3.6
    source activate sliding
    pip install -r requirements.txt
    ```
  
    - __Windows__: 
    ```bash
    conda create --name sliding python=3.6 
    activate sliding
    pip install -r requirements.txt
    ```

### Instructions
Navigate to the directory and run main.py

    python main.py

Click on Browse to select an image to be used for the puzzle tiles

Next select the size of the puzzle. Selecting 3 will make it a 3x3 sliding puzzle.

Finally click start to generate the puzzle

### Controls
Arrow keys to move the tiles around the gap<br>
'r' key to go back to the main menu<br>
's' key to have the algorithm solve the puzzle<br>
