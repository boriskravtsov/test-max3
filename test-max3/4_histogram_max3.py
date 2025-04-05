# Apr-05-2025
# 4_histogram_max3.py

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

hist_title = 'max3:  3-pointed stars  &  4-pointed stars'

# File names
# -------------------------------------------------------------
path_match = Path.cwd() / '__RESULTS_max3' / 'result_match_max3.txt'
path_mismatch = Path.cwd() / '__RESULTS_max3' / 'result_mismatch_max3.txt'
# -------------------------------------------------------------

#   M A T C H
# -------------------------------------------------------------
line_count_match = len(open(path_match).readlines())

arr_match = np.zeros(line_count_match, dtype='float32')

file_in = open(path_match, 'r')

n = 0

while True:
    line_LF = file_in.readline()

    line = line_LF.strip()

    if line != '':
        list_temp = line.split('\t\t')

        distance = float(list_temp[3])

        arr_match[n] = distance
        n += 1

    if not line:
        break

file_in.close()

arr_match_min = arr_match.min()
# -------------------------------------------------------------

#   M I S M A T C H
# -------------------------------------------------------------
line_count_mismatch = len(open(path_mismatch).readlines())

arr_mismatch = np.zeros(line_count_mismatch, dtype='float32')

file_in = open(path_mismatch, 'r')

n = 0

while True:
    line_LF = file_in.readline()

    line = line_LF.strip()

    if line != '':
        list_temp = line.split('\t\t')

        distance = float(list_temp[3])

        arr_mismatch[n] = distance
        n += 1

    if not line:
        break

file_in.close()

arr_mismatch_max = arr_mismatch.max()
# -------------------------------------------------------------

#   H I S T O G R A M
# -------------------------------------------------------------
plt.figure(figsize=(8.0, 5.0), dpi=100)

bins = np.linspace(arr_match_min, arr_mismatch_max, 24)

plt.title(hist_title, fontsize=12)

plt.hist([arr_match, arr_mismatch], bins, label=['match', 'mismatch'])

plt.xlabel('Distance', fontsize=10)
plt.ylabel('Frequency', fontsize=10)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.legend(loc='upper right')

path_hist = '__RESULTS_max3/HISTOGRAM_max3.png'
plt.savefig(path_hist, dpi=150)
# -------------------------------------------------------------

print(f'\nDone')
