import numpy as np
import json


data_file = "5D.txt"
def data_file_reading(data_file):
    data = np.genfromtxt(data_file, names=True, dtype=None, encoding=None)
    row = len(data)
    column = len(data.dtype.names)

    data_dictionary_shape = {}

    for column_label in data.dtype.names:
        array = data[column_label]
        data_list = array.tolist()
        data_dictionary_shape[column_label] = data_list


    if column <= 5:
        print(f"Successfully uploaded {column} column(s) and {row} row(s)")
    else:
        print(f"ERROR: The data uploaded has more than 5 columns")


    return data_dictionary_shape

# print(json.dumps(data_file_reading(data_file))) # Strictly OPTIONAL for visualizing data.

data_file_reading(data_file)