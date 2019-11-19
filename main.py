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
LEFT = 'W'
RIGHT = 'E'


def add_edge(u, v, graph):
    graph.add_edge(source=u.get_id(),
                   destination=v.get_id(),
                   w=v.get_weight())


def generate_graph(maze, _nx, _mx):
    # initializing the Graph
    graph = Graph(_nx * _mx)

    for _x in range(_mx):
        for _y in range(_nx):
            u = maze.cell_at(_x, _y)
            walls = u.walls

            if not walls[UP] and _y < 0:
                v = maze.cell_at(_x, _y-1)
                add_edge(v, u, graph)
            if not walls[DOWN] and _y < _mx-1:
                v = maze.cell_at(_x, _y+1)
                add_edge(v, u, graph)
            if not walls[RIGHT] and _x < _nx-1:
                v = maze.cell_at(_x+1, _y)
                add_edge(v, u, graph)
            if not walls[LEFT] and _x > 0:
                v = maze.cell_at(_x-1, _y)
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
    # print(path)
    # print(graph)
    del graph
    movements = []
    for i in range(len(path)):
        positions = path[i][:2]
        u, v = maze.get_position_by_id(positions[0]), maze.get_position_by_id(positions[1])
        movements.append([u, v, path[i][2]])
        # path[i] = (x % nx, floor(y / ny))

    # print(path)

    for p in movements:
        # new_position = tuple(p[:2])
        new_position = p[1]
        maze.update_current_position(new_position)
        # print(maze.cell_at(new_position[0], new_position[1]).walls)
        print(p[2])
        maze.write_svg(svg_name)
        draw = svg2rlg(svg_name)
        renderPM.drawToFile(draw, image_name, fmt='PNG')
        img = mpimg.imread(image_name)
        plt.imshow(img)
        plt.draw()
        plt.pause(1e-19)
        # time.sleep(0.2)

    plt.show()
    plt.close()



if __name__ == "__main__":
    main()
