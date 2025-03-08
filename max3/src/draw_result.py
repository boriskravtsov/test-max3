# Mar-08-2025
# draw_result.py

import cv2 as cv

from max3.src import cfg_max3


def draw_result(tag):

    path_in = cfg_max3.dir_debug + '/' + tag + '_peaks.png'
    magn_peaks = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    x3: int = cfg_max3.X0
    y3: int = cfg_max3.Y0

    if tag == 'image':
        x1 = cfg_max3.x_image_red
        y1 = cfg_max3.y_image_red
        x2 = cfg_max3.x_image_blue
        y2 = cfg_max3.y_image_blue

    if tag == 'templ':
        x1 = cfg_max3.x_templ_red
        y1 = cfg_max3.y_templ_red
        x2 = cfg_max3.x_templ_blue
        y2 = cfg_max3.y_templ_blue

    thickness = 2

    """
    cv.line(magn_peaks,
            (x1, y1),
            (x2, y2),
            cfg_max3.clover, thickness)  # green

    cv.line(magn_peaks,
            (x1, y1),
            (x3, y3),
            cfg_max3.maraschino, thickness)  # red

    cv.line(magn_peaks,
            (x2, y2),
            (x3, y3),
            cfg_max3.aqua, thickness)  # blue
    """

    cv.line(magn_peaks,
            (x1, y1),
            (x2, y2),
            cfg_max3.dark_gray, thickness)

    cv.line(magn_peaks,
            (x1, y1),
            (x3, y3),
            cfg_max3.dark_gray, thickness)

    cv.line(magn_peaks,
            (x2, y2),
            (x3, y3),
            cfg_max3.dark_gray, thickness)

    path_out = cfg_max3.dir_debug + '/' + tag + '_result.png'
    cv.imwrite(path_out, magn_peaks)
