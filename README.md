# phiflow2blender Tutorial

This repo aims to demonstrate a pipeline for creating a fluid simulation in phiflow and rendering the result in Blender.

## Workflow
1. Write a phiflow simulation and save the resulting frames as compressed numpy arrays (.npz).
2. Process the frames in mantaflow and output them in OpenVDB format.
3. Load the OpenVDB frame sequence in Blender, setup the scene in Blender and render!
    Follow along [this]() video :)
        1. Open [this file]() in Blender. Load the .vdb files.
        2. Select the volume object and go to the Object Data Properties tab. There you will see the available grids. This you will have to put
        in the "Density Attribute" of the smoke material.
        3. Edit the material to your liking.
        4. Adjust the camera and render settings.
        5. Render! 



## Dependencies:

 - phiflow 2.0
 - mantaflow
 - Blender >= 2.91



