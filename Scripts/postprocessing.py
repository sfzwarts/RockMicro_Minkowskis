import sys, subprocess, os, runpy, csv, numpy as np
from fileinput import filename

def create_paraview_script(in_filename, output_name, pos_x, pos_y, n_points=100, read_exodus=True):
    ''' Convert exodus file to csv file using Paraview.
      @param[in] in_filename - string, input exodus filename
      @param[in] line - list, [[x1,y1],[x2,y2]] coords of line to extract data on
      @param[in] precision - int, number of significant digits required
    '''
    tmp_dir = "tmp_paraview_dir"   
    # Create tmp directory if need be
    if not os.path.isdir(tmp_dir):
      print('Creating temporaray Paraview export directory')
      os.makedirs(tmp_dir)
    
    if not os.path.isfile(in_filename):
      print("Something goes wrong with the input file, it doesn't exist.")
      sys.exit()

    # Create a Paraview script file to ask Paraview to do the data extraction for us
    print('Creating command file for Paraview')
    command_filename = os.path.join(tmp_dir, 'paraview_commands.py')
    with open(command_filename, 'w') as f_com:
        command = '''
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
#make sure the path is set with / instead of \ or \\, otherwise gives an error
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
        '''.format(in_filename=in_filename, output_name=output_name)
        for i in range(1,101): #91): #writing for every block from 1 - 100 size to integrate in the text command
            command = command +'''
# Properties modified on clip1.ClipType
clip1.ClipType.Position = [{pos_x}, {pos_y}, -0.1]
clip1.ClipType.Length = [{length}, {length}, 0.2]

# save data
SaveData("{output_name}_{index}.csv", proxy=integrateVariables1)
print("Succesfully created {output_name}_{index}.csv")
            '''.format(in_filename=in_filename, output_name=output_name, index=str(i).zfill(3),
                pos_x=0.5-i*0.5/n_points, pos_y=0.5-i*0.5/n_points, length=i*1/n_points)
        f_com.write(command) #writing the actual python file with the text command