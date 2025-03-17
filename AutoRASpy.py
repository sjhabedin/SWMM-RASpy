# All hec modules from HEC-DSSVue #

from hec.script import Plot
from hec.heclib.dss import HecDss, DSSPathname
from hec.io import TimeSeriesContainer
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime

# python modules compatible with Jython #
import java
import os
import sys
import subprocess as sp
import csv
import time as tm
import re
from datetime import datetime as dt

# Set working directory for 'inputs_framework' to be recognized by HEC-DSSVue program #
roaming_dir = os.environ.get('APPDATA')
part_path='HEC\HEC-DSSVue\scripts'
temp_dir=roaming_dir+'\\'+part_path
sys.path.append(temp_dir)
from inputs_framework import *


def read_csv_data(filename, column_index):
    data_csv = []
    with open(filename, "r") as datafile:
        csv_reader = csv.reader(datafile)
        next(csv_reader)
        for row in csv_reader:
            if not row:
                continue
            data_csv.append(float(row[column_index]))
    return data_csv

def write_to_dss(theFile, bclines, file):
    tsc = TimeSeriesContainer()
    tsc_parta = 'BCLINE'
    
    print(file)
    
    for i, item in enumerate(bclines):
        full_path, tsc_units = construct_full_path(tsc_parta, item, comp_timeline, comp_interval, comp_identifier, i == len(bclines) - 1)
        tsc.fullName = full_path
        tsc.units = tsc_units
        start = HecTime(comp_startdate, comp_starttime)
        tsc.interval = int(re.findall(r'\d+', comp_interval)[-1])
        bcdata = read_csv_data(file, i + 1)
        
        times = [start.value() + tsc.interval * e for e in range(len(bcdata))]
        
        tsc.times = times
        tsc.values = bcdata
        tsc.numberValues = len(bcdata)
        tsc.type = "INST-VAL"
        theFile.put(tsc)
    
    print("Processed file")


def construct_full_path(part_a, item, part_d, part_e, part_f, is_stage):
    part_b = item
    part_c = 'STAGE' if is_stage else 'FLOW'
    tsc_units = "m" if is_stage else "CMS"
    full_path = '/{}/{}/{}/{}/{}/{}/'.format(part_a, part_b, part_c, part_d, part_e, part_f)
    return full_path, tsc_units

def record_count(count, directory):
    counts = str(count)
    with open(os.path.join(directory, 'countsfile.txt'), 'w') as countsfileout:
        countsfileout.write(counts)

def run_external_script(script_path, count):
    starttime = tm.time()
    sp.call(['python', script_path,str(count)], shell=True)
    endtime = tm.time()
    return round((endtime - starttime), 2)

def main():
    
    theFile = HecDss.open(org_rasHECDSS)
    bclines = [name_flowarea + ": " + node for node in nodes_ras]
    filearray = [os.path.join(directory_SWMMoutfiles, file) for file in os.listdir(directory_SWMMoutfiles) if file.endswith('.csv') and file.startswith(os.path.splitext(org_swmmfilename)[0])]
    
    for f, file in enumerate(filearray):
        write_to_dss(theFile, bclines, file)  
        record_count(f, framework_directory)  
        rasexecute_path = os.path.join(framework_directory, 'rasexecutepy.py')
        rasrun = run_external_script(rasexecute_path, f) # the rasexecute script is called #
    
    theFile.close()

    #print('\n\nHEC-RAS model run completed. Computational time:', rasrun)

if __name__ == "__main__":
    main()
