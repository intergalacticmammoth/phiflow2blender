from phi.flow import *
import time

#Params
RES = 32
RADIUS = 2
T_STEP = 1
DOMAIN = dict(x=RES, y=RES, z=RES)

SCENE_PATH = "/home/teemps/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/tum-logo/tutorial/test"
scene = Scene(SCENE_PATH)

#The center's coordinates are in relation to the BOX not the resolution.
INFLOW = CenteredGrid(Sphere(center=(8, 8, 8), radius=RADIUS), extrapolation.BOUNDARY, **DOMAIN) * 0.2
velocity = StaggeredGrid(Noise(scale=1), extrapolation.ZERO, **DOMAIN)  # or use CenteredGrid
smoke = CenteredGrid(0, extrapolation.BOUNDARY, **DOMAIN)

total_time = 0

#Time stepping
# for step in view(smoke, velocity, play=False).range(warmup=1):
for step in range(50):

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