import numpy #type: ignore
import pandas # type: ignore

from enviornment_variables import csv_file, npy_temp_name

# Use SQLite instead of just saved numpy arrays
# Review this for ideas - https://www.w3resource.com/python-exercises/numpy/write-a-numpy-array-to-a-sqlite-database-and-read-it-back.php
try:
    old_data = numpy.load(f'{npy_temp_name}.npy')
except:
    old_data = None
    print(f'There is no original {npy_temp_name} npy file')

try:
    # We will not need the first 2 lines within the csv file
    header = 1
    if old_data:
        old_size = old_data.size
        raw_data = pandas.read_csv(csv_file,header=old_size+header).values
    else:
        raw_data = pandas.read_csv(csv_file,header=header).values
    print(raw_data.shape)
    print(raw_data[0])
    # numpy.save(npy_temp_name,data)
    print('Saved new data.')
except:
    print('There is no data to mine with the necessary information!')