# % pylab inline
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import random
import time
from svglib.svglib import svg2rlg
from reportlab .graphics import renderPM
from Cell import Cell
from Traps import Traps


# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.

class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0, num_traps = 10):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.svgname = "maze.svg"
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

        self.initial_x, self.initial_y = random.randint(0, nx-1), random.randint(0, ny-1)
        self.cell_at(self.initial_x, self.initial_y).is_current_position = True
        self.cell_at(self.initial_x, self.initial_x).occupied = True
        print(self.initial_x, self.initial_y)

        self.traps = []
        for i in range(num_traps):
            while True:
                _x, _y = random.randint(0, nx-1), random.randint(0, ny-1)
                if not self.cell_at(_x, _y).occupied:
                    self.traps.append(Traps(_x, _y, random.randint(2, 10)))
                    self.cell_at(_x, _y).occupied = True
                    break

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                prefix = " "
                if self.cell_at(x, y).is_current_position:
                    prefix = "*"
                if self.cell_at(x, y).walls['E']:
                    maze_row.append(prefix + '|')
                else:
                    maze_row.append(prefix + ' ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.cell_at(x, y).walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(f, x1, y1, x2, y2):
            """Write a single wall to the SVG image file handle f."""
            f.write('<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'
                    .format(x1, y1, x2, y2),)

        def write_object(file, x_coordinate, y_coordinate, radius):
            """Write an image to the SVG"""
            file.write('<circle cx="{}" cy="{}" r="{}"/>\n'
                       .format(x_coordinate, y_coordinate, radius))

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            f.write('<?xml version="1.0" encoding="utf-8"?>')
            f.write('<svg\n\txmlns="http://www.w3.org/2000/svg"\n'
                    '\txmlns:xlink="http://www.w3.org/1999/xlink"\n')
            f.write('\twidth="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width+2*padding, height+2*padding,
                    -padding, -padding, width+2*padding, height+2*padding))
            f.write('<defs>\n<style type="text/css"><![CDATA[')
            f.write('line {')
            f.write('    stroke: #000000;\n    stroke-linecap: square;')
            f.write('    stroke-width: 5;\n}')
            f.write(']]></style>\n</defs>')
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    # print(str(x) + "  " + str(y))
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).is_current_position:
                        adjustment = (3*padding)/ 2
                        if x == 0:
                            _x = x*scx + adjustment
                        else:
                            _x = x*scx - adjustment
                        if y == 0:
                            _y = y * scy + adjustment
                        else:
                            _y = y * scy - adjustment
                        w, h = padding, padding
                        write_object(file=f,
                                     x_coordinate=_x,
                                     y_coordinate=_y,
                                     radius=padding)

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            f.write('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width))
            f.write('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height))
            f.write('</svg>')

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1


def main():
    image_name = 'maze.png'
    svg_name = 'maze.svg'
    # Maze dimensions (ncols, nrows)
    nx, ny = 15, 15
    # Maze entry position
    ix, iy = 0, 0

    maze = Maze(nx, ny, ix, iy)
    maze.make_maze()

    # print(maze)
    maze.write_svg(svg_name)
    draw = svg2rlg(svg_name)
    renderPM.drawToFile(draw, image_name, fmt='PNG')


    img = mpimg.imread(image_name)
    imgplot = plt.imshow(img)
    plt.show()
    """
    for n in range(2, 15):
        maze = Maze(n, n)
        maze.make_maze()
        maze.write_svg(svg_name)
        draw = svg2rlg(svg_name)
        renderPM.drawToFile(draw, image_name, fmt='PNG')
        img = mpimg.imread(image_name)
        imgplot = plt.imshow(img)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.1)

    plt.show()
    """


if __name__ == "__main__":
    main()