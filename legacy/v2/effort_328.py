from numpy.lib.function_base import gradient
from phi.torch.flow import *
import PIL
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from phi.field.plt import plot, animate


# Simulation Parameters
res = 8
radius = 20

DOMAIN = Domain(x=3*res, y=2*res, boundaries = OPEN, bounds=Box[0:300, 0:200])

INFLOW = DOMAIN.scalar_grid(Sphere(center=(75 , 35), radius=radius))*0.25 + \
         DOMAIN.scalar_grid(Sphere(center=(150, 35), radius=radius))*0.25 + \
         DOMAIN.scalar_grid(Sphere(center=(225, 35), radius=radius))*0.25

smoke = INFLOW


# Set up the smoke target
img = PIL.Image.open('tum_08.png')
img = np.asarray(img, dtype=np.float32)
img = img[:,:,1]
img = np.flip(img, axis=0)
norm = np.linalg.norm(img)
img = 500*img/norm
img = math.tensor(img, names='y, x')
target = DOMAIN.scalar_grid(img)

def loss(velocity, smoke):
    advected = advect.mac_cormack(smoke, velocity, dt=1.0) + INFLOW
    buoyancy_force = advected * (0, 0.5) >> velocity #resamples smoke to velocity sample points
    velocity = advect.semi_lagrangian(velocity, velocity, dt=1) + buoyancy_force
    velocity, _, _, _ = fluid.make_incompressible(velocity, DOMAIN)
    smooth_diff = diffuse.explicit(advected - target, 0.1, 1, 20)
    return field.l2_loss(smooth_diff), advected, smooth_diff

gradient_function = field.functional_gradient(loss, get_output=True)

velocity_fit = DOMAIN.staggered_grid(0)
smoke_fit = smoke
smooth_difference = DOMAIN.staggered_grid(0)
grad = DOMAIN.staggered_grid(0)
grad_x = grad.x
grad_y = grad.y
vel_x = velocity_fit.x
vel_y = velocity_fit.y
app = ModuleViewer(display=['marker_fit', 'gradient'])

'''
for _ in app.range(warmup=1):
    for _ in range(10):
        loss, smoke_fit, smooth_difference, grad = gradient_function(velocity_fit, smoke)
    smoke = smoke_fit
    app.info(f"Loss = {loss:.2f}")
    app.log_scalar('loss', loss)
    velocity_fit -= grad
'''
for _ in app.range(warmup=1):
    for _ in range(10):
        loss, smoke_fit, smooth_difference, grad = gradient_function(velocity_fit, smoke)
    smoke = smoke_fit
    app.info(f"Loss = {loss:.2f}")
    app.log_scalar('loss', loss)
    velocity_fit -= grad
    vel_x = velocity_fit.x
    grad_x = grad.x
    vel_y = velocity_fit.y
    grad_y = grad.y


'''    
smokes = []
for opt_step in range(15):
    for _ in range(5):
        loss, smoke_fit, smooth_difference, grad = gradient_function(velocity_fit, smoke)
    smoke = smoke_fit
    smokes.append(smoke_fit)
    
    #plt.plot(smoke_fit)
    #plt.savefig(f"field_plots/contagion_{opt_step}")
    #plt.close()
    print(f"Optimization step: {opt_step}, loss: {loss}")

anim = animate(smokes)
writer = animation.FFMpegWriter(fps=24)
anim.save('contagious_fungi.mp4', writer = writer)
plt.close()
'''