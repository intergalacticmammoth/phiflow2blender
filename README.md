# tum-logo
A cool simulation using the [phiflow](https://github.com/tum-pbs/PhiFlow/ ) differentiable fluid solver.



The obstacles created in the code are numbered according to the legend below. The black boxes denote inflows and the white spaces are empty domain. Same colored boxes are same sized obstacles.

<img src="readme_imgs/obstacle_numbering_legend.png" width="500" />

## 2D Version

### Simulation (res:256)
![](readme_imgs/tum2D.gif)

### Learning the T from a blob (res:32)
The initial simulation starts as a blob with zero buoyancy. 

![](readme_imgs/blob32.png)
*Simulation before optimization*

The target was generated using a *100-frame simulation* at res=32 and dt=0.5. The optimized density fields for a *30-frame simulation* were obtained after training for 300 epochs.

![](readme_imgs/t_sim.png) ![](readme_imgs/t_first.gif)

### Learning the TUM from 3 blobs

Learning the whole TUM proved to be much more difficult. As a target, an image of the logo was used. It was converted to a numpy array in python. An attempt has been made for simulation to learn the target at three different resolutions. The current results are shown below.

The relevant notebook is [this one](./differentiable-sims/tum/simple_tum.ipynb).

<img src="readme_imgs/tum_target_32.png" width="360" />

#### Res: 16x24

![](readme_imgs/tum_res08.gif)

#### Res: 32x48

![](readme_imgs/tum_res16.gif)

#### Res: 64x96

![](readme_imgs/tum_res32.gif)

It seems that the higher the resolution, the better the optimization can approximate the target, but also the computational cost increases significantly.

## 3D Version

![](readme_imgs/tum3D.gif)

The 3D version was rendered using the open-source free software [Blender](https://www.blender.org/). More details on the rendering process and setup soon.
