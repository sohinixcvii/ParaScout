from itertools import combinations

import numpy as np
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from generating_test_data_module import (
    all_data,  # it will be replacing output of load_data function.
)

dim = "3D"
all_data = {dim: all_data[dim]}  # Keep only the data for the specified dimension for testing purposes.

# TODO: add a function to create dictionary with a label of dimension regardless of what type of data comes as a input. For example, if the input is a dictionary with keys "1D", "2D", "3D", etc., the function should return a new dictionary with the same keys and values. If the input is a list of tuples, the function should return a dictionary with keys "1D", "2D", "3D", etc., and values as lists of tuples. If the input is a single tuple, the function should return a dictionary with key "1D" and value as a list containing that tuple.


for n in range(1, 6):
    if f"{n}D" in all_data:
        print(f"The file has {n}D data with labels: {all_data[f'{n}D'][0]}")


def make_column_combinations(labels, columns, max_dimension=3):
    # This dictionary will keep the results grouped as "1D", "2D", "3D", etc.
    grouped_combinations = {}

    # We cannot make a combination larger than the number of available columns.
    number_of_columns = len(labels)
    largest_dimension = min(max_dimension, number_of_columns)

    # Start from single columns, then pairs, then triples.
    for dimension in range(1, largest_dimension + 1):
        dimension_name = f"{dimension}D"
        grouped_combinations[dimension_name] = []

        # Example for 3 columns and dimension=2: (0, 1), (0, 2), (1, 2)
        column_index_combinations = combinations(range(number_of_columns), dimension)

        print(f"\nProcessing {dimension_name} combinations for labels: {labels}")  # Debugging: print the current dimension and labels
        for column_indices in column_index_combinations:
            # print("column_indices:", column_indices)  # Debugging: print the current combination of indices
            selected_labels = []
            selected_columns = []

            # Collect the labels and data columns for this specific combination.
            for index in column_indices:
                selected_labels.append(labels[index])
                selected_columns.append(columns[index])

            print("selected_labels:", selected_labels)  # Debugging: print the selected labels for this combination
            grouped_combinations[dimension_name].append((selected_labels, selected_columns))

    return grouped_combinations


def make_all_column_combinations(all_data, max_dimension=3):
    all_combinations = {}

    # Repeat the same combination process for 1D.txt, 2D.txt, ..., 5D.txt.
    for data_name, data_values in all_data.items():
        labels = data_values[0]
        columns = data_values[1]

        all_combinations[data_name] = make_column_combinations(
            labels,
            columns,
            max_dimension=max_dimension,
        )

    return all_combinations


all_combinations = make_all_column_combinations(all_data, max_dimension=3)
