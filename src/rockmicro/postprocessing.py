"""Minkowski-functional and transport post-processing utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import porespy as ps
from skimage import io
from skimage.measure import euler_number, perimeter_crofton


def create_paraview_script(
    in_filename: str | Path,
    output_name: str | Path,
    pos_x: float = 0.0,
    pos_y: float = 0.0,
    n_points: int = 100,
    read_exodus: bool = True,
) -> Path:
    ''' Convert exodus file to csv file using Paraview.
      @param[in] in_filename - string, input exodus filename
      @param[in] line - list, [[x1,y1],[x2,y2]] coords of line to extract data on
      @param[in] precision - int, number of significant digits required
    '''
    tmp_dir = Path("tmp_paraview_dir")
    # Create tmp directory if need be
    if not tmp_dir.is_dir():
      print('Creating temporaray Paraview export directory')
      tmp_dir.mkdir(parents=True)
    
    if not Path(in_filename).is_file():
      raise FileNotFoundError(f"Exodus input file not found: {in_filename}")

    # Create a Paraview script file to ask Paraview to do the data extraction for us
    print('Creating command file for Paraview')
    command_filename = tmp_dir / "paraview_commands.py"
    with command_filename.open("w") as f_com:
        command = f'''
# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
import os
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'ExodusIIReader'
model_1_pf_0320_rad_0005_res_005_outpute = ExodusIIReader(FileName=["{in_filename}"])
# Use forward slashes in this path; backslashes cause an error.
model_1_pf_0320_rad_0005_res_005_outpute.ElementVariables = ['product'] #'gradP_']
model_1_pf_0320_rad_0005_res_005_outpute.PointVariables = ['vel_', 'p']
model_1_pf_0320_rad_0005_res_005_outpute.GlobalVariables = []
model_1_pf_0320_rad_0005_res_005_outpute.NodeSetArrayStatus = []
model_1_pf_0320_rad_0005_res_005_outpute.SideSetArrayStatus = []

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.GoToLast()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()
UpdatePipeline(time=1.0, proxy=model_1_pf_0320_rad_0005_res_005_outpute)
animationScene1.GoToLast()

# Properties modified on model_1_pf_0320_rad_0005_res_005_outpute
model_1_pf_0320_rad_0005_res_005_outpute.ElementBlocks = ['block', 'Unnamed block ID: 2'] #pores
model_1_pf_0320_rad_0005_res_005_outpute.FilePrefix = ''
model_1_pf_0320_rad_0005_res_005_outpute.FilePattern = ''

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(Input=model_1_pf_0320_rad_0005_res_005_outpute)
cellDatatoPointData1.CellDataArraytoprocess = ['product']

# create a new 'Gradient Of Unstructured DataSet' #(This creates the gradient, based on the points (first input), of the property (second point))
gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=cellDatatoPointData1)
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'GlobalNodeId']
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'p']

# create a new 'Calculator'
calculator1 = Calculator(Input=gradientOfUnstructuredDataSet1)
calculator1.Function = 'Gradients_X*vel__X+Gradients_Y*vel__Y'

# create a new 'Clip'
# clip1 = Clip(Input=cellDatatoPointData1)
clip1 = Clip(Input=calculator1) #gradientOfUnstructuredDataSet1)
clip1.ClipType = 'Box'
clip1.Scalars = ['POINTS', 'ObjectId']
clip1.Value = 1.5
clip1.Invert = 1
clip1.ClipType.Position = [0.0, 0.0, -0.1]
clip1.ClipType.Length = [1.0, 1.0, 0.2]

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(Input=clip1)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
#spreadSheetView1.BlockSize = 1024L

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1)
        '''
        for i in range(1,101): #91): #writing for every block from 1 - 100 size to integrate in the text command
            index = str(i).zfill(3)
            clip_pos_x = 0.5 - i * 0.5 / n_points
            clip_pos_y = 0.5 - i * 0.5 / n_points
            length = i / n_points
            command += f'''
# Properties modified on clip1.ClipType
clip1.ClipType.Position = [{clip_pos_x}, {clip_pos_y}, -0.1]
clip1.ClipType.Length = [{length}, {length}, 0.2]

# save data
SaveData("{output_name}_{index}.csv", proxy=integrateVariables1)
print("Succesfully created {output_name}_{index}.csv")
            '''
        f_com.write(command) #writing the actual python file with the text command
    return command_filename
        
def compute_properties(
    sample_image: str | Path, axis: int = 0
) -> tuple[float, float, int, float]:
    """Compute porosity, perimeter, Euler characteristic, and tortuosity.

    White pixels are interpreted as pore space, matching the convention used by
    the published dataset and manuscript.
    """
    image = Path(sample_image)
    if not image.is_file():
        raise FileNotFoundError(f"Image file not found: {image}")

    grayscale = io.imread(image, as_gray=True)
    pore_space = grayscale > (150 / 255.0)
    solid_space = ~pore_space

    m0 = float(ps.metrics.porosity(pore_space))
    m1 = float(perimeter_crofton(solid_space, directions=4))
    m3 = int(euler_number(solid_space, connectivity=1))

    try:
        result = ps.simulations.tortuosity_fd(im=pore_space, axis=axis)
        tau = result['tortuosity']
    except Exception as e:
        error_msg = str(e)
        if (
            "No pores remain after trimming floating pores" in error_msg or
            "Solver failed to converge" in error_msg or
            "exit code: 1000" in error_msg
        ):
            print(f"Warning: tau computation failed for {image}; using infinity")
            tau = np.inf
        else:
            raise  # Let other unexpected errors propagate
    
    return m0, m1, m3, float(tau)


def Obtaining_properties(
    sample_image: str | Path, axis: int = 0
) -> tuple[float, float, int, float]:
    """Backward-compatible alias for :func:`compute_properties`."""
    return compute_properties(sample_image, axis)

def average_diameter(file: str | Path) -> float:
    """Return the mean particle diameter from an ``x y z radius`` text file."""
    data = pd.read_csv(file, sep=r"\s+", header=None)
    data.columns = ['x', 'y', 'z', 'r']
    return float(2 * data['r'].mean())


def Average_diameter(FILE: str | Path) -> float:
    """Backward-compatible alias for :func:`average_diameter`."""
    return average_diameter(FILE)
