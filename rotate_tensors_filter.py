# -*- coding: utf-8 -*-
"""Custom paraview filter to map line orientation to cells."""
import numpy as np
from paraview.util.vtkAlgorithm import smdomain, smproperty, smproxy
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


@smproxy.filter(label="Rotate Tensors")
@smproperty.input(name="Source", port_index=0)
@smdomain.datatype(
    dataTypes=["vtkUnstructuredGrid"], composite_data_supported=False
)
class RotateTensorsFilter(VTKPythonAlgorithmBase):
    """RotateTensorsFilter.

    Attributes
    ----------
    _rotation : list of float
        Rotation around x,y,z axis.

    """

    def __init__(self):
        """Set up the filter."""
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            nOutputPorts=1,
            outputType="vtkUnstructuredGrid",
        )
        self._rotation = [0.0, 0.0, 0.0]

    def FillInputPortInformation(self, port, info):
        """Require unstructured grids as input types."""
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkUnstructuredGrid")
        return 1

    @smproperty.doublevector(name="Rotation", default_values=[0.0, 0.0, 0.0])
    @smdomain.doublerange()
    def SetRotation(self, rx, ry, rz):
        """Create an input field for the rotation and save it."""
        self._rotation = [rx, ry, rz]
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        """Process the request submitted after applying the filter."""
        input = vtkUnstructuredGrid.GetData(inInfo[0])

        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfo))
        output.ShallowCopy(input)

        for key, value in zip(output.CellData.keys(), output.CellData):
            shape = value.shape
            if len(shape) > 2:
                rot = self.RotateTensor(value, self._rotation)
                output.CellData.append(rot, key + "(rotated)")

        for key, value in zip(output.PointData.keys(), output.PointData):
            shape = value.shape
            if len(shape) > 2:
                rot = self.RotateTensor(value, self._rotation)
                output.PointData.append(rot, key + "(rotated)")

        return 1

    def RotateTensor(self, T, rotation):
        """Apply three consecutive external rotations around x, y, z axis.

        Parameters
        ----------
        T : VTKArray
            An array of tensors to be rotated.
        rotation : tuple of float
            The three rotation angles around the x,y,z axis.

        Returns
        -------
        VTKArray
            A rotated tensor array.

        """
        rx = rotation[0] / 180.0 * np.pi
        ry = rotation[1] / 180.0 * np.pi
        rz = rotation[2] / 180.0 * np.pi
        Rx = np.array(
            [
                [1, 0, 0],
                [0, np.cos(rx), -np.sin(rx)],
                [0, np.sin(rx), np.cos(rx)],
            ]
        )
        Ry = np.array(
            [
                [np.cos(ry), 0, np.sin(ry)],
                [0, 1, 0],
                [-np.sin(ry), 0, np.cos(ry)],
            ]
        )
        Rz = np.array(
            [
                [np.cos(rz), -np.sin(rz), 0],
                [np.sin(rz), np.cos(rz), 0],
                [0, 0, 1],
            ]
        )
        return self.Rotate(self.Rotate(self.Rotate(T, Rx), Ry), Rz)

    def Rotate(self, T, R):
        """Apply Rayleigh product to all tensors in the array

        Parameters
        ----------
        T : VTKArray
            An array of tensors to be rotated.
        R : type
            Description of parameter `R`.

        Returns
        -------
        VTKArray
            A rotated tensor array.

        """
        return np.array([np.einsum("mi,nj,ij->mn", R, R, t) for t in T])
