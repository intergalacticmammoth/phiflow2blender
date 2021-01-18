from phi.tf.flow import *  # Causes deprecation warnings with TF 1.15
import pylab
import numpy as np
import scipy.interpolate as sc_interp
import imageio
import pylab
from tensorflow.python.distribute.distribute_lib import _DefaultDistributionExtended
import os


#===================================================================================
# TUM FLOW CLASS
#===================================================================================
class TUM_flow(World):

    def __init__(self, params):
        super().__init__()

        self.session = Session(None)
        self.target = None
        #self.optimized_velocities = []

        self.res = params["res"]
        self.frames = params["frames"]
        self.optim_steps = params["optim_steps"]

        buoyancy = 0.0
        rate = 5
        radius = 2

        self.fluid = self.add(Fluid(Domain([2*self.res, 3*self.res], boundaries=CLOSED), buoyancy_factor=buoyancy), physics=IncompressibleFlow())
        self.__setup_geometry(res=self.res, radius=radius, rate=rate)

        #Tensorflow setup for velocity
        self.fluid.velocity = variable(self.fluid.velocity)  # create TensorFlow variable
        self.states = []
        self.states.append(self.fluid.state)  # Remember the state at t=0 for later visualization
        self.session.initialize_variables()



    def __setup_geometry(self, res, radius, rate):
        self.add(Inflow(Sphere(center=[0.3*res,1.5*res], radius=radius), rate=rate))
        self.add(Inflow(Sphere(center=[0.3*res,0.75*res], radius=radius), rate=rate))
        self.add(Inflow(Sphere(center=[0.3*res,2.25*res], radius=radius), rate=rate))

    def build_graphs(self):
        for frame in range(self.frames):
            print('Building graph for frame %d' % frame)
            self.step(dt=0.5)
            self.states.append(self.fluid.state)

        print('Computing frames...')

    def set_target(self, img_path):

        self.target = imageio.imread(img_path)
        self.target = self.target[:,:,0]
        self.target = np.flip(self.target)
        self.target = self.target[:,::-1]
        self.target = np.expand_dims(self.target, axis=0)
        self.target = np.expand_dims(self.target, axis=3)

        #normalize the target values to have similar magnitude to the simulation densities
        val1 = np.max(self.fluid.density.data[0:,...])
        val2 = np.max(self.target)
        self.target = val1/val2 * self.target 

        #return target

    def train(self):
        #Define loss, optimizer and start the session
        loss = math.l2_loss(self.fluid.density.data[0:,...] - self.target)
        optim = tf.train.AdamOptimizer(learning_rate=0.25).minimize(loss)
        self.session.initialize_variables()
        print('Initial loss: %f' % self.session.run(loss))

        #Run optimization
        for optim_step in range(self.optim_steps):
            print('Running optimization step %d. %s' % (optim_step, '' if optim_step else 'The first step sets up the adjoint graph.'))
            _, loss_value = self.session.run([optim, loss])
            print('Loss: %f' % loss_value)

    def get_optimized_velocities(self):

        optimized_velocities = []

        for i in range(self.frames):
            optimized_velocities.append(self.session.run(self.states[0].velocity).at_centers())

        return optimized_velocities

    def get_densities(self):
        
        densities = []

        for i in range(self.frames):
            densities.append(self.session.run(self.states[0].density).at_centers())

        return densities
#-----------------------------------------------------------------------------------


