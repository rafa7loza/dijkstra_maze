import time
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from svglib.svglib import svg2rlg
from reportlab .graphics import renderPM
from math import floor
from Graph import Graph
from maze import Maze

UP = 'N'
DOWN = 'S'
LEFT = 'E'
RIGHT = 'W'


def add_edge(u, v, graph):
    graph.add_edge(source=u.get_id(),
                   destination=v.get_id(),
                   w=v.get_weight())


def generate_graph(maze, n, m):
    # initializing the Graph
    graph = Graph(n*m)

    for i in range(m):
        for j in range(n):
            u = maze.cell_at(i, j)
            walls = u.walls

            if not walls[UP] and j > 0:
                v = maze.cell_at(i, j-1)
                add_edge(v, u, graph)
            if not walls[DOWN] and j < n-1:
                v = maze.cell_at(i, j+1)
                add_edge(v, u, graph)
            if not walls[RIGHT] and i > 0:
                v = maze.cell_at(i-1, j)
                add_edge(v, u, graph)
            if not walls[LEFT] and i < m-1:
                v = maze.cell_at(i+1, j)
                add_edge(v, u, graph)

    return graph


def main():
    image_name = 'maze.png'
    svg_name = 'maze.svg'
    # Maze dimensions (ncols, nrows)
    nx, ny = 15, 15
    # Maze entry position
    ix, iy = 0, 0

    maze = Maze(nx, ny, ix, iy)
    maze.make_maze()
    """
    maze.write_svg(svg_name)
    draw = svg2rlg(svg_name)
    renderPM.drawToFile(draw, image_name, fmt='PNG')
    img = mpimg.imread(image_name)
    plt.imshow(img)
    plt.draw()
    plt.show()
    """
    graph = generate_graph(maze, nx, ny)
    print(maze.get_current_position())
    print(maze.get_objective_position())

    source = maze.get_current_position()
    destination = maze.get_objective_position()
    path = graph.dijsktra(source=maze.cell_at(source[0], source[1]).get_id(),
                          destination=maze.cell_at(destination[0], destination[1]).get_id())
    print(path)
    # print(graph)
    for i in range(len(path)):
        x, y = path[i][:2]
        path[i] = (floor(x/nx), y % ny)

    print(path)

    for p in path:
        new_position = tuple(p[:2])
        # print(new_position)
        maze.update_current_position(new_position)
        maze.write_svg(svg_name)
        draw = svg2rlg(svg_name)
        renderPM.drawToFile(draw, image_name, fmt='PNG')
        img = mpimg.imread(image_name)
        plt.imshow(img)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.2)

    plt.show()


if __name__ == "__main__":
    main()
