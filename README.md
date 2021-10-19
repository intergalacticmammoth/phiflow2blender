# phiflow2blender Tutorial

This repo demonstrates a pipeline for creating a smoke simulation in 
[phiflow](https://github.com/tum-pbs/PhiFlow) and rendering the result in [Blender](https://www.blender.org/). 
It aims to focus on the visualisation in Blender part, so more in depth tutorials on phiflow can be found in 
phiflow's [github repo](https://github.com/tum-pbs/PhiFlow) and also [this](https://youtube.com/playlist?list=PLYLhRkuWBmZ5R6hYzusA2JBIUPFEE755O) 
exciting new YouTube series by it's main developer. 

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

>Note: It is also possible to do this using the pyopenvdb module, but when I had issues installing the
>module and abandoned the effort.
3. Load the OpenVDB frame sequence in Blender, setup the scene in Blender and render! Since this is 
quite complicated to describe in text format, I have created [this](https://youtu.be/xI1ARz4ZSQU) video for you to follow along! :)

[![Youtube tutorial Video](https://img.youtube.com/vi/xI1ARz4ZSQU/0.jpg)](https://www.youtube.com/watch?v=xI1ARz4ZSQU)

The resulting file from the video is [tutorial_video.blend](tutorial/tutorial_video.blend) and the file I used for the final version is [final.blend](tutorial/final.blend).



## Dependencies:

 - [phiflow 2.0](https://github.com/tum-pbs/PhiFlow#installation)
 - [mantaflow](http://mantaflow.com/install.html)
 - [Blender >= 2.91](https://www.blender.org/download/)


## Contributions:
Feel free to open an issue or a PR if you have any improvements or suggestions!
