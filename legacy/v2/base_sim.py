

#phi.verify()

import sys
if 'tf' in sys.argv:
    from phi.tf.flow import *
    MODE = 'TensorFlow'
elif 'torch' in sys.argv:
    from phi.torch.flow import *
    MODE = 'PyTorch'
else:
    from phi.flow import *  # Use NumPy
    MODE = 'NumPy'

import phi
import matplotlib.pyplot as plt
from phi.field.plt import plot

res = 32
radius = 8

DOMAIN = Domain(x=3*res, y=2*res, boundaries = CLOSED, bounds=Box[0:300, 0:200])

INFLOW = DOMAIN.scalar_grid(Sphere(center=(75 , 25), radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=(150, 25), radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=(225, 25), radius=radius))

smoke = DOMAIN.scalar_grid(0)
velocity = DOMAIN.staggered_grid(0)

step = 0

#for _ in range(5):
for _ in ModuleViewer(display=('smoke', 'velocity')).range():
    smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
    buoyancy_force = smoke * (0, 0.5) >> velocity #resamples smoke to velocity sample points
    velocity = advect.semi_lagrangian(velocity, velocity, dt=1) + buoyancy_force
    velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)
    step+=1
    print('Solving step ', step)

#plot(smoke, title='Smoke')
#plt.show()

print(field.mean(smoke))
