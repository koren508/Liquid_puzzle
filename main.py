import heapq
import random
# import unittest

import heapq
import random

class TubePuzzle:
    def __init__(self, num_tubes=None, num_colors=None, tube_capacity=None, initial_matrix=None):
        """Initialize with given parameters or a predefined matrix. Sets up tubes based on configuration."""
        if initial_matrix:
            self.tubes = initial_matrix
            self.num_tubes = len(initial_matrix)
            self.num_colors = len(set(color for tube in initial_matrix for color in tube if color))
            self.tube_capacity = max(len(tube) for tube in initial_matrix)
        else:
            self.num_tubes = num_tubes
            self.num_colors = num_colors
            self.tube_capacity = tube_capacity
            self.tubes = self.initialize_tubes()

    def initialize_tubes(self):
        """Randomly distribute colors among tubes to create the initial puzzle state."""
        colors = [color for color in range(1, self.num_colors + 1) for _ in range(self.tube_capacity)]
        random.shuffle(colors)
        tubes = [colors[i:i + self.tube_capacity] for i in range(0, len(colors), self.tube_capacity)]
        tubes += [[] for _ in range(self.num_tubes - len(tubes))]
        return tubes

    def display_tubes(self):
        """Print the current configuration of tubes for debugging purposes."""
        for index, tube in enumerate(self.tubes):
            print(f"Tube {index + 1}: {tube if tube else 'Empty'}")

    def is_goal(self):
        """Check if all tubes are sorted correctly with only one color each."""
        return all(len(set(tube)) == 1 for tube in self.tubes if tube)

    def find_moves(self):
        """Identify all legal moves from the current tube configuration."""
        moves = []
        for i, src in enumerate(self.tubes):
            if src:
                for j, dest in enumerate(self.tubes):
                    if i != j and (not dest or (dest and len(dest) < self.tube_capacity and dest[-1] == src[-1])):
                        moves.append((i, j))
        return moves

    def make_move(self, from_tube, to_tube):
        """Execute a move of a color from one tube to another."""
        self.tubes[to_tube].append(self.tubes[from_tube].pop())

def heuristic(tubes, tube_capacity):
    """
    Calculate a heuristic based on misplaced colors and minimum moves required to sort each tube.

    Parameters:
    tubes (list of list of int): The current state of the tubes, where each tube is a list of colors.
    tube_capacity (int): The maximum number of colors each tube can hold.

    Returns:
    int: The heuristic value, which is the maximum of the misplaced colors heuristic and the minimum moves heuristic.

    Example:
    >>> tubes = [[1, 2, 2], [1, 1], [2], [], [2, 2, 2], []]
    >>> tube_capacity = 3
    >>> heuristic(tubes, tube_capacity)
    4
    """
    h1 = sum(len(tube) - tube.count(max(set(tube), key=tube.count)) for tube in tubes if len(set(tube)) > 1)
    h2 = sum((tube_capacity - len(tube)) for tube in tubes if len(set(tube)) == 1)
    return max(h1, h2)

def a_star(puzzle, verbose=False):
    """Perform the A* search algorithm with optional verbose output for detailed tracing."""
    open_set = []
    heapq.heappush(open_set, (0, puzzle.tubes, [], None))
    visited = set()

    while open_set:
        _, current_state, path, last_move = heapq.heappop(open_set)

        if tuple(map(tuple, current_state)) in visited:
            continue
        visited.add(tuple(map(tuple, current_state)))

        if puzzle.is_goal():
            if verbose:
                print("Goal Reached!")
            return path

        moves = puzzle.find_moves()
        if not moves and verbose:
            print("No available moves. Stuck state reached.")

        for move in moves:
            if last_move and move == (last_move[1], last_move[0]):
                continue

            new_state = [list(tube) for tube in current_state]
            color = new_state[move[0]].pop()
            new_state[move[1]].append(color)
            new_path = path + [move]
            score = len(new_path) + heuristic(new_state, puzzle.tube_capacity)
            heapq.heappush(open_set, (score, new_state, new_path, move))

            if verbose:
                print(f"Move from Tube {move[0]+1} to Tube {move[1]+1} considered. New state:")
                for idx, tube in enumerate(new_state):
                    print(f"Tube {idx + 1}: {tube}")
                    
def generate_random_initial_matrix(num_tubes, tube_capacity, max_color):
    tubes = []
    colors = [random.randint(1, max_color) for _ in range(num_tubes * tube_capacity - random.randint(1, num_tubes))]  # Ensure some emptiness
    random.shuffle(colors)
    for i in range(0, len(colors), tube_capacity):
        tubes.append(colors[i:i + tube_capacity])
    while len(tubes) < num_tubes:
        tubes.append([])  # Ensure there are empty tubes
    return tubes

def main_simulation():
    num_iterations = 20
    for i in range(num_iterations):
        num_tubes = random.randint(5, 10)
        tube_capacity = random.randint(3, 5)
        max_color = 5
        initial_matrix = generate_random_initial_matrix(num_tubes, tube_capacity, max_color)
        puzzle = TubePuzzle(initial_matrix=initial_matrix)
        print(f"Initial configuration for iteration {i + 1}:")
        puzzle.display_tubes()
        solution = a_star(puzzle, verbose=True)
        print("Solution Steps:", solution)
        print("------------------------------------------------------")

if __name__ == "__main__":
    main_simulation()





