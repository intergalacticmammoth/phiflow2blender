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
radius = 8

# Create domain
DOMAIN = Domain(x=3*res, y=2*res, boundaries = OPEN, bounds=Box[0:300, 0:200])

# Create inflows
INFLOW = DOMAIN.scalar_grid(Sphere(center=(75, 25), radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=(150, 25), radius=radius)) + \
         DOMAIN.scalar_grid(Sphere(center=(225, 25), radius=radius))


# Create smoke and velocity fields
smoke = DOMAIN.scalar_grid(0)
pred_smoke = DOMAIN.scalar_grid(0)
velocity = DOMAIN.staggered_grid(0)

# Set up the smoke target
img = PIL.Image.open('tum_32.png')
img = np.asarray(img, dtype=np.float32)
img = img[:,:,1]
img = np.flip(img, axis=0)
norm = np.linalg.norm(img)
img = 100*img/norm
img = math.tensor(img, names='y, x')
target = DOMAIN.scalar_grid(img)

# Check its read as a torch tensor
print(type(target.values.native()))

step = 0

def simulate( smoke: CenteredGrid, velocity: StaggeredGrid):
    for _ in range(5):
        smoke = advect.mac_cormack(smoke, velocity, dt=1) + INFLOW
        buoyancy_force = smoke * (0, 0.5) >> velocity
        velocity = advect.semi_lagrangian(velocity, velocity, dt=1) + buoyancy_force
        velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)

    loss = field.l2_loss(diffuse.explicit(smoke - target, 1, 1, 10))
    return loss, smoke, velocity

initial_smoke = DOMAIN.scalar_grid(math.zeros(inflow_loc=1))
initial_velocity = DOMAIN.staggered_grid(0) * math.ones(inflow_loc=1)

sim_grad = field.functional_gradient(simulate, wrt=[1], get_output=True)

#for opt_step in range(10):
for _ in ModuleViewer().range():
    loss, sm, vel, vel_grad  = sim_grad(initial_smoke, initial_velocity)
    #print(f"Optimization step: {opt_step}, loss: {loss}")
    initial_velocity -= -0.01 * vel_grad
    #plot(vel_grad)
    #plt.savefig(f"field_plots/vel_grad_{opt_step}.png")
    #plot(sm)
    #plt.savefig(f"field_plots/sm_{opt_step}.png")
    #plt.close('all')


success, initial_velocity, iterations = field.minimize(lambda v: simulate(initial_smoke, v)[0], initial_velocity, math.Solve('L-BFGS-B', 0, 1e-3, max_iterations=20))
plot(initial_velocity)
plt.savefig("init_vel.png")

for step in range(5):
    simulate(initial_smoke, initial_velocity)

plot(initial_smoke)
plt.savefig("smoke.png")
    


# Check result
#fig, axes = plot(smoke, title='Smoke')
#plt.show()
