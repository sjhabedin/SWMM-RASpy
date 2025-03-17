import numpy as np
import pandas as pd
import os
import h5py
from inputs_framework import *

def find_hdf_files_with_output(directory, keyword='output'):
    
    return [file for file in os.listdir(directory) if file.endswith('.hdf') and keyword in file]

def extract_and_save_data(directory, filenames, flow_area_name, output_variable_names, output_file_prefix):
    path_to_results = '/Results/Unsteady/Output/Output Blocks/Base Output/Unsteady Time Series/2D Flow Areas'
    
    for output_variable_name in output_variable_names:  
        path_to_outvar = f"{path_to_results}//{flow_area_name}//{output_variable_name}"
        
        for i, infile in enumerate(filenames):
            with h5py.File(os.path.join(directory, infile), 'r') as rfile:
                data_ccc = np.array(rfile.get(f'/Geometry/2D Flow Areas/{flow_area_name}/Cells Center Coordinate'))
                data_outvar = np.transpose(np.array(rfile.get(path_to_outvar)))
                data_merged = np.column_stack((data_ccc, data_outvar))
                
                df = pd.DataFrame(data_merged)
                output_filename = f"{output_file_prefix}{i}_{output_variable_name}.csv"  
                df.to_csv(os.path.join(directory, output_filename), index=False)

def parent_process(directory, project_filename, flow_area_name, output_variable_names):
    
    hdf_files = find_hdf_files_with_output(directory)
    output_file_prefix = project_filename.split('.')[0]
    extract_and_save_data(directory, hdf_files, flow_area_name, output_variable_names, output_file_prefix)

parent_process(directory_infiles, rasprojectfilename, name_flowarea, name_outvar)
