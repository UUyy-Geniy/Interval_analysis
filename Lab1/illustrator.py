import matplotlib.pyplot as plt
from interval_module import Interval
import numpy as np
import os


def illustrate_matrix(matrix, step_number, delta,folder_name="fmatrix"):
    def draw_square(point, widths, step_number, color):
        x, y = point
        dx, dy = widths
        x_left = np.linspace(0, x - dx/2)
        x_right = np.linspace(0, x + dx/2) 
        if dx == 0 or dy == 0:
            plt.plot(x, y, 'o', color=color, markersize=10)
            # plt.text(x, y, f"({x:.2f}, {y:.2f})", ha="center", va="center")
            if dx == 0:
                plt.plot([x, x], [y - dy / 2, y + dy / 2], color=color)
            else:
                plt.plot([x - dx / 2, x + dx / 2], [y, y], color=color)
                plt.plot(x - dx / 2, y, 'o', color=color)
                plt.plot(x + dx / 2, y, 'o', color=color)
                plt.plot(x_left, y/(x-dx/2) * x_left, color=color, linestyle='dashed')
                plt.plot(x_right, y/(x+dx/2) * x_right, color=color, linestyle='dashed')
        else:
            plt.gca().add_patch(plt.Rectangle((x - dx / 2, y - dy / 2), dx, dy,
                                            edgecolor=color, facecolor=color,
                                            alpha=0.3))
            plt.plot(x_left, (2*y + dy)/(2*x-dx) * x_left, color=color, linestyle='dashed')
            plt.plot(x_right, (2*y -dy)/(2*x+dx) * x_right, color=color, linestyle='dashed')

    plt.figure(step_number, figsize=(16, 8))
    colors = plt.cm.tab20(np.linspace(0, 1, 2 * len(matrix)))
    matrix_t = matrix.transpose()
    for i, row in enumerate(matrix_t):
        point = [item.mid() for item in row]
        plt.plot(point[0], point[1], 'o', color=colors[i])
        draw_square(point, [item.width() for item in row], step_number, colors[i])

    plt.grid()
    plt.title(f"Step {step_number}, delta = {np.round(delta, 3)}")

    base_dir = os.path.abspath(os.path.join(".", "Lab1/graphics"))
    path_info = os.path.join(base_dir, folder_name)
    
    # Создаём папку, если её не существует
    os.makedirs(path_info, exist_ok=True)
    plt.savefig(f"{path_info}/step_{step_number}.png", dpi=200, bbox_inches='tight')
    plt.show()





