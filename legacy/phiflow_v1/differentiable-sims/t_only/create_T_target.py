from phi.flow import *
import pylab
import time
import os

#TODO: Change this accordingly
scene = Scene.create('target/')
savedir = 'target/vis/scene_%d/'

num = 0

while True:    
    
    if not os.path.exists(savedir%(num)):
        os.mkdir(savedir%(num))
        break
    else:
        num = num + 1
        if not os.path.exists(savedir%(num)):
            os.mkdir(savedir%(num))
            break


res = 32
rt = 5      #inflow rate
bf = 0.05    #buoyancy factor
frames = 100
step_sz = 0.5
obs = 1
speed = 0.035


world = World()
fluid = world.add(Fluid(Domain([int(1.5*res), res], boundaries=CLOSED), velocity=10.0, buoyancy_factor=bf), physics=IncompressibleFlow())
world.add(Inflow(box[0.1*res:0.3*res, 0.45*res:0.55*res], rate = rt))


if obs:
    world.add(Obstacle(box[0:res, 0:0.35*res]))
    world.add(Obstacle(box[0:res, 0.65*res:res]))
    world.add(Obstacle(box[1.2*res:1.5*res, 0:res]))


for frame in range(frames):
    
    start = time.time()
    world.step(dt=step_sz)
    end = time.time()
    print('Step %d done, %.3f seconds elapsed' % (frame, end-start))
    scene.write(fluid.state, frame = frame )

    pylab.imshow(np.concatenate(fluid.density.data[...,0], axis=1), origin='lower', cmap='magma')
    plt_name = 'frame%d_bf%d_rt%d_dt%d'
    save_name = savedir + plt_name + '.png'
    pylab.savefig(save_name % (num, frame, bf*10, rt*10, step_sz*100), bbox_inches='tight')
    #pylab.show()


print('Exiting simulation...')