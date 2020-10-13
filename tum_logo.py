from phi.flow import *
import pylab
import time
import os

scene = Scene.create('/home/intergalactic-mammoth/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/phiflow/scene')
savedir = 'imgs/scene_%d/'

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


res = 128
rt = 2      #inflow rate
bf = 0.005    #buoyancy factor
frames = 100
step_sz = 0.5
obs = 0
speed = 0.1

def T_inflow(time):

    val = 0.3*res+0.3*res*(time*speed)

    threshold = 0.6*1.5*res 

    if val < threshold:
        return Sphere([0.8*res, val], radius = 0.0125*res)
    else:
        return Sphere([0.8*res-0.8*res*(time*speed*2), threshold], radius = 0.0125*res)

def M_inflow(time):

    #movement of flow in X dir
    valX = 1.1*res-1.1*res*(time*speed)
    
    #movement of flow in Y dir
    valY = 0.2*res + 0.2*res*(time*speed)

    threshold = 0.8*1.5*res 

    if valY < threshold:
        return Sphere([valY, 1.1*res], radius = 0.0125*res)
    else:
        return Sphere([0.8*res, valX], radius = 0.0125*res)

world = World()
fluid = world.add(Fluid(Domain([res, int(1.5*res)], boundaries=OPEN), buoyancy_factor=bf), physics=IncompressibleFlow())
world.add(Inflow(T_inflow(0), rate = rt), physics=GeometryMovement(T_inflow))
world.add(Inflow(M_inflow(0), rate = rt), physics=GeometryMovement(M_inflow))


if obs:
    world.add(Obstacle(Sphere(center=[0.7*res,0.5*res], radius=0.0625*res)))

for frame in range(frames):
    
    start = time.time()
    world.step(dt=step_sz)
    end = time.time()
    print('Step %d done, %.3f seconds elapsed' % (frame, end-start))

    pylab.imshow(np.concatenate(fluid.density.data[...,0], axis=1), origin='lower', cmap='magma')
    plt_name = 'frame%d_bf%d_rt%d_dt%d'
    save_name = savedir + plt_name + '.png'
    pylab.savefig(save_name % (num, frame, bf*10, rt*10, step_sz*100), bbox_inches='tight')
    pylab.show()



print('Exiting simulation...')
