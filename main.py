from typing import List, Tuple
from PIL import Image
import numpy as np

WIDTH, HEIGHT = 820, 312

# Camera dimensions
LEFT, RIGHT = -2, 2
BOTTOM, TOP = -2, 2


def get_image_index(x: float, y: float) -> Tuple[int, int]:
    x_ndc = (x - LEFT) * (WIDTH / (RIGHT - LEFT))
    y_ndc = (y - BOTTOM) * (HEIGHT / (TOP - BOTTOM))
    return int(HEIGHT - y_ndc), int(x_ndc)


def render_frame(points) -> Image:
    img_array = np.zeros((HEIGHT, WIDTH))
    img_array[:, :] = 255
    for x, y in points:
        row, col = get_image_index(x, y)
        if 0 <= row < HEIGHT and 0 <= col < WIDTH:
            img_array[row, col] = 0

    return Image.fromarray(img_array)


def update_positions(t: float, dt: float, points: List[List[int]]) -> None:
    for i, (x, y) in enumerate(points):
        x_prime = -y ** 2 - t ** 2 + t * x
        y_prime = y * t + x * y
        points[i] = [x + x_prime * dt, y + y_prime * dt]

    print(points[0])

def main():
    frames = []
    points = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    a = -2
    b = 2
    N = 200
    dt = (b - a) / N

    for t in np.linspace(a, b, N):
        frame = render_frame(points)
        frames.append(frame)
        update_positions(t, dt, points)

    frames[0].save(
        "moving_text.gif",
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=30,
        loop=0
    )


if __name__ == "__main__":
    main()
