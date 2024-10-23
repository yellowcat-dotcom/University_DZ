"""
Potential Field based path planner
Планировщик пути на основе потенциальных полей для робота
Рандомятся преграды и цели
"""
from collections import deque
import random
import numpy as np
import matplotlib.pyplot as plt


# Parameters
KP = 5.0  # коэффициент для притягивающего потенциала
ETA = 100.0  # коэффициент для отталкивающего потенциала
AREA_WIDTH = 30.0  # ширина потенциального поля [м]
OSCILLATIONS_DETECTION_LENGTH = 3  # длина истории для проверки осцилляций

show_animation = True  # показывать анимацию


# Функция для генерации случайных препятствий
def generate_random_obstacles(num_obstacles, area_width, robot_radius):
    ox = []
    oy = []
    for _ in range(num_obstacles):
        # Генерация случайных координат в пределах области
        x = random.uniform(0, area_width)
        y = random.uniform(0, area_width)
        ox.append(x)
        oy.append(y)
    return ox, oy


# Функция для генерации случайных координат цели
def generate_random_goal(area_width):
    gx = random.uniform(0, area_width)
    gy = random.uniform(0, area_width)
    return gx, gy


def calc_potential_field(gx, gy, ox, oy, reso, rr, sx, sy):
    minx = min(min(ox), sx, gx) - AREA_WIDTH / 2.0
    miny = min(min(oy), sy, gx) - AREA_WIDTH / 2.0
    maxx = max(max(ox), sx, gx) + AREA_WIDTH / 2.0
    maxy = max(max(oy), sy, gx) + AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    pmap = [[0.0 for _ in range(yw)] for _ in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, minx, miny


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * KP * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1
        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0


def get_motion_model():
    motion = [[1, 0], [0, 1], [-1, 0], [0, -1],
              [-1, -1], [-1, 1], [1, -1], [1, 1],
              [2, 1], [1, 2], [-2, -1], [-1, -2],
              [2, -1], [1, -2], [-2, 1], [-1, 2]]
    return motion


def oscillations_detection(previous_ids, ix, iy):
    previous_ids.append((ix, iy))

    if len(previous_ids) > OSCILLATIONS_DETECTION_LENGTH:
        previous_ids.popleft()

    previous_ids_set = set()
    for index in previous_ids:
        if index in previous_ids_set:
            return True
        else:
            previous_ids_set.add(index)
    return False


def potential_field_planning(sx, sy, gx, gy, ox, oy, reso, rr):
    pmap, minx, miny = calc_potential_field(gx, gy, ox, oy, reso, rr, sx, sy)

    d = np.hypot(sx - gx, sy - gy)
    ix = round((sx - minx) / reso)
    iy = round((sy - miny) / reso)
    gix = round((gx - minx) / reso)
    giy = round((gy - miny) / reso)

    if show_animation:
        draw_heatmap(pmap)
        plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    previous_ids = deque()

    oscillation_count = 0

    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]) or inx < 0 or iny < 0:
                p = float("inf")
                print("outside potential!")
            else:
                p = pmap[inx][iny]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny

        ix = minix
        iy = miniy
        xp = ix * reso + minx
        yp = iy * reso + miny
        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)

        if oscillations_detection(previous_ids, ix, iy):
            print("Oscillation detected at ({},{})!".format(ix, iy))
            oscillation_count += 1
            if oscillation_count > 3:
                random_motion = random.choice(motion)
                ix += random_motion[0]
                iy += random_motion[1]
                print("Random step applied to break oscillation.")
            continue

        if show_animation:
            plt.plot(ix, iy, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry


def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)


def main():
    print("potential_field_planning start")

    sx = 0.0  # начальная координата x
    sy = 10.0  # начальная координата y
    grid_size = 0.5  # размер ячейки сетки (разрешение)
    robot_radius = 5.0  # радиус робота

    num_obstacles = 5  # количество препятствий
    area_width = AREA_WIDTH  # ширина пространства

    # Генерация случайных препятствий
    ox, oy = generate_random_obstacles(num_obstacles, area_width, robot_radius)

    # Генерация случайной цели
    gx, gy = generate_random_goal(area_width)

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # Генерация пути
    _, _ = potential_field_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
