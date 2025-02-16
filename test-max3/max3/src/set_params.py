# Feb-13-2025
# sey_params.py

from max3.src import cfg_max3


def set_params(n_peaks: int, canonical_size: int, cutoff: float):

    cfg_max3.n_peaks = n_peaks
    cfg_max3.canonical_size = canonical_size
    cfg_max3.cutoff = cutoff

    cfg_max3.size_dft = 2048
    temp = int(cfg_max3.size_dft * cfg_max3.cutoff)
    if temp % 2:
        cfg_max3.size_roi = temp - 1
    else:
        cfg_max3.size_roi = temp

    cfg_max3.dsize_roi = (cfg_max3.size_roi, cfg_max3.size_roi)
    cfg_max3.size_roi_half = cfg_max3.size_roi // 2
    cfg_max3.X0 = cfg_max3.size_roi_half
    cfg_max3.Y0 = cfg_max3.size_roi_half
    cfg_max3.center = (cfg_max3.X0, cfg_max3.Y0)
