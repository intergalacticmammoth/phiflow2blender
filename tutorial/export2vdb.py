import os
from argparse import ArgumentParser
import numpy as np
from phi.flow import *
from manta  import *

########################
# ----Argument Parser----
########################

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
parser.add_argument(
    "-o", "--output", required=True, help="output directory for vdb files"
)

args = parser.parse_args()


########################
# ----Mantaflow Setup----
########################

params = {
    "dim": 3,
    "len": 100,
}

res = [int(x) for x in args.resolution]

if len(res) != 3:
    raise ValueError("Expected 3 resolution values: X Y Z")

gs = [res[2], res[1], res[0]]
s = FluidSolver(name="low-res", gridSize=vec3(gs[2], gs[1], gs[0]), dim=params["dim"])

# prepare grids
gF = s.create(FlagGrid)
gV = s.create(MACGrid)
gD = s.create(RealGrid)
vort = s.create(VecGrid)
vortn = s.create(RealGrid)

gF.initDomain()
gF.fillGrid()


######################
# ----Output Setup-----
######################

input_dir = args.directory
output_dir = input_dir + "post_process/"

if not os.path.exists(input_dir):
    raise ValueError(f"{input_dir} does not exist, choose a sim that exists.")

if args.output is not None:
    output_dir = args.output + "/"

save_dir = output_dir + "data/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

################################
# ---- Save .npz to OpenVDB format ----
################################

path = input_dir
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

for fn in vel_files:
    print("Reading " + fn)
    a = np.load(fn)["data"]
    b = a[:-1:, :-1, :-1, ::]  # crop, and flip XYZ vel channels again!

    copyArrayToGridMAC(target=gV, source=b)
    computeVorticity(gV, vort, vortn)

    vn = np.zeros(shape=(gs[0], gs[1], gs[2], 1), dtype=np.float32)
    copyGridToArrayReal(target=vn, source=vortn)
    copyArrayToGridReal(target=vortn, source=vn)

    # write vdb file
    vortn.save(save_dir + f"{fn.split('.')[0]}.vdb")

print(f"\n\nThe .vdb files are saved in {save_dir}.")
