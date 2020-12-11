# tum-logo
A cool simulation using the [phiflow](https://github.com/tum-pbs/PhiFlow/ ) differentiable fluid solver.



The obstacles created in the code are numbered according to the legend below. The black boxes denote inflows and the white spaces are empty domain. Same colored boxes are same sized obstacles.

<img src="readme_imgs/obstacle_numbering_legend.png" width="500" />

## 2D Version

### Simulation (res:256)
![](readme_imgs/tum2D.gif)

### Learning the T from a blob (res:32)
The simulation starts as a blob with zero buoyancy, with only 20 frames. 

![](readme_imgs/blob32.png)
*Simulation before optimization*

The target was generated using a 100-frame simulation at res=32 and dt=0.5

![](readme_imgs/t_sim.png) ![](readme_imgs/t_first.gif)
          *Target for optimizing the densities*                            *Optimized densities*

The optimized density after 300 epochs


## 3D Version

![](readme_imgs/tum3D.gif)

The 3D version was rendered using the open-source free software [Blender](https://www.blender.org/). More details on the rendering process and setup soon.