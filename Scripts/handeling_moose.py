import subprocess, sys, os
import pandas as pd, numpy as np, pyvista as pv

def parse_template(image, output_name):
    
    template_file = f'Simulation_files/Navier-Stokes_FCP_2D_image_template.i'
    data_file_path = 'Simulation_files/Navier-Stokes_FCP_2D_image_input.i'
    path = os.getcwd()
    
    with open(template_file, 'r') as f:
        template = f.read()

    input_data = {
        "image": image,
        "output_name": output_name
    }

    if mat_model == "DP":
        input_data["psi"] = material_properties["int_friction_angle"]

    data_file = template.format(**input_data)
    with open(data_file_path, 'w') as f:
        f.write(data_file)
    return data_file_path
        
def call_MOOSE(MOOSE_input_file, mpi_mode='mpiexec', mpi_processes=1, n_threads=15, executable_path="your/executable/path/moose"):
        """
        a function that calls the moose executable
        """
        data_file_path = MOOSE_input_file
        executable_cmd = executable_path

        args = [mpi_mode,'-n', f'{mpi_processes}' , executable_cmd, '-i', data_file_path, f'--n-threads={n_threads}']
        process = subprocess.Popen(args, 
                                    stdout = subprocess.PIPE, 
                                    stderr = subprocess.STDOUT,
                                    cwd = os.getcwd(),
                                    universal_newlines=True, 
                                    text = True)
        
        for line in iter(process.stdout.readline, ""):
            sys.stdout.write('\n'+line[:-1])
            sys.stdout.flush() 

def run_simulation(image, output_name):
    data_file_path = parse_template(image, output_name)
    call_MOOSE(data_file_path)