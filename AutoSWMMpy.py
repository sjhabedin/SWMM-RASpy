import pandas as pd
import numpy as np
import subprocess as sp, os, shutil
import pyswmm
from pyswmm import Simulation
import swmmtoolbox
import csv
from inputs_framework import *

# RainfallSimulator is a class created to generate Chicago Storms #

class RainfallSimulator:
    def __init__(self, directory, ttot, b, c, r, precip_interval, year, month, day):
        self.directory = directory
        self.ttot = ttot
        self.b = b
        self.c = c
        self.r = r
        self.precip_interval = precip_interval
        self.year = year
        self.month = month
        self.day = day
        
    def load_intensity_data(self):
        # Load intensity data from CSV file
        intensities = []
        with open(intensitydata, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                intensities.append(float(row['Intensity']))
        return intensities
    
    def generate_rainfall_events(self):
        # Load intensity data
        intensities = self.load_intensity_data()

        # Simulate rainfall events and save data to files
        time_int_hrs = round(self.precip_interval / 60, 3)
        A = [x * ((time_int_hrs + self.b) ** self.c) for x in intensities]

        for i, a in enumerate(A):
            iprcp, hours, minutes = self.calculate_rainfall(a, intensities[i])
            self.save_rainfall_data(i, iprcp, hours, minutes, a)


    def calculate_rainfall(self, a, max_intensity):
        #Calculate incremental rainfall#
        tp = self.r * self.ttot
        t = 0
        tprcp = []
        while t <= self.ttot:
            t += round(self.precip_interval / 60, 3)
            if t < tp:
                prcp = round(max_intensity - ((a * (tp - t)) / (((tp - t) / self.r) + self.b) ** self.c), 3)
            else:
                prcp = round(max_intensity + ((a * (t - tp)) / (((t - tp) / (1 - self.r)) + self.b) ** self.c), 3)
            tprcp.append(prcp)

        iprcp = [tprcp[j + 1] - tprcp[j] for j in range(len(tprcp) - 1)]
        hours, minutes = self.calculate_time_sequence(len(iprcp))
        return iprcp, hours, minutes

    def calculate_time_sequence(self, length):
        #Calculate the time sequence for rainfall data#
        hours = [0]
        minutes = [self.precip_interval]
        for _ in range(1, length):
            next_minutes = minutes[-1] + self.precip_interval
            if next_minutes >= 60:
                hours.append(hours[-1] + 1)
                minutes.append(next_minutes - 60)
            else:
                hours.append(hours[-1])
                minutes.append(next_minutes)
        return hours, minutes

    def save_rainfall_data(self, index, iprcp, hours, minutes, a):
        #Save rainfall data to a file#
        stid = f'chicago_{self.ttot}hr{index + 1}'
        sid = [stid for _ in range(len(iprcp))]
        yy = [self.year for _ in range(len(iprcp))]
        mm = [self.month for _ in range(len(iprcp))]
        dd = [self.day for _ in range(len(iprcp))]
        comp_array = np.column_stack([sid, yy, mm, dd, hours, minutes, iprcp])
        #out_array = np.insert(comp_array, 0, ('', '', '', '', '', '', ''), axis=0)
        out_array=comp_array
        filename = f'chicago{self.ttot}hr_a{round(a,2)}.dat'
        with open(os.path.join(self.directory, filename), 'w') as f:
            for item in out_array:
                f.write(' '.join(map(str, item)) + '\n')

if __name__ == "__main__":
    simulator = RainfallSimulator(
        directory=directory_rainfiles,
        ttot=rainfall_duration,
        b=B,
        c=C,
        r=R,
        precip_interval=rainfall_interval,
        year=year_rainfall,
        month=month_rainfall,
        day=day_rainfall
    )
    simulator.generate_rainfall_events()


def update_swmm_input_file(dummy_swmmfile, directory_rainfiles, file_name, rain_gage_params, var='[RAINGAGES]'):
    #Updates the SWMM input file with new rainfall data#
    rainfile = os.path.join(directory_rainfiles, file_name)
    is_raingages_section = False
    raingage_index = None
    with open(dummy_swmmfile, "r") as file:
        elements = file.readlines()

    for n, element in enumerate(elements):
        if element.strip() == var:
            is_raingages_section = True
            continue
        if element.strip().startswith('[') and element.strip() != var:
            is_raingages_section = False
        if is_raingages_section and rain_gage_params['raingagename'] in element:
            raingage_index = n
            print(raingage_index)
            break
    if raingage_index is None:
        print(f"Raingage {rain_gage_params['raingagename']} not found in the [RAINGAGES] section.")
    else:
        elm_index = elements[raingage_index].split()
        elm_index = list(filter(None, elm_index))
        elm_index[0] = rain_gage_params['raingagename']
        elm_index[1] = rain_gage_params['rainformat']
        elm_index[2] = rain_gage_params['raininterval']
        elm_index[3] = rain_gage_params['snowfactor']
        elm_index[4] = rain_gage_params['raindatasourcetype']
        with open(rainfile, "r") as rfile:
            next(rfile)  
            rainfile_line = rfile.readline().split()
            stationid = rainfile_line[0]
        elm_index[5] = os.path.join(directory_rainfiles, file_name) + ' ' + stationid + ' ' + rain_gage_params['rainunit']
        elements[raingage_index] = ' '.join(elm_index[:6]) + '\n'
        with open(dummy_swmmfile, "w") as file:
            file.writelines(elements)
    print ('fine')

def run_swmm_simulation(dummy_swmmfile):
    #run a SWMM simulation#
    sim = Simulation(dummy_swmmfile)
    print ('running')
    sim.execute()

def extract_and_save_node_data(outfile, node, directory_SWMMoutfiles, iter_number):
    #extracts and saves node data from the SWMM output file#
    filename = f"{outfile.split('.')[0]}_{node}.txt"
    sp.call(f'swmmtoolbox extract {outfile} node,{node},>{filename}', shell=True)
    destfile = os.path.join(directory_SWMMoutfiles, f"{org_swmmfilename.split('.')[0]}{iter_number}_{node}.txt")
    {org_swmmfilename.split('.')[0]}
    shutil.move(filename, destfile)
    return destfile

def process_node_data(destfile, node, nodes):
    #Processes node data and returns a DataFrame#
    datetime = []
    nodedata = []
    with open(destfile, "r") as dfile:
        elements = dfile.readlines()
        for e,element in enumerate(elements):
            if element.strip():
                split_element = element.split(",")
                datetime.append(split_element[0])
                data_element = split_element[5] if node != nodes[-1] else split_element[1]
                if e==0:
                    nodedata.append(data_element)
                else:
                    nodedata.append(round(float(data_element), 2))
    nodedata[0] = f"{node}_{'flow' if node != nodes[-1] else 'depth'}"
    datetime_index = pd.Index(datetime, name='datetime')   
    return pd.DataFrame(nodedata,index=datetime_index)

def main(directory_model, org_swmmfile, directory_rainfiles, nodes, directory_SWMMoutfiles, dummySWMM_model, rain_gage_params):
    filearray = [f for f in os.listdir(directory_rainfiles) if f.endswith('.dat')]
    for i, item in enumerate(filearray):
        dummy_swmmfile = os.path.join(dummySWMM_model, f"{org_swmmfilename.split('.')[0]}{i}.inp")
        shutil.copyfile(org_swmmfile, dummy_swmmfile)
        update_swmm_input_file(dummy_swmmfile, directory_rainfiles, item, rain_gage_params)
        run_swmm_simulation(dummy_swmmfile)
        outfile = os.path.join(dummySWMM_model, f"{org_swmmfilename.split('.')[0]}{i}.out")
        all_node_data = []
        for node in nodes:
            destfile = extract_and_save_node_data(outfile, node, directory_SWMMoutfiles, i)
            node_data = process_node_data(destfile, node, nodes)
            all_node_data.append(node_data)
        # Combine and process all node data and save to csv file #
        combined_df = pd.concat(all_node_data, axis=1)
        columnname_new = combined_df.iloc[0]
        combined_df = combined_df[1:]
        combined_df.columns = columnname_new
        combined_df.iloc[:,-1] = pd.to_numeric(combined_df.iloc[:,-1], errors='ignore')
        combined_df.iloc[:,-1] = combined_df.iloc[:,-1]+117.50
        combined_df.to_csv(os.path.join(directory_SWMMoutfiles, f"{org_swmmfilename.split('.')[0]}{i}.csv"), index=True)
    print('\n\nSWMM simulation finished')

if __name__ == "__main__":
    main(directory_model, org_swmmfile, directory_rainfiles, nodes, directory_SWMMoutfiles, dummySWMM_model, rain_gage_params)
