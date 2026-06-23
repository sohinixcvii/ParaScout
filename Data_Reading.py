import numpy as np


def data_file_reading():
    data = np.genfromtxt("5D.txt", names=True)
    row = len(data)
    column = len(data[0])

    if column <= 5:
        print(f"Successfully uploaded {column} column(s) and {row} row(s)")
    else:
        print(f"ERROR: The data uploaded has more than 5 columns")

data_file_reading()