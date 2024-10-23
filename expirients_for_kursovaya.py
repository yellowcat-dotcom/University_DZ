"""
Potential Field based path planner
Планировщик пути на основе потенциальных полей для робота
"""

from collections import deque
import random

import numpy as np
import matplotlib.pyplot as plt

# Parameters
KP = 5.0  # коэффициент для притягивающего потенциала | коэффициент, управляющий силой притяжения к цели.
ETA = 100.0  # коэффициент для отталкивающего потенциала | коэффициент, управляющий силой отталкивания от препятствий.
AREA_WIDTH = 30.0  # ширина потенциального поля [м] ширина пространства, в котором строится потенциальное поле.

OSCILLATIONS_DETECTION_LENGTH = 3  # длина истории для проверки осцилляций \ исло предыдущих позиций робота, которые
# используются для обнаружения осцилляций (если робот застревает)

show_animation = True  # показывать анимацию


# Функция расчета потенциального поля
# gx, gy — координаты цели (goal).
# ox, oy — координаты препятствий (obstacles).
# reso — разрешение сетки (шаг сетки в метрах).
# rr — радиус робота.
# sx, sy — координаты начальной точки (start).

def calc_potential_field(gx, gy, ox, oy, reso, rr, sx, sy):
    minx = min(min(ox), sx, gx) - AREA_WIDTH / 2.0
    miny = min(min(oy), sy, gy) - AREA_WIDTH / 2.0
    maxx = max(max(ox), sx, gx) + AREA_WIDTH / 2.0
    maxy = max(max(oy), sy, gy) + AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, minx, miny


#  Рассчитывает притягивающий потенциал на точке (x, y) относительно цели (gx, gy).
# Притягивающий потенциал пропорционален расстоянию до цели.

def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * KP * np.hypot(x - gx, y - gy)


# Рассчитывает отталкивающий потенциал для точки (x, y)
# относительно ближайшего препятствия (ox[i], oy[i]).
# Чем ближе к препятствию, тем сильнее отталкивание.
# Если точка слишком близка к препятствию (меньше радиуса робота),
# отталкивание становится очень сильным.

def calc_repulsive_potential(x, y, ox, oy, rr):
    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1

        return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
    else:
        return 0.0


def get_motion_model():
    # dx, dy
    motion = [[1, 0],  # вправо
              [0, 1],  # вверх
              [-1, 0],  # влево
              [0, -1],  # вниз
              [-1, -1],  # влево-вниз
              [-1, 1],  # влево-вверх
              [1, -1],  # вправо-вниз
              [1, 1],  # вправо-вверх
              [2, 1],  # вправо-вверх под углом
              [1, 2],  # вверх-вправо под углом
              [-2, -1],  # влево-вниз под углом
              [-1, -2],  # вниз-влево под углом
              [2, -1],  # вправо-вниз под углом
              [1, -2],  # вниз-вправо под углом
              [-2, 1],  # влево-вверх под углом
              [-1, 2]]  # вверх-влево под углом

    return motion


# Обнаружение осцилляций
# Функция сохраняет последние позиции робота и проверяет,
# не возвращался ли робот на одну из предыдущих позиций,
# что может свидетельствовать об осцилляции (застревании).
def oscillations_detection(previous_ids, ix, iy):
    previous_ids.append((ix, iy))

    if (len(previous_ids) > OSCILLATIONS_DETECTION_LENGTH):
        previous_ids.popleft()

    # check if contains any duplicates by copying into a set
    previous_ids_set = set()
    for index in previous_ids:
        if index in previous_ids_set:
            return True
        else:
            previous_ids_set.add(index)
    return False


# Основная функция планирования пути
def potential_field_planning(sx, sy, gx, gy, ox, oy, reso, rr):

    # calc potential field
    pmap, minx, miny = calc_potential_field(gx, gy, ox, oy, reso, rr, sx, sy)

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round((sx - minx) / reso)
    iy = round((sy - miny) / reso)
    gix = round((gx - minx) / reso)
    giy = round((gy - miny) / reso)

    if show_animation:
        draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    previous_ids = deque()

    oscillation_count = 0  # Счетчик осцилляций

    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]) or inx < 0 or iny < 0:
                p = float("inf")  # outside area
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

        # Проверка осцилляций
        if oscillations_detection(previous_ids, ix, iy):
            print("Oscillation detected at ({},{})!".format(ix, iy))
            oscillation_count += 1
            if oscillation_count > 3:  # Если осцилляция повторяется
                # Добавляем случайный шаг для выхода из осцилляции
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


#  Функция рисует тепловую карту потенциального поля,
#  где области с низким потенциалом (близкие к цели) будут более светлыми,
#  а области с высоким потенциалом (близкие к препятствиям) — темнее.
def draw_heatmap(data):
    data = np.array(data).T
    plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)


def main():
    print("potential_field_planning start")

    sx = 0.0  # начальная координата x
    sy = 10.0  # начальная координата y
    gx = 30.0  # координата x цели
    gy = 30.0  # координата y цели
    grid_size = 0.5  # размер ячейки сетки (разрешение)
    robot_radius = 5.0  # радиус робота

    ox = [15.0, 5.0, 20.0, 25.0, 21.0]  # координаты x препятствий
    oy = [25.0, 15.0, 26.0, 25.0, 23.0]  # координаты y препятствий

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # Генерация пути
    _, _ = potential_field_planning(
        sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
