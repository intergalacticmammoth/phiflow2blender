from phi.flow import *
import pylab
import time
import os

#TODO: Change this accordingly
scene = Scene.create('/home/intergalactic-mammoth/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/git-repo/tum-logo/2D/data')


num = 0




res = 32   #TODO: HIGH RESOLUTION! SLOW...
rt = 7      #inflow rate
bf = 0.05    #buoyancy factor
frames = 500
step_sz = 0.25
obs = 1
speed = 0.035


world = World()
fluid = world.add(Fluid(Domain([2*res, 3*res], boundaries=CLOSED), velocity=10.0, buoyancy_factor=bf), physics=IncompressibleFlow())
world.add(Inflow(box[0.31*res:0.45*res, 0.5*res:0.65*res], rate = 1.3*rt))
world.add(Inflow(box[0.31*res:0.45*res, 1.1*res:1.5*res], rate = rt))
world.add(Inflow(box[0.31*res:0.45*res, 2.05*res:2.2*res], rate = 1.2*rt))
world.add(Inflow(box[0.31*res:0.45*res, 2.6*res:2.75*res], rate = 1.2*rt))


if obs:
    world.add(Obstacle(box[0:2*res, 0:0.2*res]))        #obs1
    world.add(Obstacle(box[0:2*res, 2.8*res:3*res]))    #obs2
    world.add(Obstacle(box[0:1.45*res, 0.2*res:0.43*res]))  #obs3
    world.add(Obstacle(box[0:0.3*res, 0.66*res:2.56*res]))  #obs4
    world.add(Obstacle(box[1.7*res:2*res, 0.2*res:2.8*res]))  #obs5
    world.add(Obstacle(box[0.3*res:1.45*res, 0.66*res:0.9*res]))  #obs6
    world.add(Obstacle(box[0.3*res:1.45*res, 1.7*res:1.97*res]))  #obs7
    world.add(Obstacle(box[0.3*res:1.45*res, 2.3*res:2.55*res]))  #obs8
    world.add(Obstacle(box[0.55*res:1.7*res, 1.15*res:1.42*res])) #obs9



for frame in range(frames):
    
    start = time.time()
    world.step(dt=step_sz)
    end = time.time()
    scene.write(fluid.state, frame=frame)
    print('Step %d done, %.3f seconds elapsed' % (frame, end-start))

    #pylab.imshow(np.concatenate(fluid.density.data[...,0], axis=1), origin='lower', cmap='magma')
    #plt_name = 'frame%d_bf%d_rt%d_dt%d'
    #save_name = savedir + plt_name + '.png'
    #pylab.savefig(save_name % (num, frame, bf*10, rt*10, step_sz*100), bbox_inches='tight')
    #pylab.show()


print('Exiting simulation...')
