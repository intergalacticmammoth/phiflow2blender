from phi.tf.flow import *  # Causes deprecation warnings with TF 1.15
import pylab
import numpy as np
from .TUM_flow import TUM_flow

#Set parameters
params_08 = {'res': 8,
            'frames': 5,
            'optim_steps': 25
            }

#Initialize object and build graphs
flow_08 = TUM_flow(params_08)
flow_08.build_graphs()

#Set target, optimize
flow_08.set_target('tum/tum_08.png')
flow_08.train()

#Get optimized velocities and densities
optimized_vel_08 = flow_08.get_optimized_velocities()
densities_08 = flow_08.get_densities()

new_den = math.upsample2x(CenteredGrid(flow_08.fluid.density.data))

new_vtmp = math.upsample2x(flow_08.fluid.velocity.staggered_tensor())
new_vel = StaggeredGrid(new_vtmp)


#Set parameters for 2x res
params_16 = {'res': 16,
            'frames': 5,
            'optim_steps': 25
            }

flow_16 = TUM_flow(params_16)
flow_16.fluid = flow_16.fluid.copied_with(density = new_den, velocity = new_vel)
flow_16.build_graphs()

pylab.imshow(np.concatenate(flow_16.session.run(flow_16.states[5].density).data[...,0], axis=1), origin='lower', cmap='magma')
pylab.show()

flow_16.set_target('tum_16.png')
flow_16.train()
pylab.imshow(np.concatenate(flow_16.session.run(flow_16.states[5].density).data[...,0], axis=1), origin='lower', cmap='magma')
pylab.show()


