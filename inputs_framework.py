import os

# Define the root directory for the framework
framework_root = os.path.abspath("framework_root")

# Define directories using relative paths
framework_directory = framework_root
directory_model = os.path.join(framework_directory, "SWMMmodel") #directory of parent SWMM model#
dummySWMM_model = os.path.join(directory_model, "DummySWMMModels") #directory of dummy SWMM models where the new models/input files will be created after the simulation runs# 

directory_SWMMoutfiles = framework_directory #directory where output files from SWMM model will be stored#
directory_rainfiles = framework_directory #directory where rainfall files produced by Chicago Storm method will be stored# #
directory_infiles = framework_directory #directory where the HEC-RAS HDF output files are saved before they are moved to the datatransfer_dir defined in master.py script#

# Parent SWMM model input file
org_swmmfilename = 'SWMMmodel.inp'
org_swmmfile = os.path.join(directory_model, org_swmmfilename)

# Parent HEC-RAS model project file
rasprojectfilename = 'RASmodel.prj'
rasprojectfilepath = os.path.join(framework_root, "RASmodel")
rasprojectfile = os.path.join(rasprojectfilepath, rasprojectfilename)

# Parent HEC-RAS model files
org_rasgeomfile = os.path.join(rasprojectfilepath, 'RASmodel.g01.hdf') #geometry file#
org_rasoutfile = os.path.join(rasprojectfilepath, 'RASmodel.p01.hdf') #output HDF file#
org_rasHECDSS = os.path.join(rasprojectfilepath, 'RASmodel.dss') #HEC-DSS file#

# Rain gauge information
raingagename = 'Waterloo_CHICAGO' #raingage name in the parent SWMM model#
rainformat = 'VOLUME' #format of rainfall data#
raininterval = '0:05' #time interval of rainfall event#
snowfactor = '1.0' #leave it as 1#
raindatasourcetype = 'FILE' #source type of rainfall data to the SWMM model, leave it as FILE#
rainunit = 'MM' #unit of rain, change based on 'rainformat'#

rain_gage_params = {
    'raingagename': raingagename,
    'rainformat': rainformat,
    'raininterval': raininterval,
    'snowfactor': snowfactor,
    'raindatasourcetype': raindatasourcetype,
    'rainunit': rainunit
}

# SWMM & HEC-RAS nodes
nodes = ["US_BC2", "US_BC1", "DS_BC"]   #sample SWMM nodes#
nodes_ras = ['USleft', 'USright', 'DS'] #sample HEC-RAS nodes#

# Land cover data
lcndata = "lcndataset.csv"   #dataset where Manning's n values for each landcover will be stored#
land_cover_ranges = {
    'Developed': (0.048, 0.24),
    'Wetland': (0.036, 0.18),
    'ChannelBanks': (0.02, 0.096),
    'Channel': (0.012, 0.054)
    }                            #samle n vales for different land covers#

# Simulation parameters
runs_hydrologic = 1 # the number of simulation runs for hydrologic model, i.e the number of rainfall intensity samples #
runs_hydraulic = 3  # the number of Manning's n sample sets for the land covers #

# Rainfall generator parameters
intensitydata = "intensitydataset.csv" #dataset where rainfall intensities will be saved#
low_rainfallintensity = 100
high_rainfallintensity = 120
intensity_range = (low_rainfallintensity, high_rainfallintensity) #range of rainfall intensities#

# parameters needed for Chicago Storm event#
rainfall_duration = 3 #total duration of rainfall#
B = 0.334 #IDF curve's B coefficient#
C = 0.837 #IDF curve's C coefficient#
R = 0.35  #time to peak factor#
rainfall_interval = 5 #time interval of rainfall#
year_rainfall = 2020 #year of rainfall event#
month_rainfall = 6 #month of rainfall event#
day_rainfall = 1  #day of rainfall event#

# HEC-RAS model computation parameters
comp_startdate = '31May2020'
comp_starttime = '24:00'
comp_timeline = '31May2020-01Jun2020'
comp_interval = '5minute'
comp_identifier = 'v01'

# HEC-RAS output variables
name_outvar = ['Water Surface', 'Cell Invert Depth'] # variable for which data will be extracted from HEC-RAS HDF output files #
