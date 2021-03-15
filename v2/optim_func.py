'''
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
'''
from phi.torch.flow import *
import PIL
import matplotlib.pyplot as plt
from phi.field.plt import plot

# Simulation Parameters
res = 32
radius = 4

# Create domain
DOMAIN = Domain(x=3*res, y=2*res, boundaries = OPEN, bounds=Box[0:300, 0:200])

# Create inflows
INFLOW_LOCATIONS = [(75, 25), (150, 25), (225, 25)]
INFLOW = DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[0], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[1], radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=INFLOW_LOCATIONS[2], radius=radius))


# Create smoke and velocity fields
smoke = DOMAIN.scalar_grid(0)
pred_smoke = DOMAIN.scalar_grid(0)
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

#step = 0

def simulate( smoke: CenteredGrid, velocity: StaggeredGrid):
    step = 0
    for _ in range(50):
        smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
        buoyancy_force = smoke * (0, 0.5) >> velocity
        velocity = advect.semi_lagrangian(velocity, velocity, dt=1) * buoyancy_force
        velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)
        step+=1
        print('Solving step: ', step)

    loss = field.l2_loss(diffuse.explicit(smoke - target, 1, 1, 10))
    print('Loss: ', loss)

    return loss, smoke, velocity

initial_smoke = DOMAIN.scalar_grid(math.zeros(inflow_loc=1))
initial_velocity = DOMAIN.staggered_grid(0) * math.ones(inflow_loc=1)

sim_grad = field.functional_gradient(simulate, wrt=[1], get_output=True)

loss, sm, vel, vel_grad  = sim_grad(initial_smoke, initial_velocity)


plot(sm)
plt.show()

plot(vel)
plt.show()

plot(vel_grad)
plt.show()


# Check result
#fig, axes = plot(smoke, title='Smoke')
#plt.show()
