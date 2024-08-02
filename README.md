# Droplet Counting

This project is designed to count and visualize droplets in an image using computer vision techniques. The main functionality includes counting the number of droplets in a given image and plotting the detected droplets.

## Abstract
Complex coacervation occurs when oppositely charged polyelectrolytes interact, leading to liquid-liquid phase separation. We coupled this phase separation to a chemical reaction cycle, leading to active droplets that emerge when fuel is supplied and dissolve when the energy source is depleted. These behaviors make them an exciting protocell model and a promising step toward de novo life. However, these active coacervate droplets cannot self-divide, a crucial characteristic of life. This work demonstrates how to design division in active complex coacervate droplets. We found that mixtures of long and short polystyrene sulfonate lead to tiny speckles inside the active droplets made of the long PSS. As the droplet dissolves, these speckles liberate as daughter droplets. We could rescue the offspring by adding a second batch of fuel. Finally, we showed that we can include molecules partitioning in the complex coacervates, which stay in the offspring until they eventually dissolve. Combining our mechanism for self-division and replicators, which have feedback on the coacervate droplets, gives rise to evolution experiments in synthetic cells.

## Code

This project uses OpenCV to detect and count droplets in an image or image time series. A tif-file with either one image or a time series is required as input. For the analysis, we first smoothed the grayscale images to reduce the noise using Gaussian blur. The blurred images were then converted into a binary mask using a defined threshold. Every pixel which has an intensity above 15 was considered as a signal and the intensity was set to 255. Pixels with a intensity below 15 were considered as background and were set to 0. The binary mask was used to determine the size of the droplets in the mask. We set the minimal size of a droplet to 0.24 μm, which is the resolution of the used confocal objective. Everything below that size is not considered in the counting step and is treated as an image artefact. The remaining droplets in the mask are counted and plotted over time. 

## Features

- Count droplets in a given image/ image time series
- Visualize detected droplets

### Prerequisites

- Python 3.x
- OpenCV
- NumPy
- Matplotlib
