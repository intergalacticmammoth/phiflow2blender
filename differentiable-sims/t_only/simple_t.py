from phi.tf.flow import *  # Causes deprecation warnings with TF 1.15
import pylab
session = Session(None)  # Used to run the TensorFlow graph

#setup
save_imgs = False
res = 32
buoyancy = 0.0
rate = 8

#Create the simulation
world = World()
fluid = world.add(Fluid(Domain([48, 32], boundaries=CLOSED), buoyancy_factor=0.0), physics=IncompressibleFlow())
world.add(Inflow(Sphere(center=[6,16], radius=3), rate=8));
fluid.velocity = variable(fluid.velocity)  # create TensorFlow variable
states = []
states.append(fluid.state)  # Remember the state at t=0 for later visualization
session.initialize_variables()

#Build tensorflow graphs
for frame in range(30):
  print('Building graph for frame %d' % frame)
  world.step(dt=0.5)
  states.append(fluid.state)

#Define loss function
#Want the densities of the right blob to match the ones of the left blob (target)
arr = np.load("target/sim_000001/density_000099.npz")
target = arr['arr_0']
loss = math.l2_loss(fluid.density.data[0:,...] - target)
optim = tf.train.AdamOptimizer(learning_rate=0.1).minimize(loss)
session.initialize_variables()
print('Initial loss: %f' % session.run(loss))

#Run optimization
for optim_step in range(300):
  print('Running optimization step %d. %s' % (optim_step, '' if optim_step else 'The first step sets up the adjoint graph.'))
  _, loss_value = session.run([optim, loss])
  print('Loss: %f' % loss_value)


##Uncomment to see what the optimization did
#pylab.imshow(np.concatenate(session.run(fluid.density).data[...,0], axis=1), origin='lower', cmap='magma')


#Get the optimized velocity fields
optimized_velocity_field = session.run(states[0].velocity).at_centers()

##Uncomment to see the optimized X and Y velocity fields
#pylab.title('Initial y-velocity (optimized)')
#pylab.imshow(np.concatenate(optimized_velocity_field.data[...,0], axis=1), origin='lower')
#pylab.title('Initial x-velocity (optimized)')
#pylab.imshow(np.concatenate(optimized_velocity_field.data[...,1], axis=1), origin='lower')


#Save the plots for the optimized fluid densities
save_dir = 'vis/'

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

if (save_imgs):
    for i in range(len(states)):
        save_name = save_dir + "t_frame%03d.png"
        pylab.imshow(np.concatenate(session.run(states[i].density).data[...,0], axis=1), origin='lower', cmap='magma')
        pylab.savefig(save_name % (i), bbox_inches='tight')