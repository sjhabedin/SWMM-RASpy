import h5py
import win32com.client as win
import os
import shutil
import pandas as pd
import sys
from inputs_framework import *


lcndata = pd.read_csv(framework_directory+'\\'+'lcndataset.csv') # Load landcover data from the csv file #

count = 0
if len(sys.argv) > 1:
    count = int(sys.argv[1])
#count_suffix = str(count)
#file_name_with_count = f"filename_{count_suffix}.txt"

    
def update_mannings_n(gfile, lcndata_row):
    
    # updates Manning's n values in the HEC-RAS geometry HDF file #

    gdset = gfile.get("/Geometry/Land Cover (Manning's n)/Calibration Table")
    items = []
    for item in gdset:
        land_cover_name = item[0].decode('utf-8').replace("b'", "").replace("'", "")
        if land_cover_name in lcndata_row.index:
            item[1] = lcndata_row[land_cover_name]
        items.append(item)

    del gfile["/Geometry/Land Cover (Manning's n)/Calibration Table"]
    gfile.create_dataset("/Geometry/Land Cover (Manning's n)/Calibration Table", data=items)

def run_simulation_and_copy_output(x):

    # Runs the HEC-RAS simulation and copies the output to a new file for each trial #
    
    #Run the parent HEC-RAS model#
    hec = win.Dispatch("RAS610.HECRASController")
    hec.project_open(rasprojectfile)
    hec.Compute_CurrentPlan(None, None, True)
    hec.quitras()
    del hec
    
    #copy the output information from the model's run to a new HDF file#
    if x==count:
        dummy_rasoutfile = os.path.join(framework_directory, f"{rasprojectfilename.split('.')[0]}{x}_output.hdf")
        shutil.copy(org_rasoutfile, dummy_rasoutfile)
    if x>count:
        dummy_rasoutfile = os.path.join(framework_directory, f"{rasprojectfilename.split('.')[0]}{x}_output.hdf")
        shutil.copy(org_rasoutfile, dummy_rasoutfile)
    if x<count:
        dummy_rasoutfile = os.path.join(framework_directory, f"{rasprojectfilename.split('.')[0]}{count}_output.hdf")
        shutil.copy(org_rasoutfile, dummy_rasoutfile)


for x in range(len(lcndata)):
    
    #update the parent geometry file with new Manning's n#
    with h5py.File(org_rasgeomfile, "r+") as gfile:
        update_mannings_n(gfile, lcndata.iloc[x])
        
    run_simulation_and_copy_output(x)
    
print('\n\nRAS simulation finished')

