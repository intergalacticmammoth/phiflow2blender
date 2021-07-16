from phi.flow import *
from phi._troubleshoot import count_tensors_in_memory

# Params
RES = 32
T_STEP = 1
DOMAIN = dict(x=RES, y=RES, z=RES)

# The center's coordinates are in relation to the BOX not the resolution.
INFLOW = CenteredGrid(Sphere(center=(8, 8, 8), radius=2), extrapolation.BOUNDARY, **DOMAIN) * 0.2
velocity = StaggeredGrid(Noise(scale=1), extrapolation.ZERO, **DOMAIN)  # or use CenteredGrid
smoke = CenteredGrid(0, extrapolation.BOUNDARY, **DOMAIN)

total_time = 0

# with backend.profile(save='smoke-3D.json'):
count_tensors_in_memory()
print("Advecting smoke")
smoke = advect.mac_cormack(smoke, velocity, dt=T_STEP) + INFLOW
count_tensors_in_memory()
print("Adding buoyancy")
buoyancy_force = smoke * (0.1, 0, 0) >> velocity  # resamples smoke to velocity sample points
count_tensors_in_memory()
print("Advecting velocity")
velocity = advect.semi_lagrangian(velocity, velocity, 1) + buoyancy_force
count_tensors_in_memory()
print("Projecting")
with math.SolveTape() as solves:
    velocity, pressure = fluid.make_incompressible(velocity, (), Solve('CG-adaptive', 1e-5, 0, x0=None))
count_tensors_in_memory()
print(f"Solve time: {solves[0].solve_time} sec")
