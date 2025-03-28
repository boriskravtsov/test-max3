# Mar-08-2025
# draw_canonical.py

import cv2 as cv
from pathlib import Path

from max3.src import cfg_max3


def draw_canonical(image, templ):

    canon_image_name = 'canon_' + cfg_max3.image_name
    canon_templ_name = 'canon_' + cfg_max3.templ_name

    path_image_canon = str(Path.cwd() / cfg_max3.dir_debug / canon_image_name)
    path_templ_canon = str(Path.cwd() / cfg_max3.dir_debug / canon_templ_name)

    cv.imwrite(path_image_canon, image)
    cv.imwrite(path_templ_canon, templ)
