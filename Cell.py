class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y, w=1, maze_size=14):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.is_current_position = False
        self.weight = w
        self.occupied = False
        self.is_objective = False

        self.__size_of_maze = maze_size
        self.__id = (x*self.__size_of_maze) + y

    def change_size_of_maze(self, size):
        self.__size_of_maze = size
        self.__id = (self.x*self.__size_of_maze) + self.y

    def get_id(self):
        return self.__id

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False
