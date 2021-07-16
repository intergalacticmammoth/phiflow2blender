from phi.tf.flow import *  # Causes deprecation warnings with TF 1.15
import pylab
import os
session = Session(None)  # Used to run the TensorFlow graph


#Create 2 batch sim, target and source blob
#buoyancy is set to zero
world = World()
fluid = world.add(Fluid(Domain([32, 32], boundaries=CLOSED), buoyancy_factor=0.0, batch_size=2), physics=IncompressibleFlow())
world.add(Inflow(Sphere(center=[[16,14], [16, 18]], radius=3), rate=0.1));
fluid.velocity = variable(fluid.velocity)  # create TensorFlow variable
states = []
states.append(fluid.state)  # Remember the state at t=0 for later visualization
session.initialize_variables()

#Build tensorflow graphs
for frame in range(10):
  print('Building graph for frame %d' % frame)
  world.step(dt=1.5)
  states.append(fluid.state)


#Define loss function
#We want the densities of the right blob to match the ones of the left blob (target)
target = session.run(fluid.density).data[0,...]
loss = math.l2_loss(fluid.density.data[1:,...] - target)
optim = tf.train.AdamOptimizer(learning_rate=0.075).minimize(loss)
session.initialize_variables()
print('Initial loss: %f' % session.run(loss))


#Run optimization
for optim_step in range(300):
  print('Running optimization step %d. %s' % (optim_step, '' if optim_step else 'The first step sets up the adjoint graph.'))
  _, loss_value = session.run([optim, loss])
  print('Loss: %f' % loss_value)


#Get the optimized velocity field
optimized_velocity_field = session.run(states[0].velocity).at_centers()


#Save the plots for the optimized fluid densities
save_dir = 'vis/'

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)


for i in range(len(states)):
    save_name = save_dir + "blob_frame%d.png"
    pylab.imshow(np.concatenate(session.run(states[i].density).data[...,0], axis=1), origin='lower', cmap='magma')
    pylab.savefig(save_name % (i), bbox_inches='tight')