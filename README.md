# phiflow2blender Tutorial

This repo aims to demonstrate a pipeline for creating a smoke simulation in 
[phiflow](https://github.com/tum-pbs/PhiFlow) and rendering the result in [Blender](https://www.blender.org/). 

This is the final result we will produce:

![Final Result](readme_media/blue_white.gif)

Looks cool right? Let's dive into it!

## Workflow
1. Write a phiflow simulation and save the resulting frames as compressed 
numpy arrays (.npz). For example, see [plume.py](tutorial/plume.py) or [TUM.py](tutorial/TUM.py)
2. Process the frames in mantaflow and output them in OpenVDB format. 
You have to run the [manta2vdb.py](tutorial/manta2vdb.py) script using mantaflow, 
with the necessary arguments, i.e. the input data and the X, Y and Z resolution of the simulation. 

**IMPORTANT**: This script assumes your simulation has a scalar field named "smoke" and a vector
field named "velocity". You can tweak this to your needs.

`./path/to/manta path/to/manta2vdb.py -d path/to/scene/data -res X Y Z `

3. Load the OpenVDB frame sequence in Blender, setup the scene in Blender and render!
   
   Follow along [this]() video :)

The resulting file from the video is [tutorial_video.blend](tutorial/tutorial_video.blend) and the file I used for the final version is [final.blend](tutorial/final.blend).



## Dependencies:

 - [phiflow 2.0](https://github.com/tum-pbs/PhiFlow#installation)
 - [mantaflow](http://mantaflow.com/install.html)
 - [Blender >= 2.91](https://www.blender.org/download/)

The [legacy](legacy/) folder contains various tests and scripts that were created along the journey, but are not directly relevant anymore. They're not the prettiest code you'll see, but feel free to explore them.
