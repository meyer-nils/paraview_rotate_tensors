[![LICENSE](https://black.readthedocs.io/en/stable/_static/license.svg)](https://raw.github.com/nilsmeyerkit/paraview_rotate_tensors/master/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Paraview Transform Tensors
Paraview's default 'Transform' filter does not rotate tensors with the transformation.
Hence, this filter can be applied seperately to rotate tensors with the mesh according to

<img src="https://latex.codecogs.com/svg.latex?\tilde{\mathbf{T}}=\mathbf{R}_z\mathbf{R}_y\mathbf{R}_x\mathbf{T}\mathbf{R}_x^\top\mathbf{R}_y^\top\mathbf{R}_z^\top"/>,

where the rotation matrices are defined in the initial frame (external rotation angles). Therefore you should be able to simple copy the 'Transform' roation angles to this filter for matching rotations.
The plugin requires Paraview 5.8 or higher. Load the plugin to Paraview via 'Tools' -> 'Manage Plugins...' -> 'Load New'.
