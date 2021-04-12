import pandas as pd 
from jinja2 import *
from colorama import init
from colorama import Fore
import os
import sys
from datetime import datetime

#start time for script
start_time = datetime.now()

##Define Script Header
script_header = '''
╔══════════════════════════════════════════════════════╗
║              Network Configlet Generator                  ║
╠══════════════════════════════════════════════════════╣
║ This script generates configlets in seperate files        ║
║ based on the first column on CSV variables. User          ║
║ input defines the output location, if the directory       ║
║ doesn't exist, the directory will be created.             ║
╚══════════════════════════════════════════════════════╝
'''

#resets colorama colors#
init(autoreset=True)


## script header output
print(Fore.CYAN +  script_header)
print(Fore.RED + '\nUsage Example:' + Fore.CYAN + 'netfig.py variables.csv jinjatemplate.j2')
print(Fore.WHITE + '\n' + '-' * 70)
print('\n' * 3)


## Define Usage ##
if len(sys.argv) < 3:
    print(Fore.WHITE + '\n' + '*' * 70)
    print('\n')
    print(Fore.RED + 'Usage Error. Try Again. Working Usage Example:' + Fore.CYAN +  'netfig.py variables.csv jinjatemplate.j2')   ##this Script #commands in a list #device type and login type
    print('\n')
    print(Fore.WHITE + '*' * 70)
    print('\n')
    exit()



## define csv variables ##
csv_var = sys.argv[1]

## Ensure system arugment filetype is csv
check_csv = os.path.splitext(csv_var)[1]
if '.csv' not in check_csv:
    print(Fore.RED + 'Error: First Argument must be in CSV format.' + '\n')
    sys.exit()

## define jinja template to use ## 
template_var = sys.argv[2]

## Ensure system arugment filetype is csv
check_jaytwo = os.path.splitext(template_var)[1]
if '.j2' not in check_jaytwo:
    print(Fore.RED + 'Error: Second Argument must be in Jinja2 format.' + '\n')
    sys.exit()

print('\n' + Fore.CYAN + 'Starting netfig.....')

#project directory based in user input
project_dir = input('\n' + Fore.CYAN + 'Enter the name of the project directory where configlets will be placed: ')

#statically defined directory 
#Checks if project directory exists or not, overwrites if user instructs to do so.

output_dir = '/YOURDIRECTORYHERE/netfig/{}'.format(project_dir)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
else:
    print('\n' + Fore.RED + 'Error: Directory already exists...')    
    overwrite = input('\n' + Fore.WHITE + 'Overwrite?: y = yes, n = no: ')
    if overwrite.lower() == 'y':
        print('\n' + Fore.GREEN + 'Overwriting...')
    else:
        print('\n' + Fore.RED + 'Directory remains, please rerun script and choose different name. Exiting...')
        sys.exit()
        
print('\n' + Fore.CYAN + 'Output will be placed into the directory: ' + Fore.RED + '{}'.format(output_dir))
print('\n' * 4)

## Reads the CSV Data
df = pd.read_csv(csv_var, na_filter=False, dtype=str)
data_list = df.to_dict('records')

## Jinja environment and defining template from sys argument ##
env = Environment(loader=FileSystemLoader(searchpath="."))
template = env.get_template(template_var)


## loop to replace variables based on jinja template and renders accordingly ##
## outputs each row as its own file ##
for keys in data_list:
    config = template.render(keys)
    fname = list(keys.values())[0]
    with open(os.path.join(output_dir,fname + '.txt'), 'w') as outputfile:
            outputfile.write(config)


## outputs all content as a single file, helpful for one config for one device ##
## this file is stored in main directory ##
for keys in data_list:
    config = template.render(keys)
    with open("output-singlefile.txt", 'a') as singleoutput:
        singleoutput.write(config)
        
## exiting script
print(Fore.WHITE + '\n..')
print(Fore.WHITE + '\n.....')
print(Fore.WHITE + '\n........')
print(Fore.WHITE + '\nScript completed successfully, please check output directory for configlets: ')
print(Fore.RED + '{}'.format(output_dir))
print(Fore.WHITE + '\nTotal Elapsed time: ' + str(datetime.now() - start_time))
