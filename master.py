import subprocess
import shutil
import os

#Define Python path and its version #
python = r'C:\Users\sjhabedi\AppData\Local\Programs\Python\Python38\python.exe'

# Get current working directory of the Framework's python programs #
current_directory = os.getcwd()

# Define paths to the python programs #
inputs_framework_path = os.path.join(current_directory, 'inputs_framework.py')
autosamppy_path = os.path.join(current_directory, 'AutoSAMPpy.py')
autoswmmpy_path = os.path.join(current_directory, 'AutoSWMMpy.py')
autoraspy_path = os.path.join(current_directory, 'AutoRASpy.py')
rasexecutefile_path = os.path.join(current_directory, 'rasexecutepy.py')  #called inside AutoRASpy#
autorashdfpy_path=os.path.join(current_directory, 'AutoRAS-HDFpy.py')

# Define the HEC-DSSVue program path and the target directory for AutoRASpy #
hecdss_program = r'C:\Program Files\HEC\HEC-DSSVue\HEC-DSSVue'
target_dir = r'C:\Users\sjhabedi\AppData\Roaming\HEC\HEC-DSSVue\scripts'

# Function to run python scripts #
def run_python_script(script_path):
    subprocess.run([python, script_path], check=True)


# Function to move and run AutoRASpy within HEC-DSSVue #
def run_in_hecdss(script_path, inputs_framework_path, target_dir, hecdss_program):
    original_file = os.path.join(current_directory, os.path.basename(script_path))
    inputs_framework_current_directory = os.path.join(current_directory, os.path.basename(inputs_framework_path))

    shutil.copy(inputs_framework_current_directory, os.path.join(target_dir,os.path.basename(inputs_framework_path)))
    shutil.move(original_file, target_dir)

    os.chdir(target_dir)

    subprocess.run([hecdss_program, os.path.join(target_dir,os.path.basename(script_path))], shell=True) #AutoRASpy script is run#

    shutil.move(os.path.join(target_dir,os.path.basename(script_path)), current_directory)
    os.remove(os.path.join(target_dir,os.path.basename(inputs_framework_path)))
 
    os.chdir(current_directory)
 
# Call the functions to run python scripts in order #
if __name__ == "__main__":
    run_python_script(inputs_framework_path)
    run_python_script(autosamppy_path)
    run_python_script(autoswmmpy_path)
    run_in_hecdss(autoraspy_path, inputs_framework_path, target_dir, hecdss_program)
    run_python_script(autorashdfpy_path)

# Process to move all the data files except python scripts from the current directory to the directory where the files will be eventually stored #

current_directory = os.getcwd()
datatransfer_dir = os.path.join(current_directory, 'Data')

if not os.path.exists(datatransfer_dir):
    os.makedirs(datatransfer_dir)

for filename in os.listdir(current_directory):
    file_path = os.path.join(current_directory, filename)

    if os.path.isfile(file_path) and not filename.endswith('.py'):
        shutil.move(file_path, os.path.join(datatransfer_dir, filename))

print('\n\nFramework is successfully run')

