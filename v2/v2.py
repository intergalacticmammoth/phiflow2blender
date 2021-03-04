import phi
import matplotlib.pyplot as plt

from phi.torch.flow import *
from phi.field.plt import plot

#phi.verify()

res = 32
radius = 4

DOMAIN = Domain(x=3*res, y=2*res, boundaries = CLOSED, bounds=Box[0:300, 0:200])

INFLOW_LOCATIONS = [(75, 25), (150, 25), (225, 25)]
INFLOW = DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[0], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[1], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[2], radius=radius))

smoke = DOMAIN.scalar_grid(0)
velocity = DOMAIN.staggered_grid(Noise())
pressure = DOMAIN.scalar_grid(0)
divergence = DOMAIN.scalar_grid(0)
remaining_divergence = DOMAIN.scalar_grid(0)

step = 0

for _ in range(20):
    smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
    buoyancy_force = smoke * (0, 0.5) >> velocity #resamples smoke to velocity sample points
    velocity = advect.semi_lagrangian(velocity, velocity, dt=1) + buoyancy_force
    velocity, pressure, iterations, divergence = fluid.make_incompressible(velocity, DOMAIN, pressure_guess=pressure)
    remaining_divergence = field.divergence(velocity)
    step+=1
    print('Solving step ', step)

fig, axes = plot(smoke, title='Smoke')
plt.show()
