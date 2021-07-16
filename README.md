# A Simple Phi-flow Tutorial

This repo aims to demonstrate a pipeline for creating a fluid simulation in phiflow and rendering the result in Blender.

## Workflow
1. Write a phiflow simulation and save the resulting frames as compressed numpy arrays (.npz).
2. Process the frames in mantaflow and output them in OpenVDB format.
3. Load the OpenVDB frame sequence in Blender.
4. Setup the scene in Blender and render!

## Dependencies:

 - phiflow 2.0
 - Blender >= 2.91
