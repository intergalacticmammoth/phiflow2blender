import numpy as np
import openvdb as vdb
from argparse import ArgumentParser
import os


def numpy2vdb(data, vector=False):
    grid = vdb.FloatGrid

    if vector:
        grid = vdb.Vec3SGrid()

    grid.copyFromArray(data)

    return grid


def convert_sim_data(input_dir, output_dir):

    vel_files = []
    smoke_files = []

    for dirpath, dirnames, filenames in os.walk(input_dir):
        for file in filenames:
            if file.endswith(".npz"):
                full_data_file = os.path.join(dirpath, file)
                if "velocity" in file:
                    vel_files.append(full_data_file)
                if "smoke" in file:
                    smoke_files.append(full_data_file)

    for file in smoke_files:
        zipped = np.load(file)
        data = zipped["data"]

        vdb_data = numpy2vdb(data, vector=False)

        vdb.write(output_dir + f"{file.split('.')[0]}.vdb", grids=[vdb_data])


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-in", "--input", required=True, help="input directory for processing"
    )
    parser.add_argument(
        "-out", "--output", required=True, help="output directory for vdb files"
    )

    args = parser.parse_args()

    convert_sim_data(args.inp, args.out)

    # For debugging
    # input = '~/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/tum-logo/tutorial/test/'
    # output = '~/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/tum-logo/tutorial/test_vdb'
    # convert_sim_data(input, output)

if __name__ == "__main__":
    main()
