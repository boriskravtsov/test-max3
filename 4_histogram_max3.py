# Mar-08-2025
# 4_histogram_max3.py

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

hist_title = 'max3:  4-pointed stars  &  5-pointed stars'

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

        similarity = float(list_temp[3])

        arr_match[n] = similarity
        n += 1

    if not line:
        break

file_in.close()

arr_match_max = arr_match.max()
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

        similarity = float(list_temp[3])

        arr_mismatch[n] = similarity
        n += 1

    if not line:
        break

file_in.close()

arr_mismatch_min = arr_mismatch.min()
# -------------------------------------------------------------

#   H I S T O G R A M
# -------------------------------------------------------------
# plt.figure(figsize=(5.0, 4.0), dpi=100)
# plt.figure(figsize=(7.0, 5.0), dpi=100)
plt.figure(figsize=(8.0, 5.0), dpi=100)

bins = np.linspace(arr_mismatch_min, arr_match_max, 24)

plt.title(hist_title, fontsize=12)

plt.hist([arr_mismatch, arr_match], bins, label=['mismatch', 'match'])

plt.xlabel('Similarity', fontsize=10)
plt.ylabel('Frequency', fontsize=10)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.legend(loc='upper right')

path_hist = '__RESULTS_max3/HISTOGRAM_max3.png'
plt.savefig(path_hist, dpi=150)
# -------------------------------------------------------------

print(f'\nDone')
