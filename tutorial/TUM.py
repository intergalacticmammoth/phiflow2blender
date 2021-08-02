from phi.flow import *
import time 

RES = 32
RADIUS = 2
T_STEP = 1
DOMAIN = dict(x=2*RES, y=RES, z=3*RES)

SCENE_PATH = "/home/teemps/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/tum-logo/tutorial/TUM"
scene = Scene(SCENE_PATH)


OBSTACLE_GEOMETRIES = [
    Box[0:20*  RES           , 0:RES, 0.00     :0.20*  RES],
    Box[0:20*  RES           , 0:RES, 2.80* RES:3.00*  RES],
    Box[0:1.45*RES           , 0:RES, 0.20* RES:0.43*  RES],
    Box[0:0.30*RES           , 0:RES, 0.66* RES:2.56*  RES],
    Box[1.70*  RES:2*     RES, 0:RES, 0.20* RES:2.80*  RES],
    Box[0.30*  RES:1.45*  RES, 0:RES, 0.66* RES:0.90*  RES],
    Box[0.30*  RES:1.45*  RES, 0:RES, 1.70* RES:1.97*  RES],
    Box[0.30*  RES:1.45*  RES, 0:RES, 2.30* RES:2.55*  RES],
    Box[0.55*  RES:1.7*   RES, 0:RES, 1.15* RES:1.42*  RES]
]
OBSTACLE = Obstacle(union(OBSTACLE_GEOMETRIES))
OBSTACLE_MASK = HardGeometryMask(OBSTACLE.geometry) >> CenteredGrid(0, extrapolation.BOUNDARY, **DOMAIN)


INFLOW = CenteredGrid(Box[0.31*RES:0.45*RES, 0.35*RES:0.75*RES, 0.5* RES:0.65*RES ], extrapolation.BOUNDARY, **DOMAIN) * 0.2 + \
         CenteredGrid(Box[0.31*RES:0.45*RES, 0.35*RES:0.75*RES, 1.1* RES:1.5* RES ], extrapolation.BOUNDARY, **DOMAIN) * 0.2 + \
         CenteredGrid(Box[0.31*RES:0.45*RES, 0.35*RES:0.75*RES, 2.05*RES:2.2* RES ], extrapolation.BOUNDARY, **DOMAIN) * 0.2 + \
         CenteredGrid(Box[0.31*RES:0.45*RES, 0.35*RES:0.75*RES, 2.6* RES:2.75*RES ], extrapolation.BOUNDARY, **DOMAIN) * 0.2
velocity = StaggeredGrid(Noise(scale=1), extrapolation.ZERO, **DOMAIN)  # or use CenteredGrid
smoke = CenteredGrid(0, extrapolation.BOUNDARY, **DOMAIN)

total_time = 0

for step in range(500):

    start = time.time()
    smoke = advect.mac_cormack(smoke, velocity, dt=T_STEP) + INFLOW
    buoyancy_force = smoke * (0.1, 0, 0) >> velocity  # resamples smoke to velocity sample points
    velocity = advect.semi_lagrangian(velocity, velocity, 1) + buoyancy_force
    with math.SolveTape() as solves:
        velocity, pressure = fluid.make_incompressible(velocity, (OBSTACLE,), Solve('CG-adaptive', 1e-5, 0, x0=None))
    scene.write({'smoke': smoke, 'velocity': velocity}, frame = step )
    end = time.time()

    total_time += end-start
    print(f'Step {step}:\t {end-start}seconds \tTotal time:{total_time}')