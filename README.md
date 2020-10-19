## Netfig

yet another network configlet/configuration generator.

#### What it does:
netfig is a simple network configlet/configuration generator where variables are defined by column headers in a .csv file. These variables then pass on the contents in the columns over to a jinja2 template then exports then as .txt files to a user defined directory. For example the column header would be 'vrf' and the contents would be 'TestVrf', the jinja2 format to define the variable in the template would need to be in this format {{ vrf }}, matching the header of the csv for the variable that needs to be replaced. E.g 'ip vrf forwarding {{ vrf }}', will then be 'ip vrf forwarding TestVrf'.

Each row will create a new file, based on the first columns variables. 

#### Requirements:
This has been tested using python 3.8.
Please see requirements.txt and install via pip install -r requirements.txt perferably in ones favorite virtual environment.

#### Usage:

 1. Define the project_dir variable with the parent directory desired within the script.
 2. Define csv and jinja2 template, reference example in this repository.
 3. Run the script: python3.8 variables.csv template.j2
 4. Check output folder!


