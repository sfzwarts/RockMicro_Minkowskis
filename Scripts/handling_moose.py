import subprocess, sys, os
import pandas as pd, numpy as np, pyvista as pv

def parse_template_image(image, output_name):
    
    template_file = f'Simulation_files/Navier-Stokes_FCP_2D_image_template.i'
    data_file_path = 'Simulation_files/Navier-Stokes_FCP_2D_image_input.i'
    path = os.getcwd()
    
    with open(template_file, 'r') as f:
        template = f.read()

    input_data = {
        "image": image,
        "output_name": output_name
    }
    data_file = template.format(**input_data)
    with open(data_file_path, 'w') as f:
        f.write(data_file)
    return data_file_path

def parse_template_mesh(image, output_name):
    
    template_file = f'Simulation_files/Navier-Stokes_FCP_2D_mesh_template.i'
    data_file_path = 'Simulation_files/Navier-Stokes_FCP_2D_mesh_input.i'
    path = os.getcwd()
    
    with open(template_file, 'r') as f:
        template = f.read()

    input_data = {
        "image": image,
        "output_name": output_name
    }
    data_file = template.format(**input_data)
    with open(data_file_path, 'w') as f:
        f.write(data_file)
    return data_file_path        

def call_MOOSE(data_file_path)
    command = f'moose -i {data_file_path}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running MOOSE simulation: {stderr.decode()}")
    else:
        print(f"MOOSE simulation completed successfully: {stdout.decode()}")

def run_simulation_image(image, output_name):
    data_file_path = parse_template_image(image, output_name)
    call_MOOSE(data_file_path)

def run_simulation_mesh(image, output_name):
    data_file_path = parse_template_mesh(image, output_name)
    call_MOOSE(data_file_path)