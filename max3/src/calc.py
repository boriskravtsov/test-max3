# Mar-08-2025
# calc.py

import sys
import cv2 as cv
import numpy as np

from max3.src import cfg_max3
from max3.src.magnitude import get_magn_roi, get_magn_half
from max3.src.get_peaks import get_peaks
from max3.src.create_table import create_table
from max3.src.create_joint_table import create_joint_table
from max3.src.draw_magn import draw_magn
from max3.src.draw_peaks import draw_peaks
from max3.src.draw_result import draw_result
from max3.src.draw_image_warp import draw_image_warp
from max3.src.draw_difference_map import draw_difference_map
from max3.src.utils_list import save_list_of_peaks_txt


def calc(image: np.uint8, templ: np.uint8) -> (float, float):

    image_magn_roi = get_magn_roi(image)
    image_magn_half = get_magn_half(image_magn_roi)
    image_list_of_peaks = get_peaks(image_magn_half)
    image_table, n_image_table_rows = create_table(image_list_of_peaks)

    if n_image_table_rows == 0:
        print(f'\ncalc_similarity ERROR: ' + cfg_max3.path_image + ' - unacceptable shape')
        sys.exit(1)

    if cfg_max3.debug_mode:
        draw_magn('image', image_magn_roi)
        draw_peaks('image', image_list_of_peaks)
        save_list_of_peaks_txt('image_list_of_peaks', image_list_of_peaks)

    templ_magn_roi = get_magn_roi(templ)
    templ_magn_half = get_magn_half(templ_magn_roi)
    templ_list_of_peaks = get_peaks(templ_magn_half)
    templ_table, n_templ_table_rows = create_table(templ_list_of_peaks)

    if n_templ_table_rows == 0:
        print(f'\ncalc_similarity ERROR: ' + cfg_max3.path_templ + ' - unacceptable shape')
        sys.exit(1)

    if cfg_max3.debug_mode:
        draw_magn('templ', templ_magn_roi)
        draw_peaks('templ', templ_list_of_peaks)
        save_list_of_peaks_txt('templ_list_of_peaks', templ_list_of_peaks)

    joint_table, n_joint_table_rows = \
        create_joint_table(image_table, n_image_table_rows,
                           templ_table, n_templ_table_rows)

    if n_joint_table_rows == 0:
        print(f"\nERROR: " + cfg_max3.path_image + "  vs.  " + cfg_max3.path_templ + " - we can't compare")
        sys.exit(1)

    distance, similarity = calc_cont(
                                image_magn_roi, templ_magn_roi,
                                joint_table, n_joint_table_rows)

    return distance, similarity


def calc_cont(
        image_magn_roi, templ_magn_roi,
        joint_table, joint_table_rows) -> (float, float):

    distance_result: float = float(1000000000)
    similarity_result: float = float(0)
    difference_map_current: np.float32 = np.float32(0)
    difference_map_result: np.float32 = np.float32(0)

    for n in range(joint_table_rows):

        y_image_blue = joint_table[n, 0]
        x_image_blue = joint_table[n, 1]
        y_image_red = joint_table[n, 2]
        x_image_red = joint_table[n, 3]

        y_templ_blue = joint_table[n, 4]
        x_templ_blue = joint_table[n, 5]
        y_templ_red = joint_table[n, 6]
        x_templ_red = joint_table[n, 7]

        pts_image = np.float32([[x_image_blue, y_image_blue],
                                [x_image_red, y_image_red],
                                [cfg_max3.X0, cfg_max3.Y0]])

        pts_templ = np.float32([[x_templ_blue, y_templ_blue],
                                [x_templ_red, y_templ_red],
                                [cfg_max3.X0, cfg_max3.Y0]])

        mat_affine = cv.getAffineTransform(pts_image, pts_templ)
        dsize = (cfg_max3.size_roi, cfg_max3.size_roi)

        image_magn_roi_warp = cv.warpAffine(image_magn_roi, mat_affine, dsize)

        if cfg_max3.debug_mode:
            distance_current, similarity_current, difference_map_current \
                                    = calc_cont2_map(
                                            np.float32(image_magn_roi_warp),
                                            np.float32(templ_magn_roi))
        else:
            distance_current, similarity_current \
                                    = calc_cont2(
                                            np.float32(image_magn_roi_warp),
                                            np.float32(templ_magn_roi))

        if distance_current < distance_result:
            distance_result = distance_current
            similarity_result = similarity_current

            if cfg_max3.debug_mode:
                difference_map_result = difference_map_current.copy()

                cfg_max3.y_image_blue = y_image_blue
                cfg_max3.x_image_blue = x_image_blue
                cfg_max3.y_image_red = y_image_red
                cfg_max3.x_image_red = x_image_red

                cfg_max3.y_templ_blue = y_templ_blue
                cfg_max3.x_templ_blue = x_templ_blue
                cfg_max3.y_templ_red = y_templ_red
                cfg_max3.x_templ_red = x_templ_red

    if cfg_max3.debug_mode:
        draw_result('image')
        draw_result('templ')
        draw_image_warp()
        draw_difference_map(difference_map_result)

    return distance_result, similarity_result


def calc_cont2_map(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> (float, float, np.float32):

    arr_zero = np.zeros(cfg_max3.dsize_roi, dtype=np.float32)
    arr_1 = np.maximum(magnitude_1, arr_zero)
    arr_2 = np.maximum(magnitude_2, arr_zero)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    difference_map = np.subtract(arr_max, arr_min, where=arr_min > 0)
    nonzero_count = np.count_nonzero(difference_map)

    if nonzero_count == 0:
        distance = 0.0
        similarity = 1.0
    else:
        distance = np.sum(difference_map) / nonzero_count
        similarity = 1.0 / (1.0 + cfg_max3.param_similarity * distance)

    return distance, similarity, difference_map


def calc_cont2(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> (float, float):

    arr_zero = np.zeros(cfg_max3.dsize_roi, dtype=np.float32)
    arr_1 = np.maximum(magnitude_1, arr_zero)
    arr_2 = np.maximum(magnitude_2, arr_zero)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    difference_map = np.subtract(arr_max, arr_min, where=arr_min > 0)
    nonzero_count = np.count_nonzero(difference_map)

    if nonzero_count == 0:
        distance = 0.0
        similarity = 1.0
    else:
        distance = np.sum(difference_map) / nonzero_count
        similarity = 1.0 / (1.0 + cfg_max3.param_similarity * distance)

    return distance, similarity
