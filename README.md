# SWMM-RASpy Framework

The **SWMM-RASpy Framework** is a suite of Python scripts designed to automate the process of sampling hydrologic and hydraulic parameters, running hydrologic (PCSWMM) and hydraulic (HEC-RAS 2D) simulations, and extracting model outputs for subsequent analysis. The framework aims to facilitate stochastic flood modeling and risk assessment by coupling two widely used modeling systems under varying climate and land cover conditions.

---

## Overview

The framework streamlines the following processes:

- **Parameter Sampling:** Uses Latin Hypercube Sampling to generate a range of rainfall intensities and Manning’s n (land cover roughness) values.
- **Hydrologic Simulation:** Modifies and runs a SWMM model (via PCSWMM) using generated rainfall data.
- **Hydraulic Simulation:** Updates HEC-RAS boundary conditions with SWMM output, modifies the HEC-RAS geometry with new land cover parameters, and runs the HEC-RAS simulation.
- **Output Extraction:** Reads HEC-RAS HDF output files and extracts time series data for designated flow areas and variables.

The entire workflow is coordinated through a master script that sequentially calls the individual modules.

---

## System Requirements

- **Software:**
  - EPA SWMM (version 5.0 or greater)
  - HEC-RAS (version 5.0 or greater)
  - HEC-DSSVue (version 3.0 or greater) – required for running parts of the HEC-RAS integration in a Jython environment
- **Python:**
  - Python 3.6 or greater
  - Required packages:
    - numpy
    - pandas
    - h5py
    - PySWMM
    - swmmtoolbox
    - pywin32 (for win32com in `rasexecutepy.py`)

---

## Installation Instructions

1. **Install the required modeling software:**
   - Download and install [EPA SWMM](https://www.epa.gov/water-research/storm-water-management-model-swmm) and [HEC-RAS](https://www.hec.usace.army.mil/software/hec-ras/).
   - Install [HEC-DSSVue](https://www.hec.usace.army.mil/software/hec-dssvue/) for HEC-DSS database management.

2. **Set up the Python environment:**
   - Ensure Python 3.6+ is installed.
   - Install the necessary Python packages (e.g., via `pip install numpy pandas h5py pyswmm swmmtoolbox pywin32`).

3. **Download the repository:**
   - Clone or download the project repository to your local machine.
   - Make sure that the directory structure is maintained, as the scripts use relative paths defined in `inputs_framework.py`.

---

## Workflow

The overall workflow of the project is orchestrated by the `master.py` script, which executes the following sequence:

1. **Initialization:**
   - **`inputs_framework.py`**  
     Sets up all input parameters, file directories, and simulation settings for both SWMM and HEC-RAS models.

2. **Parameter Sampling:**
   - **`AutoSAMPpy.py`**  
     Uses Latin Hypercube Sampling to generate:
     - Rainfall intensity dataset (`intensitydataset.csv`)
     - Land cover (Manning’s n) dataset (`lcndataset.csv`)

3. **Hydrologic Simulation:**
   - **`AutoSWMMpy.py`**  
     - Updates the SWMM input file with the generated rainfall data.
     - Runs SWMM simulations using the PySWMM and swmmtoolbox libraries.
     - Extracts node flow and stage data from the SWMM simulation outputs.

4. **Hydraulic Simulation and Integration:**
   - **`AutoRASpy.py`**  
     - Reads SWMM output CSV files.
     - Updates the HEC-RAS boundary conditions through HEC-DSSVue.
     - Calls **`rasexecutepy.py`** to update the HEC-RAS geometry file with sampled Manning’s n values and run simulations.
   - **`rasexecutepy.py`**  
     - Iterates through the land cover dataset.
     - Updates the geometry HDF file with corresponding Manning’s n values.
     - Runs the HEC-RAS simulation via the HEC-RAS controller.
     - Copies and uniquely identifies HEC-RAS output files after each simulation run.

5. **Output Extraction:**
   - **`AutoRAS-HDFpy.py`**  
     - Scans the directory for HEC-RAS HDF output files.
     - Extracts specified time series data (e.g., water surface elevation and cell invert depth) from defined flow areas.
     - Merges cell coordinate data with the extracted time series data.
     - Saves the final results as CSV files for further analysis.

6. **Data Consolidation:**
   - After the simulations, non-Python files (e.g., CSV outputs, HDF files) are moved to a designated data directory for organized storage.

---

## Running the Project

1. **Preparation:**
   - Verify that all necessary software and Python dependencies are installed.
   - Update the file paths and simulation parameters in `inputs_framework.py` if needed.
   - Ensure that the parent SWMM and HEC-RAS model files are correctly set up and that the models run as expected independently.

2. **Execute the master script:**
   - Open a terminal or command prompt in the project’s root directory.
   - Run the command:
     ```bash
     python master.py
     ```
   - The master script will call each module in sequence and eventually move the output data files to the `Data` folder.

---

## Script Descriptions

- **`inputs_framework.py`**  
  Defines directories, filenames, simulation parameters, and model-specific settings. This file is critical as it provides the configuration for all subsequent scripts.

- **`AutoSAMPpy.py`**  
  Performs Latin Hypercube Sampling to generate:
  - Rainfall intensity samples saved as `intensitydataset.csv`
  - Land cover (Manning’s n) sample datasets saved as `lcndataset.csv`

- **`AutoSWMMpy.py`**  
  Automates the modification of SWMM input files with new rainfall data, runs SWMM simulations, and extracts node data (e.g., flow and stage hydrographs) for use in HEC-RAS.

- **`AutoRASpy.py`**  
  Integrates the SWMM output with HEC-RAS by updating boundary conditions through HEC-DSSVue. This script internally calls `rasexecutepy.py` to update the HEC-RAS geometry with sampled Manning’s n values and run simulations.

- **`rasexecutepy.py`**  
  Iterates over the generated land cover data, updates the HEC-RAS geometry file with new Manning’s n values, and executes the HEC-RAS simulation via the HEC-RAS controller. Copies and stores output HDF files for each simulation run.

- **`AutoRAS-HDFpy.py`**  
  Searches for HEC-RAS HDF output files, extracts specified time series data from defined flow areas, and saves the results as CSV files for further analysis.

- **`master.py`**  
  Serves as the central orchestrator. It sequentially calls each of the above scripts, manages temporary file movements (e.g., to the HEC-DSSVue scripts directory), and organizes the final output into a dedicated data folder.

---

## Considerations

- **HEC-DSSVue Environment:**  
  `AutoRASpy.py` must be executed within the HEC-DSSVue environment (a Jython-based environment). The framework handles this by temporarily copying necessary files and moving scripts as needed.

- **Input Data Integrity:**  
  Ensure that the parent models (SWMM and HEC-RAS) are fully operational before running the framework. All parameters (e.g., rainfall intensities, land cover ranges) should be verified in `inputs_framework.py`.

- **File Organization:**  
  The framework uses relative paths defined in `inputs_framework.py`. It is important to maintain the prescribed directory structure to avoid path errors.

---

## License and Contributions

---

## Contact

For questions or further information about the SWMM-RASpy Framework, please contact at sayedabedin.joy@gmail.com
