##############################################
# Example of a 3D fluid simulation with phiflow - https://github.com/tum-pbs/PhiFlow
# It creates a simple plume.
# Author: Aristotelis
# Date: 02 Aug 2021
#############################################
from phi.flow import *
import time

#Params
RES = 32
RADIUS = 2
T_STEP = 1
DOMAIN = dict(x=RES, y=RES, z=RES)
NUM_FRAMES = 250

#choose where to save the resulting frames
SCENE_PATH = "/home/teemps/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/tum-logo/tutorial/test"
scene = Scene(SCENE_PATH)

#The center's coordinates are in relation to the BOX not the resolution.
INFLOW = CenteredGrid(Sphere(center=(8, 16, 16), radius=RADIUS), extrapolation.BOUNDARY, **DOMAIN) * 0.2
velocity = StaggeredGrid(Noise(scale=1), extrapolation.ZERO, **DOMAIN)  # or use CenteredGrid
smoke = CenteredGrid(0, extrapolation.BOUNDARY, **DOMAIN)

total_time = 0

#Time stepping
for step in range(NUM_FRAMES):

    start = time.time()
    smoke = advect.mac_cormack(smoke, velocity, dt=T_STEP) + INFLOW
    buoyancy_force = smoke * (0.1, 0, 0) >> velocity  # resamples smoke to velocity sample points
    velocity = advect.semi_lagrangian(velocity, velocity, 1) + buoyancy_force
    with math.SolveTape() as solves:
        velocity, pressure = fluid.make_incompressible(velocity, (), Solve('CG-adaptive', 1e-5, 0, x0=None))
    scene.write({'smoke': smoke, 'velocity': velocity}, frame = step )
    end = time.time()

    total_time += end-start
    print(f'Step {step}:\t {end-start}seconds \tTotal time:{total_time}')