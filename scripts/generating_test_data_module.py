from pathlib import Path

import numpy as np

base = Path(__file__).parent.parent / "test_data_multi_dimension"


def read_txt_with_labels(path):
    labels = np.loadtxt(path, max_rows=1, dtype=str)
    labels = np.atleast_1d(labels).tolist()

    data = np.loadtxt(path, skiprows=1, ndmin=2)

    columns = data.T.tolist()

    return labels, columns


all_data = {}

for n in range(1, 6):
    labels, columns = read_txt_with_labels(base / f"{n}D.txt")
    all_data[f"{n}D"] = (labels, columns)

# store only first 5 row of data for each dimension and delete the rest to save space
for n in range(1, 6):
    all_data[f"{n}D"] = (all_data[f"{n}D"][0], [col[:5] for col in all_data[f"{n}D"][1]])
