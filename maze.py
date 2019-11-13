import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import random
import time
from svglib.svglib import svg2rlg
from reportlab .graphics import renderPM
from Cell import Cell


# Disclaim: Most part of this code was taken from the source mentioned below.
# It has been modified according to my needs.

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
        self.svg_name = "maze.svg"
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

        self.initial_x, self.initial_y = random.randint(0, nx - 1), random.randint(0, ny - 1)
        self.cell_at(self.initial_x, self.initial_y).is_current_position = True
        self.cell_at(self.initial_x, self.initial_y).occupied = True
        print(self.initial_x, self.initial_y)

        # Generating the traps
        for i in range(num_traps):
            _x, _y = self.generate_random_position(nx, ny)
            w = random.randint(2, 9)
            self.cell_at(_x, _y).occupied = True
            self.cell_at(_x, _y).weight = w

        cnt = 0
        for row in self.maze_map:
            for elem in row:
                if elem.occupied:
                    print(str(elem.x) + " " + str(elem.y) + ": " + str(elem.is_current_position))
                    cnt += 1
        print(cnt)

    def generate_random_position(self, x, y):
        while True:
            _x, _y = random.randint(0, x - 1), random.randint(0, y - 1)
            if not self.cell_at(_x, _y).occupied:
                return [_x, _y]

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
            f.write('\t<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'
                    .format(x1, y1, x2, y2),)

        def write_circle(file, x_coordinate, y_coordinate, radius, color):
            """Write an image to the SVG"""
            file.write('\t<circle cx="{}" cy="{}" r="{}" fill="{}"/>\n'
                       .format(x_coordinate, y_coordinate, radius, color))

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            f.write('<?xml version="1.0" encoding="utf-8"?>')
            f.write('<svg\n\txmlns="http://www.w3.org/2000/svg"\n'
                    '\txmlns:xlink="http://www.w3.org/1999/xlink"\n')
            f.write('\twidth="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width+2*padding, height+2*padding,
                    -padding, -padding, width+2*padding, height+2*padding))
            f.write('<defs>\n<style type="text/css"><![CDATA[line {\n')
            f.write('\tstroke: #000000;\n\tstroke-linecap: square;\n\tstroke-width: 5;\n}')
            f.write(']]></style>\n</defs>\n')
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

                    # Draw any circle in the maze
                    if self.cell_at(x, y).occupied:
                        adjustment = (3*padding) / 2
                        _x = x*scx + adjustment
                        _y = y * scy + adjustment

                        if self.cell_at(x, y).is_current_position:
                            print("Debbug")
                            write_circle(file=f,
                                         x_coordinate=_x,
                                         y_coordinate=_y,
                                         radius=padding,
                                         color="blue")
                        else:
                            write_circle(file=f,
                                         x_coordinate=_x,
                                         y_coordinate=_y,
                                         radius=padding,
                                         color="red")

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            f.write('\t<line x1="0" y1="0" x2="{}" y2="0"/>\n'.format(width))
            f.write('\t<line x1="0" y1="0" x2="0" y2="{}"/>\n'.format(height))
            f.write('</svg>')

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
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
    # plt.show()

    for n in range(2, 16):
        maze = Maze(n, n, num_traps=int((n*3)/4))
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



if __name__ == "__main__":
    main()
