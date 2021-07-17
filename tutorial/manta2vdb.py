import os
from argparse import ArgumentParser
import numpy as np
from pathlib import Path

# parse args
parser = ArgumentParser()
parser.add_argument(
    "-d", "--directory", required=True, help="input directory for processing"
)
parser.add_argument(
    "-res",
    "--resolution",
    nargs="+",
    required=True,
    help="X Y Z resolution of the phiflow simulation",
)

args = parser.parse_args()


#initialize mantaflow fields
res = [int(x) for x in args.resolution]

if len(res) != 3:
    raise ValueError("Expected 3 resolution values: X Y Z")

gs = [res[2], res[1], res[0]]
s = FluidSolver(name="low-res", gridSize=vec3(gs[2], gs[1], gs[0]), dim=3)

# prepare grids
gV = s.create(MACGrid)
gD = s.create(RealGrid)
vort = s.create(VecGrid)
vortn = s.create(RealGrid)

# input / output
input_dir = Path(args.directory)

if not input_dir.exists():
    raise ValueError(f"{input_dir} does not exist, choose a sim that exists.")

output_dir = input_dir/'to_vdb/'
output_dir.mkdir(parents=True, exist_ok=True)



# Find all smoke and velocity files in input directory
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

# save velocity and vorticity to OpenVDB
for file_name in vel_files:
    data = np.load(file_name)["data"]
    data = data[:-1:, :-1, :-1, ::]  # crop, and flip XYZ vel channels again!

    copyArrayToGridMAC(target=gV, source=data)
    computeVorticity(gV, vort, vortn)

    vn = np.zeros(shape=(gs[0], gs[1], gs[2], 1), dtype=np.float32)
    copyGridToArrayReal(target=vn, source=vortn)
    copyArrayToGridReal(target=vortn, source=vn)

    # write vdb file
    gV.save(output_dir.__str__() + f"/{file_name.split('.')[0].rsplit('/')[-1]}.vdb")
    vortn.save(output_dir.__str__() + f"/{file_name.split('.')[0].rsplit('/')[-1]}.vdb".replace("velocity", "vorticity"))

# save smoke to OpenVDB
for file_name in smoke_files:
    data = np.load(file_name)["data"]

    copyArrayToGridReal(target=gD, source=data)
    gD.save(output_dir.__str__() + f"/{file_name.split('.')[0].rsplit('/')[-1]}.vdb")
    


print(f"\n\nThe files are saved in:\n {output_dir}")
