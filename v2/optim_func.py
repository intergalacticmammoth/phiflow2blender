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

import PIL
import matplotlib.pyplot as plt
from phi.field.plt import plot
import imageio

# Simulation Parameters
res = 32
radius = 4

# Create domain
DOMAIN = Domain(x=3*res, y=2*res, boundaries = CLOSED, bounds=Box[0:300, 0:200])

# Create inflows
INFLOW_LOCATIONS = [(75, 25), (150, 25), (225, 25)]
INFLOW = DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[0], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[1], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[2], radius=radius))

# Create smoke and velocity fields
smoke = DOMAIN.scalar_grid(0)
velocity = DOMAIN.staggered_grid(Noise())

# Set up the smoke target
img = PIL.Image.open('tum_32.png')
img = np.asarray(img, dtype=np.float32)
img = img[:,:,1]
norm = np.linalg.norm(img)
img = 100*img/norm
img = math.tensor(img, names='y, x')
target = DOMAIN.scalar_grid(img)

# Check its read as a torch tensor
print(type(target.values.native()))

step = 0

# Simulate and optimize
for _ in range(100):
    with math.record_gradients(velocity.values):
        smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
        buoyancy_force = smoke * (0, 0.5) >> velocity
        velocity = advect.semi_lagrangian(velocity, velocity, dt=1) * buoyancy_force
        velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)
        loss = field.l2_loss(diffuse.explicit(smoke - target, 1, 1, 10))
        grad = math.gradients(loss)
        step+=1
        print('Solving step: ', step, '\tloss: ', loss)

    velocity -= DOMAIN.staggered_grid(grad)

# Check result
fig, axes = plot(smoke, title='Smoke')
plt.show()
