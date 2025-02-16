# Feb-13-2025
# draw_image_warp.py

import cv2 as cv
import numpy as np
from pathlib import Path

from max3.src import cfg_max3


def draw_image_warp():

    path_in = str(Path.cwd() / cfg_max3.dir_debug / 'image.png')
    # path_in = str(Path.cwd() / cfg_max3.dir_debug / 'image_peaks.png')
    image_in = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    y_image_blue = cfg_max3.y_image_blue
    x_image_blue = cfg_max3.x_image_blue
    y_image_red = cfg_max3.y_image_red
    x_image_red = cfg_max3.x_image_red

    y_templ_blue = cfg_max3.y_templ_blue
    x_templ_blue = cfg_max3.x_templ_blue
    y_templ_red = cfg_max3.y_templ_red
    x_templ_red = cfg_max3.x_templ_red

    pts_image = np.float32([[x_image_blue, y_image_blue],
                            [x_image_red, y_image_red],
                            [cfg_max3.X0, cfg_max3.Y0]])

    pts_templ = np.float32([[x_templ_blue, y_templ_blue],
                            [x_templ_red, y_templ_red],
                            [cfg_max3.X0, cfg_max3.Y0]])

    mat_affine = cv.getAffineTransform(pts_image, pts_templ)

    image_out = cv.warpAffine(image_in, mat_affine, cfg_max3.dsize_roi)

    path_out = str(Path.cwd() / cfg_max3.dir_debug / 'image_warp.png')
    cv.imwrite(path_out, image_out)
