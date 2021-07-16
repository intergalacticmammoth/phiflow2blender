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
import imageio

res = 32
radius = 4

DOMAIN = Domain(x=3*res, y=2*res, boundaries = CLOSED, bounds=Box[0:300, 0:200])

INFLOW_LOCATIONS = [(75, 25), (150, 25), (225, 25)]
INFLOW = DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[0], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[1], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[2], radius=radius))

smoke = DOMAIN.scalar_grid(0)
velocity = inc_velocity = DOMAIN.staggered_grid(Noise())

#target = imageio.imread('tum_32.png')
#target = np.transpose(target[:,:,1])
#target = DOMAIN.scalar_grid(target)

import PIL

img = PIL.Image.open('tum_32.png')
img = np.asarray(img, dtype=np.float32)
img = img[:,:,1]
norm = np.linalg.norm(img)
img = img/norm
img = math.tensor(img, names='y, x')

#target = imageio.imread('tum_32.png')
#target = target[:,:,0]
#target = np.flip(target)
#target = target[:,::-1]
#target = math.tensor(target, names='y, x')
#target = math.cast(target, math.DType(float, 32))
target = DOMAIN.scalar_grid(img)
print(type(target.values.native()))

step = 0

for _ in range(50):
    with math.record_gradients(velocity.values):
        smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
        buoyancy_force = smoke * (0, 0.5) >> velocity
        velocity = advect.semi_lagrangian(velocity, velocity, dt=1) * buoyancy_force
        velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)
        loss = field.l2_loss(smoke - target)
        grad = math.gradients(loss)
        step+=1
        print('Solving step: ', step, '\tloss: ', loss)

    velocity -= DOMAIN.staggered_grid(grad)

fig, axes = plot(smoke, title='Smoke')
plt.show()
