# phiflow2blender Tutorial

This repo demonstrates a pipeline for creating a smoke simulation in 
[phiflow](https://github.com/tum-pbs/PhiFlow) and rendering the result in [Blender](https://www.blender.org/). 

More in depth tutorials on phiflow can be found in phiflow's [github repo](https://github.com/tum-pbs/PhiFlow). 

Using the scripts provided in this repo, we will produce this visualization:

![Final Result](readme_media/blue_white.gif)

Looks cool right? Let's dive into it!

## Workflow
1. Write a phiflow simulation and save the resulting frames as compressed 
numpy arrays (.npz). For example, see [plume.py](tutorial/plume.py) or [TUM.py](tutorial/TUM.py)
2. Process the frames in [mantaflow](http://mantaflow.com/install.html) and output them in OpenVDB format. Blender has great support to 
easily import OpenVDB volumes. To convert your simulation files, you have to run the [manta2vdb.py](tutorial/manta2vdb.py) 
script using [mantaflow](http://mantaflow.com/install.html), with the following arguments:
- `-d path-to-the-input-file`
- `-res X-resolution Y-resolution Z-resolution`

>**IMPORTANT**: This script assumes your simulation has a scalar field named "smoke" and a vector
>field named "velocity". You can tweak this to your needs.

For example: 
`./path/to/manta path/to/manta2vdb.py -d path/to/scene/data -res 64 64 64 `

3. Load the OpenVDB frame sequence in Blender, setup the scene in Blender and render! Since this is 
quite complicated to describe in text format, I have created [this](https://youtu.be/xI1ARz4ZSQU) video for you to follow along! :)

The resulting file from the video is [tutorial_video.blend](tutorial/tutorial_video.blend) and the file I used for the final version is [final.blend](tutorial/final.blend).



## Dependencies:

 - [phiflow 2.0](https://github.com/tum-pbs/PhiFlow#installation)
 - [mantaflow](http://mantaflow.com/install.html)
 - [Blender >= 2.91](https://www.blender.org/download/)


